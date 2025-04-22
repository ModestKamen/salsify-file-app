# Line Server System Analysis

## How does your system work?

The system is a distributed line server designed for scalable and efficient access to specific lines of a large text file.

### 1. Architecture
- Built in **Python 3.13** using the **aiohttp** framework for asynchronous HTTP handling.
- Follows a microservices architecture, with **NGINX** as a load balancer.
- Each service instance handles a range of line numbers (e.g., lines 1–100, 101–200).
- **Index files** store byte offsets where each line begins.
- Each index entry is 13 bytes: 12 bytes for the byte offset and 1 for `\n`.
- Knowing the fixed entry size allows calculation of the offset in the index file for a given line.
- The offset is then used to retrieve the corresponding line from the main file.

### 2. Components
- `FileIndexRepository`: Maps line numbers to byte offsets using the index file.
- `FileRepository`: Reads from the main data file using those offsets.
- `NGINX`: Routes requests to the appropriate service shard based on the line number.
- Dockerized for ease of deployment and scaling.

### 3. Data Storage
- Index file allows **O(1)** access to any line.
- The main file is read using offsets from the index file.
- Files are sharded and assigned to instances based on line number ranges.

## Performance Analysis

### File Size Performance

Tested on 5GB and 10GB files using **Locust** for load testing with 1,000+ concurrent connections to a single instance.

- **Average latency**: ~50ms
- **Test environment**: MacBook Air M1, 16GB RAM, 512GB SSD

The system is I/O-bound and performs well due to efficient byte-offset access.

### Concurrent Users Performance

#### 100 Users
- Easily handled by a single instance.

#### 10,000 Users
- Requires more workers per shard.
- One NGINX instance should suffice for routing.

#### 1,000,000 Users
- Requires horizontal scaling: more service replicas and potentially multiple file copies.
- Use DNS or GEO-based routing for geographic distribution.
- Add monitoring and auto-scaling for reliability.

## Technical Choices

### Libraries and Tools

- **aiohttp**: Async server framework, ideal for non-blocking I/O.
- **NGINX**: Reverse proxy and load balancer, enables efficient routing and fault tolerance.
- **Docker**: Simplifies deployment, scalability, and consistency across environments.
- **Pydantic**: Provides type-safe settings management and validation.

### Resources Consulted

- aiohttp official documentation
- Articles on file indexing strategies
- Benchmarking practices for high-throughput systems

## Development Time

- Planning & Design: ~3 hours  
- Implementation: ~5 hours  
- Testing & Optimization: ~4 hours  
- Documentation: ~2 hours  
**Total**: ~14–16 hours

## Future Improvements

Given unlimited time, I would:

- Add support for **streaming** responses to improve performance with large responses.
- Improve test coverage, including load and edge cases.
- Support reading from the end of the file, which might be more efficient in some cases.

## Self Review

### Areas for Improvement
- Add structured logging for observability.
- Improve automated test suite.
- Optimize end-of-file access paths.
- Improve fault tolerance in case of file corruption or shard failure.

## Local Installation

### Prerequisites

1. Install Python 3.13:
```bash
# On macOS using Homebrew
brew install python@3.13

# Verify installation
python3.13 --version
```

### Setting up Development Environment

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
make install
```

### Running Tests

```bash
make test
```

## Testing Instructions

### Running the Service

1. Clone the project and ensure Docker is installed.
2. Run the service:
```bash
./run.sh
```
The service starts at `http://localhost:8001`, serving lines 1 to 100.

### Testing with Your Own Data

1. **Prepare Data**:
   - Place your text file in the `LOCAL_PROD_DATA` directory.
   - Ensure each line ends with `\n`.

2. **Generate Index File**:
```bash
python -m commands/create_index_file LOCAL_PROD_DATA/your_data_file.txt
```
This creates `your_data_file.txt_index.txt`.

3. **Configure Docker**:
Update `docker-compose-single-instance.yml`:
```yaml
- INDEX_FILE_PATH=/app/LOCAL_PROD_DATA/your_data_file.txt_index.txt
- INDEX_FIRST_LINE_NUMBER=1
- INDEX_LAST_LINE_NUMBER=<your_max_line_number>
- FILE_REPOSITORY_FILE_PATH=/app/LOCAL_PROD_DATA/your_data_file.txt
```

4. **Start the Service**:
```bash
./run.sh
```

5. **Test Endpoint**:
```bash
curl http://localhost:8001/lines/1
```
