# Reservoir SDK

A simple Python client for the Reservoir video querying system.

## Installation

```bash
pip install reservoir-sdk
```

## Authentication

You must provide an API key to use the Reservoir SDK. The API key can be passed directly to the client or set via the `RESERVOIR_API_KEY` environment variable:

```python
# Directly in code
client = ReservoirClient(api_key="your-api-key-here")

# Or via environment variable
# export RESERVOIR_API_KEY="your-api-key-here"
client = ReservoirClient()  # Will use RESERVOIR_API_KEY env var
```

## Usage

```python
from reservoir_sdk import ReservoirClient

# Initialize with API key
client = ReservoirClient(api_key="your-api-key-here")

# Simple query
result = client.query(
    query_text="People having a conversation",
    max_duration_minutes=5.0,
    min_confidence=0.7
)

print(f"Query submitted! Job ID: {result['job_id']}")
print(f"Check results at: {result['result_url']}")

# Get available models
models = client.get_available_models()
print(f"Available models: {models}")

# List creators
creators = client.list_creators()
print(f"Found {len(creators)} creators")

# Get a specific creator's ID
if creators:
    creator_id = creators[0]['id']
    
    # Query with a specific creator
    result = client.query(
        query_text="People laughing",
        creators_ids=[creator_id],
        max_duration_minutes=2.0
    )
    
    print(f"Creator-specific query submitted! Job ID: {result['job_id']}")

# Check status of a query
status = client.get_query_status(result['job_id'])
print(f"Query status: {status['status']}")
```

## API Reference

### Client Initialization

```python
client = ReservoirClient(
    api_key="your-api-key-here",  # Required unless RESERVOIR_API_KEY env var is set
    base_url="http://localhost:8000"  # Optional, defaults to http://localhost:8000
)
```

### Methods

#### query

Submit a query to search for video segments.

```python
result = client.query(
    query_text="People having a conversation",  # Required
    max_duration_minutes=5.0,  # Optional, defaults to 10.0
    max_chunks=20,  # Optional, defaults to 20
    min_confidence=0.7,  # Optional, defaults to 0.5
    models=["active_speaker", "conversation_confidence"],  # Optional, defaults to all models
    creators_ids=["creator-id-1", "creator-id-2"]  # Optional, defaults to all creators
)
```

#### get_query_status

Check the status of a submitted query.

```python
status = client.get_query_status(job_id)
```

#### list_creators

Get a list of all available creators.

```python
creators = client.list_creators()
```

#### get_available_models

Get a dictionary of available models.

```python
models = client.get_available_models()
```

## Requirements

- Python 3.7+
- `requests` library

## Development

To build and install the package locally for development:

```bash
git clone https://github.com/yourusername/reservoir-sdk.git
cd reservoir-sdk
pip install -e .
``` 