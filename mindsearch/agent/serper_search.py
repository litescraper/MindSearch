# Candidate for etheia-agent-map — no existing equivalent could be inspected.
# See: https://github.com/Etheia-Consulting-LLC/etheia-agent-map
# Transport methods adapted from lagent/actions/web_browser.py, lagent 0.5.0rc2.
# Local modification: configure the endpoint; inherit parsing, filtering,
# caching, retries, authentication, request parameters, and browser behavior.
import aiohttp
import requests
from lagent.actions.web_browser import GoogleSearch


class ConfigurableGoogleSearch(GoogleSearch):

    def __init__(self, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url.rstrip('/')

    def _call_serper_api(self, query: str) -> dict:
        endpoint = f'{self.base_url}/{self.search_type}'
        params = {
            'q': query,
            'num': self.topk,
            **{
                key: value
                for key, value in self.kwargs.items() if value is not None
            },
        }
        headers = {
            'X-API-KEY': self.api_key or '',
            'Content-Type': 'application/json'
        }
        response = requests.get(endpoint,
                                headers=headers,
                                params=params,
                                proxies=self.proxy)
        response.raise_for_status()
        return response.json()

    async def _async_call_serper_api(self, query: str) -> dict:
        endpoint = f'{self.base_url}/{self.search_type}'
        params = {
            'q': query,
            'num': self.topk,
            **{
                key: value
                for key, value in self.kwargs.items() if value is not None
            },
        }
        headers = {
            'X-API-KEY': self.api_key or '',
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(
                    endpoint,
                    headers=headers,
                    params=params,
                    proxy=(self.proxy
                           and (self.proxy.get('http')
                                or self.proxy.get('https')))) as resp:
                return await resp.json()
