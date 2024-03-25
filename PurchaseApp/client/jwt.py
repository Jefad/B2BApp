# Blog post reference: https://www.codingforentrepreneurs.com/blog/python-jwt-client-django-rest-framework-simplejwt

from dataclasses import dataclass 
import requests
from getpass import getpass
import pathlib 
import json


@dataclass
class JWTClient:
    access: str = None
    refresh: str = None
    header_type: str = "Bearer"
    base_endpoint = "http://localhost:8000/api/auth"
    cred_path: pathlib.Path = pathlib.Path("creds.json")

    def __post_init__(self):
        if self.cred_path.exists():
            try:
                data = json.loads(self.cred_path.read_text())
            except Exception:
                print("Assuming creds has been tampered with")
                data = None
            if data is None:
                self.clear_tokens()
                self.perform_auth()
            else:
                self.access = data.get('access')
                self.refresh = data.get('refresh')
                token_verified = self.verify_token()
                if not token_verified:
                    refreshed = self.perform_refresh()
                    if not refreshed:
                        print("invalid data, login again.")
                        self.clear_tokens()
                        self.perform_auth()
        else:
            self.perform_auth()
        
    def get_headers(self, header_type=None):
        _type = header_type or self.header_type
        token = self.access
        if not token:
            return {}
        return {
                "Authorization": f"{_type} {token}"
        }

    def perform_auth(self):
        endpoint = f"{self.base_endpoint}/token/" 
        username = input("What is your username?\n")
        password = getpass("What is your password?\n")
        response = requests.post(endpoint, json={'username': username, 'password': password})
        if response.status_code != 200:
            raise Exception(f"Access not granted: {response.text}")
        print('access granted')
        self.write_creds(response.json())

    def write_creds(self, data: dict):
        if self.cred_path is not None:
            self.access = data.get('access')
            self.refresh = data.get('refresh')
            if self.access and self.refresh:
                self.cred_path.write_text(json.dumps(data))
    
    def verify_token(self):
        data = {
            "token": f"{self.access}"
        }
        endpoint = f"{self.base_endpoint}/token/verify/" 
        response = requests.post(endpoint, json=data)
        return response.status_code == 200
    
    def clear_tokens(self):
        self.access = None
        self.refresh = None
        if self.cred_path.exists():
            self.cred_path.unlink()
    
    def perform_refresh(self):
        print("Refreshing token.")
        headers = self.get_headers()
        data = {
            "refresh": f"{self.refresh}"
        }
        endpoint = f"{self.base_endpoint}/token/refresh/" 
        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code != 200:
            self.clear_tokens()
            return False
        refresh_data = response.json()
        if not 'access' in refresh_data:
            self.clear_tokens()
            return False
        stored_data = {
            'access': refresh_data.get('access'),
            'refresh': self.refresh
        }
        self.write_creds(stored_data)
        return True

    def list(self, endpoint=None, limit=3):
        headers = self.get_headers()
        if endpoint is None or self.base_endpoint not in str(endpoint):
            endpoint = f"{self.base_endpoint}/products/?limit={limit}" 
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Request not complete {response.text}")
        data = response.json()
        return data


if __name__ == "__main__":

    client = JWTClient()
    print({'access': client.access})

    # lookup_1_data = client.list(limit=5)
    #
    # results = lookup_1_data.get('results')
    # next_url = lookup_1_data.get('next')
    # print("First lookup result length", len(results))
    # if next_url:
    #     lookup_2_data = client.list(endpoint=next_url)
    #     results += lookup_2_data.get('results')
    #     print("Second lookup result length", len(results))
