import requests
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup  # For prettifying HTML

# Response Wrapper for sync and async
class ResponseWrapper:
    def __init__(self, resp):
        self.status_code = resp.status_code if isinstance(resp, requests.Response) else resp.status
        self.ok = resp.ok if isinstance(resp, requests.Response) else 200 <= resp.status < 300
        self.text = resp.text if isinstance(resp, requests.Response) else None
        self.json_data = None
        try:
            self.json_data = resp.json() if isinstance(resp, requests.Response) else json.loads(self.text)
        except:
            pass
    
    def json(self):
        return self.json_data

# Sync Client
class HyperIO:
    def __init__(self, headers=None):
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(self, url, **kwargs):
        return ResponseWrapper(self.session.get(url, **kwargs))

    def post(self, url, data=None, json=None, **kwargs):
        return ResponseWrapper(self.session.post(url, data=data, json=json, **kwargs))

    def put(self, url, data=None, **kwargs):
        return ResponseWrapper(self.session.put(url, data=data, **kwargs))

    def delete(self, url, **kwargs):
        return ResponseWrapper(self.session.delete(url, **kwargs))

    def download(self, url, filename):
        r = self.session.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    def login(self, url, username, password):
        return self.post(url, json={'username': username, 'password': password})

    def register(self, url, username, password, email=None):
        data = {'username': username, 'password': password}
        if email:
            data['email'] = email
        return self.post(url, json=data)

    def view_html(self, url):
        """Fetch HTML content and render in a readable format."""
        response = self.get(url)
        if response.ok:
            # Beautify the HTML using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.prettify()  # Returns prettified HTML as a string
        else:
            return f"Failed to fetch HTML. Status Code: {response.status_code}"

# Async Client
class AsyncHyperIO:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as resp:
            return await self._wrap(resp)

    async def post(self, url, data=None, json=None, **kwargs):
        async with self.session.post(url, data=data, json=json, **kwargs) as resp:
            return await self._wrap(resp)

    async def put(self, url, data=None, **kwargs):
        async with self.session.put(url, data=data, **kwargs) as resp:
            return await self._wrap(resp)

    async def delete(self, url, **kwargs):
        async with self.session.delete(url, **kwargs) as resp:
            return await self._wrap(resp)

    async def download(self, url, filename):
        async with self.session.get(url) as r:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await r.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    async def login(self, url, username, password):
        return await self.post(url, json={'username': username, 'password': password})

    async def register(self, url, username, password, email=None):
        data = {'username': username, 'password': password}
        if email:
            data['email'] = email
        return await self.post(url, json=data)

    async def view_html(self, url):
        """Fetch HTML content and render in a readable format."""
        response = await self.get(url)
        if response['ok']:
            # Beautify the HTML using BeautifulSoup
            soup = BeautifulSoup(response['text'], 'html.parser')
            return soup.prettify()  # Returns prettified HTML as a string
        else:
            return f"Failed to fetch HTML. Status Code: {response['status']}"

    async def _wrap(self, resp):
        text = await resp.text()
        try:
            json_data = await resp.json()
        except:
            json_data = None
        return {
            'status': resp.status,
            'ok': 200 <= resp.status < 300,
            'text': text,
            'json': json_data
        }

    async def close(self):
        await self.session.close()

# Usage Example (Sync):
# client = HyperIO()
# html_content = client.view_html("https://www.example.com")
# print(html_content)

# Usage Example (Async):
# async def main():
#     client = AsyncHyperIO()
#     html_content = await client.view_html("https://www.example.com")
#     print(html_content)
#     await client.close()

# asyncio.run(main())
