# Insyt Secure

A proprietary service for securely interacting with databases, APIs, and other services within a secure environment. Visit https://insyt.co for more information.

## Quick Start

### Installation

```bash
# Basic installation (core functionality only)
pip install insyt-secure
```

#### Advanced Installation Options

Insyt Secure provides flexible installation options to include only the dependencies you need:

```bash
# Install with PostgreSQL support
pip install "insyt-secure[postgres]"

# Install with MongoDB support
pip install "insyt-secure[mongodb]"

# Install with multiple database support
pip install "insyt-secure[postgres,mongodb,redis]"

# Install with vector database support
pip install "insyt-secure[pinecone]" # or any other vector DB

# Install with cloud provider support
pip install "insyt-secure[aws]" # or azure

# Install with messaging system support
pip install "insyt-secure[kafka]" # or rabbitmq, pulsar

# Complete installation with all dependencies
pip install "insyt-secure[all]"
```

Available extension categories:
- SQL databases: `postgres`, `mysql`, `mssql`, `oracle`, `clickhouse`, `snowflake`, `duckdb`
- NoSQL databases: `mongodb`, `redis`, `cassandra`, `neo4j`, `elasticsearch`, `couchdb`
- Vector databases: `pinecone`, `qdrant`, `milvus`, `weaviate`, `chroma`, `faiss`
- Cloud services: `aws`, `azure`
- Messaging systems: `kafka`, `pulsar`, `rabbitmq`

Broader categories are also available: `rdbms`, `nosql`, `vector`, `cloud`, `messaging`

### Basic Usage

```bash
# Run with required parameters
insyt-secure --project-id your-project-id-123 --api-key your-api-key-xyz
```

### Getting Help

```bash
# View all available options and examples
insyt-secure --help
```

The help command provides detailed information about all parameters, their defaults, and usage examples directly in your terminal.

### Advanced Options

```bash
# Run with all options
insyt-secure \
  --project-id your-project-id-123 \
  --api-key your-api-key-xyz \
  --max-workers 10 \
  --execution-timeout 60 \
  --allowed-ips "192.168.1.1,10.0.0.1:3456"
```

### Logging Options

By default, logs are user-friendly and redact sensitive information. You can customize logging behavior:

```bash
# Enable more detailed debug logs
insyt-secure --project-id your-project-id --api-key your-api-key --debug

# Show more verbose logs including from third-party libraries
insyt-secure --project-id your-project-id --api-key your-api-key --verbose

# Output logs in JSON format (useful for log processing systems)
insyt-secure --project-id your-project-id --api-key your-api-key --json-logs

# Disable redaction of sensitive information (not recommended for production)
insyt-secure --project-id your-project-id --api-key your-api-key --show-sensitive
```

You can also control the log level via environment variables:

```bash
# Set log level using environment variable
INSYT_LOG_LEVEL=DEBUG insyt-secure --project-id your-project-id --api-key your-api-key
```

## Cross-Platform Compatibility

Insyt Secure is designed to work seamlessly on all major platforms:

- **Windows**: Fully supported natively, no additional configuration needed
- **macOS**: Fully supported
- **Linux**: Fully supported

The service uses paho-mqtt with a platform-agnostic implementation to ensure consistent behavior across all operating systems.

## Command Line Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--project-id` | Your Insyt project ID (required) | - |
| `--api-key` | Your Insyt API key (required) | - |
| `--max-workers` | Maximum number of concurrent code executions | 5 |
| `--execution-timeout` | Default maximum execution time in seconds per code snippet | 30 |
| `--allowed-ips` | Comma-separated list of allowed IPs/hostnames | All allowed |
| `--verbose` | Enable more verbose logs | False |
| `--debug` | Enable debug level logging | False |
| `--json-logs` | Output logs in JSON format | False |
| `--show-sensitive` | Show sensitive information in logs | False |

## Credentials Management

This service automatically retrieves and manages connection credentials:

1. When the service starts, it gets credentials from the Insyt API
2. If the connection drops or credentials expire, it automatically requests new credentials


## Use Cases

### Data Processing Microservice

Perfect for running data transformation code that connects to various data sources:

```bash
insyt-secure --project-id your-project-id --api-key your-api-key --max-workers 15
```

### Secure Environment for Code Testing

Create a sandboxed environment with restricted network access:

```bash
insyt-secure --project-id your-project-id --api-key your-api-key \
  --allowed-ips "10.0.0.1,192.168.1.100" --execution-timeout 20
```

### Containerized Deployment

```bash
docker run -d --name insyt-secure \
  insyt-secure insyt-secure \
  --project-id your-project-id --api-key your-api-key
```

## System Requirements and Dependencies

Insyt Secure is designed with a modular dependency structure to minimize installation size and resource usage. Below is a breakdown of what's included in each installation option:

### Core Dependencies (included in base install)

The base installation includes:
- HTTP client capabilities via `httpx`
- MQTT connectivity via `paho-mqtt`
- Basic data science libraries: NumPy, Pandas, SciPy
- JSON and date handling utilities

### Optional Dependencies

#### SQL Database Connectors
- `postgres`: High-performance PostgreSQL client (asyncpg)
- `mysql`: MySQL client libraries
- `mssql`: Microsoft SQL Server connectivity
- `oracle`: Oracle database connectivity
- `clickhouse`: ClickHouse analytics database client
- `snowflake`: Snowflake data warehouse client
- `duckdb`: Embedded analytical database

#### NoSQL Database Connectors
- `mongodb`: MongoDB client with async support
- `redis`: Redis client
- `cassandra`: Apache Cassandra and ScyllaDB clients
- `neo4j`: Neo4j graph database client
- `elasticsearch`: Elasticsearch search engine client
- `couchdb`: CouchDB document database client

#### Vector Database Connectors
- `pinecone`: Pinecone vector database client
- `qdrant`: Qdrant vector search engine client
- `milvus`: Milvus vector database client
- `weaviate`: Weaviate vector search engine
- `chroma`: ChromaDB for AI embeddings
- `faiss`: Facebook AI Similarity Search

#### Cloud Services
- `aws`: AWS SDK (boto3) with S3, Dynamo, etc.
- `azure`: Azure clients for Cosmos DB, Blob Storage, etc.

#### Messaging Systems
- `kafka`: Apache Kafka client
- `pulsar`: Apache Pulsar client
- `rabbitmq`: RabbitMQ client

### Performance Considerations

The base installation already includes the core ML libraries (numpy, pandas, etc.). If you're installing on a resource-constrained environment, consider using only the specific connector extensions you need rather than the broader categories.

For production deployments, we recommend specifying exact dependencies rather than using broader categories:

```bash
# Good (minimal dependencies)
pip install "insyt-secure[postgres,redis]"

# Less efficient (pulls in many unused dependencies)
pip install "insyt-secure[rdbms,nosql]"
```

### Platform-Specific Installation

Insyt Secure is designed to work on all major platforms without modification:

#### Windows

```bash
# Install on Windows
pip install insyt-secure

# Run (in PowerShell or Command Prompt)
insyt-secure --project-id your-project-id-123 --api-key your-api-key-xyz
```

#### macOS/Linux

```bash
# Install on macOS/Linux
pip install insyt-secure

# Run
insyt-secure --project-id your-project-id-123 --api-key your-api-key-xyz
```

#### Docker

```bash
# Create a simple Dockerfile
echo 'FROM python:3.10-slim
RUN pip install insyt-secure
ENTRYPOINT ["insyt-secure"]' > Dockerfile

# Build the Docker image
docker build -t insyt-secure .

# Run in Docker
docker run insyt-secure --project-id your-project-id-123 --api-key your-api-key-xyz
```

#### Platform-Specific Considerations

- **Windows**: Works natively without WSL, using a cross-platform MQTT implementation
- **MacOS/Linux**: All features fully supported
- **Docker**: Ideal for deployment in containerized environments


#### Installing on a Fresh Ubuntu Instance

Follow these steps to set up insyt-secure on a fresh Ubuntu installation:

```bash
# Step 1: Install required packages
sudo apt update
sudo apt install python3-pip
sudo apt install python3-venv python3-full

# Step 2: Create a directory for your project (optional)
mkdir myproject
cd myproject

# Step 3: Create the virtual environment
python3 -m venv venv

# Step 4: Activate the virtual environment
source venv/bin/activate
# Your command prompt should change to show the virtual environment name
# Example: (venv) ubuntu@ip-100-1-11-111:~/myproject$

# Step 5: Install insyt-secure with desired extensions
pip install insyt-secure[mysql,postgres]
pip install python-dotenv
```

**Notes:**
1. To run the service, use the following command:
```bash
insyt-secure --project-id your-project-id --api-key your-api-key
```
or run the service in the background:
```bash
nohup insyt-secure --project-id your-project-id --api-key your-api-key &
```

2. Remember to activate the virtual environment each time you want to use this package in a new terminal session.
```bash
source venv/bin/activate
```

3. To deactivate the virtual environment when you're done:
```bash
deactivate
```

4. To stop the service, use the following command:
```bash
pkill -f insyt-secure
```

5. To check the status of the service, use the following command:
```bash
ps aux | grep insyt-secure
```



