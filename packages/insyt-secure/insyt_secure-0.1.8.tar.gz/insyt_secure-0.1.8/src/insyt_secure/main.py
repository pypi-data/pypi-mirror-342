import os
import sys
import time
import argparse
import asyncio
import socket
import threading
import logging
import logging.config
import signal
import json
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from insyt_secure.executor.code_executor import CodeExecutor, NetworkRestrictionError
from insyt_secure.utils.logging_config import configure_logging, UserFriendlyFormatter, LoggingFormat
from insyt_secure.utils import get_log_level_from_env

# Create a logger for this module
logger = logging.getLogger(__name__)

# Constants
MAX_RETRIES = 5  # Maximum number of retry attempts for credential acquisition
RETRY_DELAY = 5  # Delay in seconds between retry attempts

def get_credentials(project_id, api_url, api_key=None):
    """
    Get service credentials from the API.
    
    Args:
        project_id: The project ID to get credentials for
        api_url: The base URL of the credentials API
        api_key: Optional API key for authentication
        
    Returns:
        dict: Dictionary containing credentials and connection details
        
    Raises:
        Exception: If unable to get valid credentials after MAX_RETRIES
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempting to acquire credentials (attempt {attempt}/{MAX_RETRIES})...")
            
            # Construct the full API URL
            endpoint = f"api/v1/service/broker/proxy-credentials?projectId={project_id}"
            full_url = urljoin(api_url, endpoint)
            
            logger.info(f"Requesting service credentials")
            logger.debug(f"API URL: {full_url}")
            
            # Set up headers if API key is provided
            headers = {}
            if api_key:
                headers["X-API-Key"] = api_key
                
            # Make the API request
            response = requests.post(full_url, headers=headers, json={}, timeout=10)
            
            # Check if the request was successful
            if response.status_code == 200:
                logger.info("Successfully received API response")
                api_response = response.json()
                
                # Map the response to the expected format
                credentials = {
                    'username': api_response.get('username'),
                    'password': api_response.get('password'),
                    'broker': 'broker.insyt.co',  # Hard-coded broker address
                    'port': api_response.get('sslPort', 8883),
                    'topic': api_response.get('topic'),
                    'ssl_enabled': api_response.get('sslEnabled', True)
                }
                
                # Validate the required credentials are present
                required_fields = ['username', 'password', 'broker', 'port', 'topic']
                missing_fields = [field for field in required_fields if field not in credentials]
                
                if missing_fields:
                    logger.error(f"Missing required credentials: {', '.join(missing_fields)}")
                    raise ValueError(f"Missing required credentials: {', '.join(missing_fields)}")
                
                logger.info("Credentials received successfully")
                return credentials
            else:
                logger.error(f"Failed to get credentials. Status code: {response.status_code}")
                logger.debug(f"Response: {response.text}")
                
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        
        # If we've reached the maximum number of retries, raise an exception
        if attempt >= MAX_RETRIES:
            raise Exception(f"Failed to acquire valid credentials after {MAX_RETRIES} attempts")
        
        # Wait before retrying
        logger.info(f"Retrying in {RETRY_DELAY} seconds...")
        time.sleep(RETRY_DELAY)

def setup_argparse():
    """Set up and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Insyt Secure Execution Service",
        epilog="The service securely executes code received via the signaling server."
    )
    
    # Basic configuration
    parser.add_argument(
        "--project-id", 
        default=os.getenv("INSYT_PROJECT_ID"),
        help="Project ID for credential acquisition (default: from INSYT_PROJECT_ID env var)"
    )
    parser.add_argument(
        "--api-key", 
        default=os.getenv("INSYT_API_KEY"),
        help="API key for authenticating with the credentials API (default: from INSYT_API_KEY env var)"
    )
    parser.add_argument(
        "--api-url", 
        default=os.getenv("INSYT_API_URL", "https://api.account.insyt.co/"),
        help="API URL for credential acquisition (default: from INSYT_API_URL env var or https://api.account.insyt.co/)"
    )
    
    # Execution configuration
    parser.add_argument(
        "--max-workers",
        type=int,
        default=int(os.getenv("INSYT_MAX_WORKERS", "5")),
        help="Maximum number of concurrent execution workers (default: 5)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("INSYT_EXECUTION_TIMEOUT", "30")),
        help="Execution timeout in seconds (default: 30)"
    )
    
    # Network security
    parser.add_argument(
        "--allowed-hosts",
        type=str,
        default=os.getenv("INSYT_ALLOWED_HOSTS"),
        help="Comma-separated list of allowed hosts (default: from INSYT_ALLOWED_HOSTS env var)"
    )
    parser.add_argument(
        "--always-allowed-domains",
        type=str,
        default=os.getenv("INSYT_ALWAYS_ALLOWED_DOMAINS", "insyt.co,localhost"),
        help="Comma-separated list of always-allowed domains (default: insyt.co,localhost)"
    )
    
    # Logging configuration
    parser.add_argument(
        "--log-level",
        type=str,
        default=os.getenv("INSYT_LOG_LEVEL", "info"),
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level (default: info)"
    )
    parser.add_argument(
        "--log-format",
        type=str,
        default=os.getenv("INSYT_LOG_FORMAT", "user_friendly"),
        choices=["user_friendly", "json", "standard"],
        help="Set the logging format (default: user_friendly)"
    )
    
    return parser

async def main():
    """Main entry point for the service."""
    # Parse command line arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Configure logging based on command line arguments or environment variables
    log_level = get_log_level_from_env(args.log_level)
    log_format = args.log_format
    
    # Map string format to enum
    format_mapping = {
        "user_friendly": LoggingFormat.USER_FRIENDLY,
        "json": LoggingFormat.JSON,
        "standard": LoggingFormat.STANDARD
    }
    logging_format = format_mapping.get(log_format, LoggingFormat.USER_FRIENDLY)
    
    # Apply logging configuration
    configure_logging(level=log_level, format=logging_format)
    
    # Log startup message
    logger.info("Insyt Secure Execution Service starting up")
    
    # Set up a hook for the SIGTERM signal
    def handle_sigterm(*args):
        logger.info("Received SIGTERM signal, shutting down...")
        # We'll raise a KeyboardInterrupt to break out of the main loop
        raise KeyboardInterrupt()
    
    # Register the signal handler
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    # Check if required configurations are provided
    if not args.project_id:
        logger.error("Project ID not provided. Use --project-id or set INSYT_PROJECT_ID environment variable.")
        sys.exit(1)
    
    # Parse network security settings
    allowed_hosts = None
    if args.allowed_hosts:
        allowed_hosts = [h.strip() for h in args.allowed_hosts.split(",")]
        logger.debug(f"Using allowed hosts: {allowed_hosts}")
    
    always_allowed_domains = [d.strip() for d in args.always_allowed_domains.split(",")]
    logger.debug(f"Using always allowed domains: {always_allowed_domains}")
    
    # Main service loop
    while True:
        try:
            # Get credentials from the API
            credentials = get_credentials(args.project_id, args.api_url, args.api_key)
            logger.info("Successfully acquired valid credentials")
            
            # Log the topic information but mask sensitive data
            masked_username = credentials['username'][:3] + "..." if credentials['username'] else None
            logger.info(f"Subscription topic: {credentials['topic']}")
            logger.info(f"Broker: {credentials['broker']}:{credentials['port']}, SSL: {credentials.get('ssl_enabled', True)}")
            logger.debug(f"Username: {masked_username}")
            
            # Initialize executor with credentials
            logger.info("Initializing execution service...")
            executor = CodeExecutor(
                mqtt_broker=credentials['broker'],
                mqtt_port=int(credentials['port']),
                mqtt_username=credentials['username'],
                mqtt_password=credentials['password'],
                subscribe_topic=credentials['topic'],
                publish_topic=credentials.get('response_topic', f"response/{credentials['topic']}"),  # Fallback response topic
                ssl_enabled=credentials.get('ssl_enabled', True),
                allowed_ips=allowed_hosts,
                always_allowed_domains=always_allowed_domains,
                max_workers=args.max_workers,
                execution_timeout=args.timeout
            )
            
            # Start the executor
            logger.info("Starting service and listening for execution requests...")
            await executor.start()
            
            # If executor.start() returns normally, it means credentials have expired
            logger.warning("Connection lost or credentials expired. Getting new credentials...")
            
        except NetworkRestrictionError as e:
            # Network restriction errors are critical security issues - exit immediately
            logger.critical(f"Network security error: {str(e)}")
            sys.exit(1)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C or SIGTERM
            logger.info("Shutdown signal received. Exiting...")
            break
            
        except Exception as e:
            # Handle any other exceptions
            logger.exception(f"Unexpected error: {str(e)}")
            logger.info(f"Restarting in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    # Run the main async function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete.")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

def run_main():
    """Entry point for the command-line script."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete.")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)