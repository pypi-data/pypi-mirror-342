# PySilentWave

![PyPI](https://img.shields.io/pypi/v/pysilentwave)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/thesilentwave/pysilentwave/Publish%20to%20PyPI)

API client for TheSilentWave devices.

## Installation

```bash
pip install pysilentwave
```

## Usage

```python
import asyncio
from pysilentwave import SilentWaveClient

async def main():
    client = SilentWaveClient("192.168.1.100")
    status = await client.get_status()
    print(f"Device status: {status}")

asyncio.run(main())
```

## Requirements

- Python 3.9 or higher
- aiohttp 3.8.0 or higher

## License

MIT