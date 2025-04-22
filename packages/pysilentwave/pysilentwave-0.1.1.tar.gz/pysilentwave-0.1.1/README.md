# PySilentWave

A Python client library for TheSilentWave API.

## Installation

```bash
pip install pysilentwave
```

## Usage

```python
import asyncio
from pysilentwave import SilentWaveClient

async def main():
    # Initialize the client with your device's IP
    client = SilentWaveClient("192.168.1.100")
    
    # Get the current status
    status = await client.get_status()
    print(f"Device status: {status}")

asyncio.run(main())
```

## Requirements

- Python 3.9 or higher
- aiohttp 3.8.0 or higher

## License

MIT