import asyncio
import logging

import aiohttp


class RequestScheduler:
    def __init__(self, rate_limits):
        """
        Initializes the RequestScheduler with rate limits for each API.

        :param rate_limits: Dictionary containing rate limits for different APIs.
        """
        self.rate_limits = rate_limits
        self.session = aiohttp.ClientSession()
        self.request_queues = {api: asyncio.Queue() for api in rate_limits}
        self.lock = asyncio.Lock()

    async def fetch(self, url, api_name, params=None):
        """
        Fetches data asynchronously from the given URL, adhering to the rate limits.

        :param url: API endpoint URL
        :param api_name: API name for rate limiting
        :param params: Optional query parameters
        """
        if api_name not in self.rate_limits:
            raise ValueError(f"Unknown API: {api_name}")

        async with self.lock:
            # Enforce rate limiting
            await asyncio.sleep(60 / self.rate_limits[api_name])

        try:
            async with self.session.get(url, params=params) as response:
                return await response.json()
        except Exception as e:
            logging.error(f"Error fetching data from {url}: {e}")
            return None

    async def close(self):
        """Closes the session."""
        await self.session.close()
