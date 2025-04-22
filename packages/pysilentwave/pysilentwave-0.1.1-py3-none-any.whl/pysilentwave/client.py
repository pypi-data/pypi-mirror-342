"""Client for TheSilentWave devices."""

import aiohttp
from .exceptions import SilentWaveError


class SilentWaveClient:
    """Client to interact with TheSilentWave API."""

    def __init__(self, host):
        """Initialize the client."""
        self._host = host
        self._base_url = f"http://{host}:8080/api"

    async def get_status(self):
        """Get the current status."""
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self._base_url}/status"
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.text()
                    return "on" if data.strip() == "1" else "off"
            except aiohttp.ClientError as err:
                raise SilentWaveError(f"Error communicating with device: {err}") from err
