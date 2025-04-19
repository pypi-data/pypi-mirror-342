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
        
        # Subscription tracking
        self.last_subscription_time = 0
        self.last_subscription_mid = None
        self.subscription_confirmed = False
        self.client_id = None  # Will be set during client setup
        
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
            
            # Set connection status before subscribing
            self.connected = True
            
            # Use QoS level 2 for subscribing to ensure exactly-once delivery
            try:
                result, mid = client.subscribe(self.subscribe_topic, qos=2)
                subscription_status = "Success" if result == 0 else f"Failed with code {result}"
                logger.info(f"Subscription status: {subscription_status}")
                logger.info(f"Subscribed to topic: {self.subscribe_topic} with QoS=2")
                # More detailed logging at debug level
                logger.debug(f"Subscription details - Topic: {self.subscribe_topic}, QoS: 2, Result: {result}, Message ID: {mid}")
                
                # Track subscription attempt
                self.last_subscription_time = time.time()
                self.last_subscription_mid = mid
                self.subscription_confirmed = False  # Will be set to True in on_subscribe
                
            except Exception as e:
                logger.error(f"Error subscribing to topic: {str(e)}")
                import traceback
                logger.error(f"Exception traceback: {traceback.format_exc()}")
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
            try:
                # Convert the message to the format expected by process_message
                message = MQTTMessageWrapper(msg)
                # Schedule the message processing in the asyncio event loop
                asyncio.run_coroutine_threadsafe(self.message_queue.put(message), self.loop)
            except Exception as e:
                logger.error(f"Error queueing message for processing: {str(e)}")
                import traceback
                logger.error(f"Exception traceback: {traceback.format_exc()}")

    # Add callback for successful subscriptions
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """Callback when subscription is confirmed by the broker."""
        logger.info(f"Broker confirmed subscription with message ID: {mid}")
        logger.info(f"Granted QoS: {granted_qos}")
        
        # Mark subscription as confirmed
        self.subscription_confirmed = True
        
        # Schedule a self-test after subscription is confirmed
        if self.loop:
            asyncio.run_coroutine_threadsafe(self._run_subscription_test(), self.loop)
    
    # Add callback for publish confirmations
    def on_publish(self, client, userdata, mid):
        """Callback when publish is confirmed by the broker."""
        logger.debug(f"Broker confirmed message publication with message ID: {mid}")
        # Could track specific message IDs here if needed
    
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
        
        # Track the client ID for diagnostics
        self.client_id = client_id
        
        try:
            logger.info(f"Setting up MQTT client with ID: {client_id}")
            
            # Check if MQTTv5 is available in this version of paho-mqtt
            mqtt_version = mqtt.MQTTv311  # Default to 3.1.1
            try:
                if hasattr(mqtt, 'MQTTv5'):
                    mqtt_version = mqtt.MQTTv5
                    logger.info("Using MQTT 5.0 protocol")
                else:
                    logger.info("MQTT 5.0 not available, using MQTT 3.1.1")
            except AttributeError:
                logger.info("MQTT 5.0 not available, using MQTT 3.1.1")
            
            # Create client with appropriate protocol version
            if mqtt_version == mqtt.MQTTv5:
                self.client = mqtt.Client(client_id=client_id, protocol=mqtt_version)
            else:
                # For MQTT 3.1.1, we can use clean_session
                self.client = mqtt.Client(client_id=client_id, clean_session=True)
            
            # Store MQTT version for later use
            self.mqtt_version = mqtt_version
            
            # Set up username and password
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
            
            # Set up callbacks
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.on_subscribe = self.on_subscribe  # Add subscription callback
            self.client.on_publish = self.on_publish      # Add publish callback
            
            # Set up SSL if enabled
            if self.ssl_enabled:
                logger.info("SSL enabled for connection")
                self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
                self.client.tls_insecure_set(False)
            
            # Set the client to automatically reconnect with exponential backoff
            self.client.reconnect_delay_set(min_delay=1, max_delay=30)
            
            # Set up will message for clean disconnect notification
            will_message = {
                "status": "offline",
                "client_id": client_id,
                "timestamp": time.time(),
                "reason": "unexpected_disconnect"
            }
            will_topic = f"status/{client_id}"
            self.client.will_set(will_topic, json.dumps(will_message), qos=2, retain=True)
            
            # Double-check host against allowed IPs before connecting
            if self.allowed_ips:
                self._validate_host(self.mqtt_broker)
            
            return self.client
        except Exception as e:
            logger.error(f"Error setting up MQTT client: {str(e)}")
            import traceback
            logger.error(f"Exception traceback: {traceback.format_exc()}")
            raise

    def _mqtt_client_connect(self):
        """Connect the client to the signaling server and start the network loop."""
        try:
            logger.info(f"Connecting to signaling server...")
            # Log detailed connection info only at debug level
            logger.debug(f"Server: {self.mqtt_broker}:{self.mqtt_port}, Username: {self.mqtt_username}")
            
            # Connect with appropriate parameters based on MQTT version
            if hasattr(self, 'mqtt_version') and self.mqtt_version == mqtt.MQTTv5:
                # For MQTT 5.0
                try:
                    # Try to create Properties object if available
                    connect_properties = None
                    # The constant 1 is for CONNECT packet type
                    # This is more resilient than relying on mqtt.PacketTypes.CONNECT
                    if hasattr(mqtt, 'Properties'):
                        try:
                            # First try with PacketTypes if available
                            if hasattr(mqtt, 'PacketTypes'):
                                connect_properties = mqtt.Properties(mqtt.PacketTypes.CONNECT)
                            else:
                                # Fall back to using the raw value (1 is CONNECT)
                                connect_properties = mqtt.Properties(1)
                        except TypeError:
                            # Some versions might expect different parameters
                            logger.warning("Could not create MQTT Properties, connecting without properties")
                    
                    self.client.connect(
                        self.mqtt_broker, 
                        self.mqtt_port, 
                        keepalive=60, 
                        clean_start=True,
                        properties=connect_properties
                    )
                except (TypeError, AttributeError) as e:
                    # If clean_start or properties aren't supported, fall back to basic connect
                    logger.warning(f"MQTT 5.0 connect failed, trying basic connect: {str(e)}")
                    self.client.connect(self.mqtt_broker, self.mqtt_port, keepalive=60)
            else:
                # For MQTT 3.1.1
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
            
            # Publish online status
            try:
                status_message = {
                    "status": "online",
                    "client_id": self.client_id,
                    "timestamp": time.time(),
                    "pod_name": self.pod_name,
                    "subscribe_topic": self.subscribe_topic
                }
                status_topic = f"status/{self.client_id}"
                self.client.publish(status_topic, json.dumps(status_message), qos=1, retain=True)
                logger.info(f"Published online status to {status_topic}")
            except Exception as e:
                logger.warning(f"Failed to publish online status: {str(e)}")
                # Non-critical, so continue even if this fails
                
        except Exception as e:
            logger.error(f"Error connecting to signaling server: {str(e)}")
            if self.client:
                self.client.loop_stop()
            raise
    
    async def _process_messages(self):
        """Process messages from the queue."""
        while True:
            try:
                # Wait for a message from the queue
                message = await self.message_queue.get()
                
                # Process the message in a separate task
                task = asyncio.create_task(self.process_message(message))
                self.active_tasks.add(task)
                task.add_done_callback(self._task_done_callback)
                
                # Log if we're at capacity
                if len(self.active_tasks) >= self.max_workers:
                    logger.info(f"Processing at capacity with {len(self.active_tasks)} concurrent executions")
                
                # Let the queue know we're done with this item
                self.message_queue.task_done()
            except asyncio.CancelledError:
                logger.info("Message processing loop cancelled")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in message processing loop: {str(e)}")
                import traceback
                logger.error(f"Exception traceback: {traceback.format_exc()}")
                # Sleep briefly to avoid tight error loops
                await asyncio.sleep(1)
    
    def _task_done_callback(self, task):
        """Callback when a task is done - checks for exceptions and logs them."""
        self.active_tasks.discard(task)
        
        # Check if the task raised an exception
        if not task.cancelled():
            exception = task.exception()
            if exception:
                logger.error(f"Task raised an unhandled exception: {str(exception)}")
                import traceback
                logger.error(f"Exception traceback: {traceback.format_tb(exception.__traceback__)}")
    
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
                
                # Start heartbeat task
                heartbeat_task = asyncio.create_task(self._send_heartbeat())
                
                # Start subscription monitor task
                subscription_monitor = asyncio.create_task(self._monitor_subscription())
                
                # Keep the event loop running
                try:
                    while self.connected:
                        await asyncio.sleep(1)
                    
                    # If we get here, it means we disconnected
                    logger.warning("Disconnected from signaling server")
                    raise Exception("Disconnected from signaling server")
                    
                except asyncio.CancelledError:
                    # Cancel all tasks if we're shutting down
                    message_processor.cancel()
                    diagnostic_task.cancel()
                    heartbeat_task.cancel()
                    subscription_monitor.cancel()
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
        start_time = time.time()
        response_topic = None  # Initialize for error handling
        status = "failure"  # Default status
        
        try:
            # Parse the message payload
            try:
                payload = json.loads(message.payload)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message payload as JSON: {str(e)}")
                logger.error(f"Raw payload: {message.payload[:100]}..." if len(message.payload) > 100 else message.payload)
                return  # Can't process non-JSON messages
            except Exception as e:
                logger.error(f"Unexpected error parsing message payload: {str(e)}")
                return
            
            # Log the message structure without sensitive content
            try:
                payload_structure = {k: '***' if k == 'pythonCode' else ('present' if v else 'missing') 
                                    for k, v in payload.items()}
                logger.info(f"Message structure: {payload_structure}")
            except Exception as e:
                logger.error(f"Error logging message structure: {str(e)}")
                # Continue processing even if we can't log the structure
            
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
                if self.publish_topic:
                    logger.warning(f"Message missing response channel, using default: {self.publish_topic}")
                    response_topic = self.publish_topic
                else:
                    logger.error("Message missing response channel and no default publish topic configured")
                    return  # Can't respond without a topic
            
            # Extract execution timeout from payload or use default
            # Note: according to spec, it's "executionTime" not "executionTimeout"
            execution_timeout = payload.get("executionTime")
            if execution_timeout:
                try:
                    execution_timeout = int(execution_timeout)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid execution time value '{execution_timeout}', using default: {self.execution_timeout}")
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
            execution_start_time = time.time()
            
            try:
                future = self.executor.submit(
                    self.extract_and_run_python_code_with_timeout, 
                    python_code, 
                    execution_timeout
                )
                
                # Get the result with a timeout that's slightly longer than the execution timeout
                # This prevents the system from hanging if there's an issue with the executor
                extended_timeout = execution_timeout + 10
                result, parsed_result = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None, future.result),
                    timeout=extended_timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Critical: Executor did not complete within extended timeout ({extended_timeout}s)")
                result = f"Execution timed out after {execution_timeout} seconds (critical system timeout)"
                parsed_result = None
            except concurrent.futures.CancelledError:
                logger.error("Execution was cancelled")
                result = "Execution was cancelled by the system"
                parsed_result = None
            except Exception as e:
                logger.error(f"Unexpected error during execution: {str(e)}")
                result = f"Execution failed with unexpected error: {str(e)}"
                parsed_result = None
            
            # Log execution time
            actual_execution_time = time.time() - execution_start_time
            logger.info(f"Execution completed in {actual_execution_time:.2f}s")
            
            # Determine if execution was successful (no error message in result)
            has_error = isinstance(result, str) and ("Error" in result or "timed out" in result or "cancelled" in result)
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
            
            try:
                response_json = json.dumps(response)
            except (TypeError, ValueError) as e:
                logger.error(f"Failed to serialize response to JSON: {str(e)}")
                # Try to create a simpler response that can be serialized
                response = {
                    "codeOutput": f"Error: Failed to serialize original output: {str(e)}",
                    "requestId": request_id,
                    "executionTime": str(actual_execution_time),
                    "status": "failure"
                }
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
                try:
                    result = self.client.publish(response_topic, response_json, qos=2)
                    if result.rc == mqtt.MQTT_ERR_SUCCESS:
                        logger.info(f"Successfully published result with QoS=2 (Message ID: {result.mid})")
                    else:
                        logger.error(f"Failed to publish result: MQTT error code {result.rc}")
                except Exception as e:
                    logger.error(f"Exception during publish: {str(e)}")
            else:
                logger.error(f"Cannot publish result: Not connected to signaling server (connected={self.connected}, client={'initialized' if self.client else 'not initialized'})")
                
        except Exception as e:
            # Get total processing time regardless of errors
            total_time = time.time() - start_time
            
            # Log the exception with full traceback
            import traceback
            logger.error(f"Unhandled exception in process_message: {str(e)}")
            logger.error(f"Exception traceback: {traceback.format_exc()}")
            logger.error(f"Total processing time before error: {total_time:.2f}s")
            
            # Attempt to publish error response if we have a requestId and client
            if request_id and response_topic and self.client and self.connected:
                try:
                    error_response = {
                        "codeOutput": f"Error: {str(e)}",
                        "requestId": request_id,
                        "executionTime": str(total_time),
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
                    result = self.client.publish(response_topic, json.dumps(error_response), qos=2)
                    if result.rc == mqtt.MQTT_ERR_SUCCESS:
                        logger.info(f"Published error response with QoS=2 (Message ID: {result.mid})")
                    else:
                        logger.error(f"Failed to publish error response: MQTT error code {result.rc}")
                except Exception as publish_error:
                    logger.error(f"Failed to publish error response: {str(publish_error)}")
                    logger.error(f"Exception traceback: {traceback.format_exc()}")
            elif request_id:
                logger.error(f"Could not publish error for request ID ****{masked_id if 'masked_id' in locals() else request_id[-4:] if len(request_id) > 4 else '****'}")
                if not response_topic:
                    logger.error("No response topic available")
                if not self.client:
                    logger.error("MQTT client not initialized")
                if not self.connected:
                    logger.error("Not connected to broker")

    def extract_and_run_python_code(self, code):
        """Execute code and capture its output."""
        try:
            logger.info("Starting code execution")
            
            # Log the code to be executed (added as requested)
            logger.info("=== EXECUTING PYTHON CODE ===")
            logger.info(code)
            logger.info("============================")
            
            # Create a dictionary to store globals
            globals_dict = {}

            # Redirect stdout to a StringIO object
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            # Execute the code, passing the globals dictionary
            try:
                exec(code, globals_dict)
                execution_success = True
            except Exception as e:
                logger.error(f"Error during code execution: {str(e)}")
                # Print the error to the redirected stderr
                import traceback
                print(f"Error: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                execution_success = False

            # Get the printed output
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()

            # Restore the original stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Combine stdout and stderr for the result
            if stderr_output:
                result = stderr_output.strip()
                if stdout_output:
                    result = f"{stdout_output.strip()}\n\n{result}"
            else:
                result = stdout_output.strip()

            # Only show a preview of the output
            result_preview = (result[:50] + "...") if len(result) > 50 else result
            if execution_success:
                logger.info(f"Code execution completed successfully")
            else:
                logger.warning(f"Code execution completed with errors")
            logger.debug(f"Output preview: {result_preview}")

            try:
                # Try to parse the result as JSON
                parsed_result = json.loads(result)
                logger.debug("Result was valid JSON")
            except json.JSONDecodeError:
                logger.debug("Result was not valid JSON")
                parsed_result = None
            except Exception as e:
                logger.error(f"Unexpected error parsing result as JSON: {str(e)}")
                parsed_result = None

            return result, parsed_result

        except Exception as e:
            logger.error(f"Critical error executing code: {str(e)}")
            import traceback
            logger.error(f"Exception traceback: {traceback.format_exc()}")
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
                    # Attempt to cancel the future to clean up resources
                    if not future.done():
                        future.cancel()
                        logger.info("Cancelled timed-out execution task")
                    return f"Execution timed out after {timeout} seconds", None
                except Exception as e:
                    logger.error(f"Unexpected error in timeout handler: {str(e)}")
                    import traceback
                    logger.error(f"Exception traceback: {traceback.format_exc()}")
                    return f"Error: {str(e)}", None
        except Exception as e:
            logger.error(f"Critical error setting up execution with timeout: {str(e)}")
            import traceback
            logger.error(f"Exception traceback: {traceback.format_exc()}")
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
                
                # Add connection details
                client_id = self.client._client_id.decode('utf-8') if self.client and hasattr(self.client, '_client_id') else "Not connected"
                print(f"Client ID: {client_id}")
                print(f"Broker: {self.mqtt_broker}:{self.mqtt_port}")
                
                # Add active task info
                active_task_count = len(self.active_tasks) if hasattr(self, 'active_tasks') else 0
                print(f"Active tasks: {active_task_count}/{self.max_workers}")
                
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
                print(f"Messages published: {self.message_published_count}")
                print(f"Topics published to:")
                if self.message_published_topics:
                    for topic in sorted(self.message_published_topics):
                        print(f"  - {topic}")
                else:
                    print("No messages published yet")
                
                # Add memory usage info if possible
                try:
                    import psutil
                    process = psutil.Process()
                    memory_info = process.memory_info()
                    print("-"*40)
                    print(f"Memory usage: {memory_info.rss / (1024 * 1024):.1f} MB")
                    print(f"CPU usage: {process.cpu_percent(interval=None):.1f}%")
                except ImportError:
                    # psutil not available
                    pass
                except Exception as e:
                    print(f"Error getting resource usage: {str(e)}")
                
                print("*"*80 + "\n")
                
            except asyncio.CancelledError:
                logger.info("Diagnostic logger task cancelled")
                raise
            except Exception as e:
                logger.error(f"Error in diagnostic logging: {str(e)}")
                import traceback
                logger.error(f"Exception traceback: {traceback.format_exc()}")
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
            
            # Use a separate topic for testing if possible
            # If broker ACLs restrict self-publishing to subscription topic, this might fail
            test_topic = self.subscribe_topic
            
            # Set a flag to track whether we received our own test message
            self.test_message_received = False
            
            # Log the publish topic more prominently
            logger.info("="*50)
            logger.info(f"ATTEMPTING TO PUBLISH TEST MESSAGE TO: {test_topic}")
            logger.info("(Note: If broker ACL rules prohibit self-publishing, this test may fail)")
            logger.info("="*50)
            
            try:
                # Publish the message
                result = self.client.publish(test_topic, test_message_json, qos=2)
                
                # Track published topics for diagnostics only if successful
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    self.message_published_count += 1
                    self.message_published_topics.add(test_topic)
                    logger.info(f"Test message published successfully with message ID: {result.mid}")
                    
                    # Wait for the message to be received back
                    await asyncio.sleep(5)  # Wait 5 seconds for message to be received
                    
                    if not self.test_message_received:
                        logger.warning("❌ SUBSCRIPTION TEST INCONCLUSIVE: Did not receive test message")
                        logger.warning("This might be due to broker ACL rules preventing self-publishing")
                        logger.warning("The subscription may still be working correctly for messages from other clients")
                    else:
                        logger.info("✅ SUBSCRIPTION TEST PASSED: Successfully received test message")
                        logger.info("Subscription to topic is working correctly")
                else:
                    logger.warning(f"Failed to publish test message, error code: {result.rc}")
                    logger.warning("This might be due to broker ACL rules preventing publishing to this topic")
                    logger.warning("The subscription may still be working correctly for messages from other clients")
            except Exception as e:
                # Don't fail the whole process if the test doesn't work
                logger.warning(f"Subscription test publishing failed: {str(e)}")
                logger.warning("This might be due to broker ACL rules or other restrictions")
                logger.warning("The subscription may still be working correctly for messages from other clients")
                
        except Exception as e:
            logger.error(f"Error during subscription test: {str(e)}")
            # Don't propagate the exception as this is just a diagnostic test

    async def _send_heartbeat(self):
        """Send periodic heartbeat messages to confirm the connection is active."""
        while True:
            try:
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
                
                if self.connected and self.client:
                    try:
                        # Create heartbeat message
                        heartbeat_message = {
                            "type": "heartbeat",
                            "client_id": self.client_id,
                            "timestamp": time.time(),
                            "received_count": self.message_received_count,
                            "published_count": self.message_published_count
                        }
                        
                        # Publish heartbeat
                        heartbeat_topic = f"heartbeat/{self.client_id}"
                        result = self.client.publish(heartbeat_topic, json.dumps(heartbeat_message), qos=0)
                        
                        if result.rc == mqtt.MQTT_ERR_SUCCESS:
                            logger.debug(f"Sent heartbeat to {heartbeat_topic}")
                        else:
                            logger.warning(f"Failed to send heartbeat: {result.rc}")
                            
                    except Exception as e:
                        logger.error(f"Error sending heartbeat: {str(e)}")
            except asyncio.CancelledError:
                logger.info("Heartbeat task cancelled")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in heartbeat task: {str(e)}")
                await asyncio.sleep(10)  # Wait before retrying
    
    async def _monitor_subscription(self):
        """Monitor subscription status and re-subscribe if needed."""
        while True:
            try:
                await asyncio.sleep(15)  # Check every 15 seconds
                
                if self.connected and self.client:
                    # Check if we've received confirmation of our subscription
                    if not self.subscription_confirmed and self.last_subscription_time > 0:
                        time_since_subscribe = time.time() - self.last_subscription_time
                        
                        # If it's been more than 10 seconds since we tried to subscribe without confirmation
                        if time_since_subscribe > 10:
                            logger.warning(f"Subscription not confirmed after {time_since_subscribe:.1f} seconds, re-subscribing")
                            
                            try:
                                # Try to subscribe again
                                result, mid = self.client.subscribe(self.subscribe_topic, qos=2)
                                logger.info(f"Re-subscription attempt result: {result}")
                                
                                # Update tracking
                                self.last_subscription_time = time.time()
                                self.last_subscription_mid = mid
                            except Exception as e:
                                logger.error(f"Error re-subscribing: {str(e)}")
                    
                    # Check if we've received any messages on our subscribed topic recently
                    if self.message_received_count > 0:
                        time_since_message = time.time() - self.last_message_time
                        
                        # If it's been more than 5 minutes since last message, log a diagnostic message
                        # This isn't necessarily an error, just useful information
                        if time_since_message > 300:  # 5 minutes
                            logger.info(f"No messages received in {time_since_message:.1f} seconds on {self.subscribe_topic}")
            except asyncio.CancelledError:
                logger.info("Subscription monitor task cancelled")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in subscription monitor: {str(e)}")
                await asyncio.sleep(10)  # Wait before retrying

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