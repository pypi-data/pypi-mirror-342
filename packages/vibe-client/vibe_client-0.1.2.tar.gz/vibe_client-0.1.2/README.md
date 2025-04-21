# Vibe Python SDK

A Python client for the Vibe API, enabling seamless interaction with Vibe agents and experiments.

## Installation

```bash
pip install vibe_client
```

## Features

- Easy-to-use client for interacting with Vibe API
- Comprehensive data models for structuring requests and responses
- Async support for efficient API communication
- Built-in error handling and serialization/deserialization

## Quick Start

```python
import asyncio
from vibe_client.models import QueryAgentInput, ObservationValueBox
from vibe_client.client import VibeClient

async def main():
    # Initialize the client with your API key
    client = VibeClient(api_key="your_api_key_here")
    
    # Create observations
    observations = ObservationValueBox([
        [1, 1.2, 3.0],
        [1, 1.2, 3.0],
        [1, 1.2, 3.0],
        [1, 1.2, 3.0],
        [1, 1.2, 3.0]
    ])
    
    # Set up query input
    query_input = QueryAgentInput(
        experiment_id="your_experiment_id",
        observations=observations
    )
    
    # Execute the query
    try:
        response = await client.query_agent(input=query_input)
        print("Query response:", response)
        print("Actions:", response.actions)
    except Exception as e:
        print(f"Error executing query_agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

Full documentation is available in the `/docs` directory. To build the documentation:

```bash
cd docs
make html
```

The built documentation will be available in `docs/build/html/index.html`.

## Project Structure

```
vibe/
├── src/vibe_client/            # Main package source code
│   ├── __init__.py      # Package initialization
│   ├── client.py        # API client implementation
│   ├── config.py        # Configuration utilities
│   ├── models.py        # Data models
│   ├── serialize.py     # Serialization utilities
│   ├── deserialize.py   # Deserialization utilities
│   └── _private/        # Private implementation details
├── tests/               # Test suite
├── docs/                # Documentation
│   ├── client/          # Client API documentation
│   └── models/          # Models documentation
└── build/               # Build artifacts
```

## Development

### Setting Up Development Environment

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest tests/
   ```


