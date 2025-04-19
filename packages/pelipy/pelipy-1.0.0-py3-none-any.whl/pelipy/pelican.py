import requests
from .objects import *

class Pelican:
    def __init__(self, api_key: str, panel_url: str):
        self.api_key = api_key
        self.api_url = panel_url + "/api/client/"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        print(self.api_url)
        print(self.headers)
        print(self.api_key)
    
    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.api_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if response.status_code == 204:
            return None

        try:
            data = response.json()
        except requests.JSONDecodeError:
            raise Exception(
                f"Failed to decode JSON:\nStatus: {response.status_code}\nURL: {url}\nResponse: {response.text[:300]}"
            )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        return data

    
    def server(self, server_id: str) -> Server:
        data = self._request("GET", f"servers/{server_id}")
        return Server(data.get("attributes", {}), self)