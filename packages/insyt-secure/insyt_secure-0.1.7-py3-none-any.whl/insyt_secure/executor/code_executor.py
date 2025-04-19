import os
import json
import asyncio
import logging
import io
import sys
import re
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Tuple, List, Optional
import concurrent.futures
import threading
import time
import paho.mqtt.client as mqtt
import uuid
import platform

# Configure module-level logger
logger = logging.getLogger(__name__)

class NetworkRestrictionError(Exception):
    """Exception raised when attempting to connect to a restricted network."""
    pass

class CodeExecutionTimeoutError(Exception):
    """Exception raised when code execution exceeds the timeout."""
    pass

class CodeExecutor:
    """
    Executes Python code snippets received via secure communication channel.
    
    The execution timeout can be specified in two ways:
    1. As a default value when initializing the executor
    2. Dynamically in each message payload with the "execution_time" key
    
    If "execution_time" is present in the message, it will override the default timeout
    for that specific execution.
    """
    def __init__(self, mqtt_broker, mqtt_port, mqtt_username, mqtt_password, subscribe_topic, 
                 publish_topic=None, ssl_enabled=False, allowed_ips=None, always_allowed_domains=None, 
                 max_workers=5, execution_timeout=30):
        """
        Initialize the CodeExecutor with connection details.
        
        All connection parameters are required and must be provided explicitly.
        
        Args:
            mqtt_broker: Broker hostname or IP
            mqtt_port: Broker port
            mqtt_username: Username
            mqtt_password: Password
            subscribe_topic: Topic to subscribe to
            publish_topic: Topic to publish results to (if None, will use response_topic from individual messages)
            ssl_enabled: Whether to use SSL for connection
            allowed_ips: Optional list of allowed IPs/hostnames (with optional ports)
            always_allowed_domains: Domains that are always allowed regardless of IP restrictions
            max_workers: Maximum number of concurrent executions (default: 5)
            execution_timeout: Maximum execution time in seconds for each code snippet (default: 30)
        """
        # Connection parameters - must be provided explicitly
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_username = mqtt_username
        self.mqtt_password = mqtt_password
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic
        self.ssl_enabled = ssl_enabled
        self.allowed_ips = allowed_ips
        self.always_allowed_domains = always_allowed_domains or []
        
        # Execution parameters
        self.pod_name = os.getenv('POD_NAME', 'local-executor')
        self.max_workers = max_workers
        self.execution_timeout = execution_timeout  # Store default timeout
        
        # MQTT message tracking for diagnostics
        self.message_received_count = 0
        self.message_published_count = 0
        self.message_published_topics = set()  # Keep track of all topics we've published to
        self.message_received_topics = set()   # Keep track of all topics we've received from
        self.last_message_time = 0
        
        logger.info(f"Setting up executor with {self.max_workers} concurrent workers")
        logger.info(f"Execution timeout set to {self.execution_timeout} seconds")
        logger.info(f"SSL enabled: {self.ssl_enabled}")
        
        # Log sensitive information only at debug level
        logger.debug(f"Input channel: {self.subscribe_topic}")
        logger.debug(f"Output channel: {self.publish_topic}")
        
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        
        # Create a queue for coordinating message processing across threads
        self.message_queue = asyncio.Queue(maxsize=self.max_workers)
        
        # For tracking active message processing tasks
        self.active_tasks = set()
        
        # Validate host against allowed IPs
        if self.allowed_ips:
            logger.info(f"Network restrictions enabled")
            # Only show allowed IPs at debug level
            logger.debug(f"Allowed IPs: {self.allowed_ips}")
            logger.debug(f"Always allowed domains: {self.always_allowed_domains}")
            self._validate_host(self.mqtt_broker)
        
        # Initialize client
        self.client = None
        self.connected = False
        self.loop = None
        self.mqtt_client_thread = None
        
    def _validate_host(self, host):
        """Validate if a host is allowed based on the IP whitelist."""
        if not self.allowed_ips:
            return True
            
        # Properly check if host is insyt.co or a subdomain of insyt.co
        if host == "insyt.co" or host.endswith(".insyt.co"):
            logger.debug(f"Host {host} is allowed as an insyt.co domain")
            return True
            
        # Also check against explicitly allowed domains
        for domain in self.always_allowed_domains:
            if host == domain or host.endswith(f".{domain}"):
                logger.debug(f"Host {host} is allowed as part of domain {domain}")
                return True
            
        # Check if host is in allowed IPs
        if any(host.startswith(ip.split(':')[0]) for ip in self.allowed_ips):
            return True
            
        # Resolve hostname to IP and check
        try:
            ip = socket.gethostbyname(host)
            if any(ip == allowed_ip.split(':')[0] for allowed_ip in self.allowed_ips):
                return True
        except socket.gaierror:
            pass
            
        raise NetworkRestrictionError(f"Host {host} is not in the allowed IP list")
    
    # Client callback for when the client receives a CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when connection is established to signaling server."""
        if rc == 0:
            logger.info(f"Successfully connected to signaling server")
            # Use QoS level 2 for subscribing to ensure exactly-once delivery
            result, mid = client.subscribe(self.subscribe_topic, qos=2)
            subscription_status = "Success" if result == 0 else f"Failed with code {result}"
            logger.info(f"Subscription status: {subscription_status}")
            logger.info(f"Subscribed to topic: {self.subscribe_topic} with QoS=2")
            # More detailed logging at debug level
            logger.debug(f"Subscription details - Topic: {self.subscribe_topic}, QoS: 2, Result: {result}, Message ID: {mid}")
            self.connected = True
        else:
            connection_results = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier",
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorised"
            }
            error_message = connection_results.get(rc, f"Unknown error code: {rc}")
            logger.error(f"Failed to connect to signaling server: {error_message}")
            self.connected = False
            
            # If authentication error, signal main thread to get new credentials
            if rc == 4 or rc == 5:
                logger.error("Authentication error. Credentials may have expired.")
                if self.loop:
                    asyncio.run_coroutine_threadsafe(self._signal_auth_error(), self.loop)
    
    # Client callback for when a message is received from the server
    def on_message(self, client, userdata, msg):
        """Callback when a message is received."""
        # Update message tracking
        self.message_received_count += 1
        self.message_received_topics.add(msg.topic)
        self.last_message_time = time.time()
        
        # Print raw message for debugging
        print("\n" + "="*80)
        print(f"RECEIVED MESSAGE ON TOPIC: {msg.topic}")
        print(f"QoS: {msg.qos}, Retain: {msg.retain}")
        print("RAW PAYLOAD START")
        try:
            # Try to decode and pretty print if it's valid JSON
            payload_str = msg.payload.decode('utf-8')
            try:
                # Try to parse and pretty print JSON
                json_payload = json.loads(payload_str)
                # Mask pythonCode if present
                if isinstance(json_payload, dict) and 'pythonCode' in json_payload:
                    json_payload['pythonCode'] = '*** CODE CONTENT MASKED ***'
                print(json.dumps(json_payload, indent=2))
            except json.JSONDecodeError:
                # Just print raw string if not valid JSON
                print(payload_str)
        except UnicodeDecodeError:
            # If it's not valid UTF-8, print hex representation
            print("Binary data (hex):", ' '.join(f'{b:02x}' for b in msg.payload))
        print("RAW PAYLOAD END")
        print("="*80 + "\n")

        logger.info(f"Received message on topic: {msg.topic}")
        logger.info(f"Message QoS: {msg.qos}, Retain: {msg.retain}")
        # Log message size instead of content for security
        logger.info(f"Message size: {len(msg.payload)} bytes")
        
        # Check if this is a subscription test message
        try:
            payload = json.loads(msg.payload)
            if isinstance(payload, dict) and payload.get("type") == "subscription_test":
                logger.info("Received subscription test message")
                self.test_message_received = True
                return  # Skip further processing for test messages
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass  # Not a JSON message or not our test message
            
        logger.debug(f"Message received on channel: {msg.topic}")
        if self.loop:
            # Convert the message to the format expected by process_message
            message = MQTTMessageWrapper(msg)
            # Schedule the message processing in the asyncio event loop
            asyncio.run_coroutine_threadsafe(self.message_queue.put(message), self.loop)
    
    # Client callback for when the client disconnects from the server
    def on_disconnect(self, client, userdata, rc, properties=None):
        """Callback when disconnected from signaling server."""
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnection from signaling server, rc: {rc}")
            # Try to reconnect
            if self.loop:
                asyncio.run_coroutine_threadsafe(self._handle_reconnection(), self.loop)
        else:
            logger.info("Successfully disconnected from signaling server")
    
    async def _signal_auth_error(self):
        """Signal that an authentication error occurred."""
        logger.error("Authentication error. Signaling main thread to get new credentials.")
        # Raise exception to be caught in start() method
        raise Exception("Authentication error. Credentials may have expired.")
    
    async def _handle_reconnection(self):
        """Handle reconnection logic after unexpected disconnection."""
        # This will be caught in start() method and trigger reconnection
        raise Exception("Unexpected disconnection. Triggering reconnection.")
    
    def _mqtt_client_setup(self):
        """Set up the client with all callbacks and configuration."""
        # Create a new client instance with a unique ID that won't collide
        unique_id = str(uuid.uuid4())[:8]
        hostname = platform.node()
        client_id = f"insyt-secure-{self.pod_name}-{hostname}-{os.getpid()}-{unique_id}"
        self.client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
        
        # Set username and password
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # Set up SSL if enabled
        if self.ssl_enabled:
            logger.info("SSL enabled for connection")
            self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
            self.client.tls_insecure_set(False)
        
        # Double-check host against allowed IPs before connecting
        if self.allowed_ips:
            self._validate_host(self.mqtt_broker)
        
        return self.client
    
    def _mqtt_client_connect(self):
        """Connect the client to the signaling server and start the network loop."""
        try:
            logger.info(f"Connecting to signaling server...")
            # Log detailed connection info only at debug level
            logger.debug(f"Server: {self.mqtt_broker}:{self.mqtt_port}, Username: {self.mqtt_username}")
            self.client.connect(self.mqtt_broker, self.mqtt_port, keepalive=60)
            
            # Start the network loop to process callbacks
            self.client.loop_start()
            
            # Wait for connection to be established or failed
            timeout = 10  # seconds
            start_time = time.time()
            while not self.connected and time.time() - start_time < timeout:
                time.sleep(0.1)
            
            if not self.connected:
                logger.error(f"Failed to connect to signaling server within {timeout} seconds")
                self.client.loop_stop()
                raise Exception("Failed to connect to signaling server")
            
        except Exception as e:
            logger.error(f"Error connecting to signaling server: {str(e)}")
            if self.client:
                self.client.loop_stop()
            raise
    
    async def _process_messages(self):
        """Process messages from the queue."""
        while True:
            # Wait for a message from the queue
            message = await self.message_queue.get()
            
            # Process the message in a separate task
            task = asyncio.create_task(self.process_message(message))
            self.active_tasks.add(task)
            task.add_done_callback(self.active_tasks.discard)
            
            # Log if we're at capacity
            if len(self.active_tasks) >= self.max_workers:
                logger.info(f"Processing at capacity with {len(self.active_tasks)} concurrent executions")
            
            # Let the queue know we're done with this item
            self.message_queue.task_done()
    
    async def start(self):
        """Start the executor and connect to signaling server."""
        retry_count = 0
        
        # Store the event loop for use in callbacks
        self.loop = asyncio.get_running_loop()
        
        # Log expected message format
        self._log_message_format()
        
        while True:
            try:
                # Set up client
                self._mqtt_client_setup()
                
                # Connect to signaling server
                self._mqtt_client_connect()
                
                # Reset retry count on successful connection
                if retry_count > 0:
                    logger.info(f"Reconnection successful after {retry_count} attempts")
                    retry_count = 0
                
                # Start message processing
                message_processor = asyncio.create_task(self._process_messages())
                
                # Start diagnostic logger task
                diagnostic_task = asyncio.create_task(self._log_topic_diagnostics())
                
                # Keep the event loop running
                try:
                    while self.connected:
                        await asyncio.sleep(1)
                    
                    # If we get here, it means we disconnected
                    logger.warning("Disconnected from signaling server")
                    raise Exception("Disconnected from signaling server")
                    
                except asyncio.CancelledError:
                    # Cancel message processor if we're shutting down
                    message_processor.cancel()
                    diagnostic_task.cancel()
                    raise
                    
            except NetworkRestrictionError as e:
                logger.error(f"Network restriction error: {str(e)}")
                sys.exit(1)  # Exit immediately for security reasons
                
            except Exception as e:
                retry_count += 1
                logger.error(f"Connection error (attempt {retry_count}): {str(e)}")
                
                # Clean up resources
                if self.client:
                    self.client.loop_stop()
                    self.client = None
                
                # Check for authentication errors
                error_str = str(e).lower()
                if "auth" in error_str or "unauthorized" in error_str or "credentials" in error_str:
                    logger.error("Authentication error. Credentials may have expired. Requesting new credentials.")
                    return
                
                # Implement backoff for connection retries
                backoff_time = min(30, 2 ** min(retry_count, 4) + (0.1 * retry_count))  # Cap at 30 seconds
                logger.warning(f"Connection failed. Retrying in {backoff_time:.1f} seconds...")
                await asyncio.sleep(backoff_time)
        
    def _log_message_format(self):
        """Log details about expected message format and subscription."""
        logger.info("=== Subscription and Message Format Information ===")
        logger.info(f"This service is configured to subscribe to: {self.subscribe_topic}")
        if self.publish_topic:
            logger.info(f"Default publish topic for responses: {self.publish_topic}")
        else:
            logger.info("No default publish topic configured - will use response_topic from messages")
        logger.info("Expected incoming message format:")
        logger.info("""
        {
            "pythonCode": "...", // Required: Python code to execute
            "requestId": "...",  // Required: Unique identifier for this request
            "sharedTopic": "...", // Optional: Topic to publish results to
            "executionTime": "30" // Optional: Maximum execution time in seconds
        }
        """)
        logger.info("Response message format:")
        logger.info("""
        {
            "codeOutput": "...", // Output from the code execution
            "requestId": "...",  // Same requestId that was received
            "executionTime": "...", // Actual execution time in seconds
            "status": "success"|"failure" // Execution status
        }
        """)
        logger.info("===================================================")
    
    async def process_message(self, message):
        """Process an incoming execution request."""
        request_id = None  # Initialize for error logging
        try:
            # Parse the message payload
            payload = json.loads(message.payload)
            
            # Log the message structure without sensitive content
            payload_structure = {k: '***' if k == 'pythonCode' else ('present' if v else 'missing') 
                                for k, v in payload.items()}
            logger.info(f"Message structure: {payload_structure}")
            
            # Use debug level for full message content
            logger.debug(f"Received message details: {payload}")
            
            # Extract fields from payload with the correct keys
            python_code = payload.get("pythonCode")
            if not python_code:
                logger.warning("Received message without code to execute")
                return
            
            # Extract requestId
            request_id = payload.get("requestId")
            if not request_id:
                logger.warning("Received message without requestId")
                return
                
            # Get the response topic from the message, or fall back to the default
            response_topic = payload.get("sharedTopic")
            if not response_topic:
                logger.warning(f"Message missing response channel, using default")
                response_topic = self.publish_topic
            
            # Extract execution timeout from payload or use default
            # Note: according to spec, it's "executionTime" not "executionTimeout"
            execution_timeout = payload.get("executionTime")
            if execution_timeout:
                try:
                    execution_timeout = int(execution_timeout)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid execution time value, using default: {self.execution_timeout}")
                    execution_timeout = self.execution_timeout
            else:
                execution_timeout = self.execution_timeout
            
            # Calculate code length for logging (useful for debugging but avoid logging full code for security)
            code_length = len(python_code)
            
            # Log request with masked ID
            masked_id = request_id[-4:] if len(request_id) > 4 else "****"
            logger.info(f"Processing execution request (ID: ****{masked_id}, length: {code_length} chars)")
            logger.debug(f"Using timeout: {execution_timeout}s for request ID: {request_id}")
            
            # Execute the code with the specified timeout
            start_time = time.time()
            
            future = self.executor.submit(
                self.extract_and_run_python_code_with_timeout, 
                python_code, 
                execution_timeout
            )
            
            # Get the result
            result, parsed_result = await asyncio.get_event_loop().run_in_executor(
                None, future.result
            )
            
            # Log execution time
            actual_execution_time = time.time() - start_time
            logger.info(f"Execution completed in {actual_execution_time:.2f}s")
            
            # Determine if execution was successful (no error message in result)
            has_error = "Error" in result or "Execution timed out" in result
            status = "failure" if has_error else "success"
            
            # Format the response according to the specified structure
            response = {
                "codeOutput": result,
                "requestId": request_id,
                "executionTime": str(actual_execution_time),
                "status": status
            }
            
            # Publish response
            logger.info(f"Publishing result with status: {status}")
            # Log detailed info only at debug level
            logger.debug(f"Publishing to channel: {response_topic}")
            response_json = json.dumps(response)
            
            # Use client to publish response
            if self.client and self.connected:
                # Log the publish topic more prominently
                logger.info("="*50)
                logger.info(f"PUBLISHING RESULT TO: {response_topic}")
                logger.info("="*50)
                
                # Track published topics for diagnostics
                self.message_published_count += 1
                self.message_published_topics.add(response_topic)
                
                # Use QoS level 2 for publishing to ensure exactly-once delivery
                self.client.publish(response_topic, response_json, qos=2)
                logger.info(f"Successfully published result with QoS=2")
            else:
                logger.error(f"Cannot publish result: Not connected to signaling server")
                
        except Exception as e:
            if request_id:
                masked_id = request_id[-4:] if len(request_id) > 4 else "****"
                logger.error(f"Error processing request ID ****{masked_id}: {str(e)}")
            else:
                logger.error(f"Error processing request: {str(e)}")
            
            # Attempt to publish error response if we have a requestId and client
            if request_id and self.client and self.connected and 'response_topic' in locals():
                try:
                    error_response = {
                        "codeOutput": f"Error: {str(e)}",
                        "requestId": request_id,
                        "executionTime": "0",
                        "status": "failure"
                    }
                    # Log the publish topic more prominently
                    logger.info("="*50)
                    logger.info(f"PUBLISHING ERROR RESPONSE TO: {response_topic}")
                    logger.info("="*50)
                    
                    # Track published topics for diagnostics
                    self.message_published_count += 1
                    self.message_published_topics.add(response_topic)
                    
                    # Use QoS level 2 for publishing error responses
                    self.client.publish(response_topic, json.dumps(error_response), qos=2)
                    logger.info(f"Published error response with QoS=2")
                except Exception as publish_error:
                    logger.error(f"Failed to publish error response: {str(publish_error)}")

    def extract_and_run_python_code(self, code):
        """Execute code and capture its output."""
        try:
            logger.info("Starting code execution")
            # Create a dictionary to store globals
            globals_dict = {}

            # Redirect stdout to a StringIO object
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            # Execute the code, passing the globals dictionary
            exec(code, globals_dict)

            # Get the printed output
            output = sys.stdout.getvalue()

            # Restore the original stdout
            sys.stdout = old_stdout

            # The result should be in the output
            result = output.strip()
            
            # Only show a preview of the output
            result_preview = (result[:50] + "...") if len(result) > 50 else result
            logger.info(f"Code execution completed successfully")
            logger.debug(f"Output preview: {result_preview}")

            try:
                # Try to parse the result as JSON
                parsed_result = json.loads(result)
                logger.debug("Result was valid JSON")
            except json.JSONDecodeError:
                logger.debug("Result was not valid JSON")
                parsed_result = None

            return result, parsed_result

        except Exception as e:
            logger.error(f"Error executing code: {str(e)}")
            return f"Error executing code: {str(e)}", None

    def extract_and_run_python_code_with_timeout(self, code_block, timeout):
        """Execute code with a timeout."""
        try:
            logger.info(f"Running code with {timeout}s timeout")
            # Set up the timeout mechanism
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.extract_and_run_python_code, code_block)
                try:
                    result, parsed_result = future.result(timeout=timeout)
                    return result, parsed_result
                except concurrent.futures.TimeoutError:
                    logger.warning(f"Execution timed out after {timeout}s")
                    return f"Execution timed out after {timeout} seconds", None
        except Exception as e:
            logger.error(f"Error during execution with timeout: {str(e)}")
            return f"Error: {str(e)}", None

    async def _log_topic_diagnostics(self):
        """Periodically log diagnostic information about topics and message activity."""
        while True:
            try:
                await asyncio.sleep(30)  # Log diagnostics every 30 seconds
                
                # Print topic summary
                print("\n" + "*"*80)
                print("MQTT TOPIC AND MESSAGE ACTIVITY SUMMARY")
                print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Connected: {self.connected}")
                print("-"*40)
                print(f"Subscribed topic: {self.subscribe_topic}")
                print(f"Default publish topic: {self.publish_topic if self.publish_topic else 'None (using message-specific topics)'}")
                print("-"*40)
                print(f"Messages received: {self.message_received_count}")
                if self.message_received_topics:
                    print("Received from topics:")
                    for topic in sorted(self.message_received_topics):
                        print(f"  - {topic}")
                else:
                    print("No messages received yet")
                print("-"*40)
                print(f"Topics published to:")
                if self.message_published_topics:
                    for topic in sorted(self.message_published_topics):
                        print(f"  - {topic}")
                else:
                    print("No messages published yet")
                print("*"*80 + "\n")
                
            except Exception as e:
                logger.error(f"Error in diagnostic logging: {str(e)}")
                await asyncio.sleep(10)  # If there's an error, wait a bit before retrying

    async def _run_subscription_test(self):
        """Send a test message to verify subscription is working."""
        await asyncio.sleep(2)  # Give a small delay to ensure subscription is fully processed
        
        try:
            # Create a test message with a special marker
            test_message = {
                "type": "subscription_test",
                "timestamp": time.time(),
                "client_id": self.client._client_id.decode('utf-8') if hasattr(self.client, '_client_id') else "unknown"
            }
            
            test_message_json = json.dumps(test_message)
            test_topic = self.subscribe_topic
            
            # Log the publish topic more prominently
            logger.info("="*50)
            logger.info(f"PUBLISHING TEST MESSAGE TO: {test_topic}")
            logger.info("="*50)
            
            # Publish the message
            result = self.client.publish(test_topic, test_message_json, qos=2)
            
            # Track published topics for diagnostics
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.message_published_count += 1
                self.message_published_topics.add(test_topic)
                logger.info(f"Test message published successfully with message ID: {result.mid}")
            else:
                logger.warning(f"Failed to publish test message, error code: {result.rc}")
                
            # Set a timer to check if we received our own message
            self.test_message_received = False
            await asyncio.sleep(5)  # Wait 5 seconds for message to be received
            
            if not self.test_message_received:
                logger.warning("❌ SUBSCRIPTION TEST FAILED: Did not receive test message")
                logger.warning("This indicates the subscription is not working correctly")
                logger.warning("Check EMQX broker configuration and network connectivity")
            else:
                logger.info("✅ SUBSCRIPTION TEST PASSED: Successfully received test message")
                logger.info("Subscription to topic is working correctly")
                
        except Exception as e:
            logger.error(f"Error during subscription test: {str(e)}")

# Wrapper class to maintain API compatibility with messages
class MQTTMessageWrapper:
    def __init__(self, mqtt_message):
        self.topic = mqtt_message.topic
        self.payload = mqtt_message.payload
        self.qos = mqtt_message.qos
        self.retain = mqtt_message.retain
        self.mid = mqtt_message.mid

async def main():
    executor = CodeExecutor()
    await executor.start()

if __name__ == "__main__":
    asyncio.run(main())