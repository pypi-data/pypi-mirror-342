import requests
import json


class AmplifierJWTAuth:
    def __init__(self, username, password, auth_url):
        self.username = username
        self.password = password
        self.auth_url = f'{auth_url}auth/'

    def get_token(self):
        uri = self.auth_url
        payload = {
            'password': self.password,
            'username': self.username
        }
        response = requests.post(uri, data=payload)
        response_content = response.text
        jwt_obj = json.loads(response_content)
        return jwt_obj
