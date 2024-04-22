import base64

import requests


class PinterestOAuth:
    def __init__(self, config):
        self.config = config
        self.client_id = config['client_id']
        self.redirect_url = config['redirect_url']
        self.client_secret = config['client_secret']

    def generate_auth_url(self):
        url = "https://www.pinterest.com/oauth/"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "response_type": "code",
            "scope": "ads:read,boards:read,boards:read_secret,boards:write,boards:write_secret,pins:read,pins:read_secret,pins:write,pins:write_secret,user_accounts:read,catalogs:read,catalogs:write"
        }
        auth_url = requests.Request('GET', url, params=params).prepare().url
        return auth_url

    def open_auth_url(self):
        auth_url = self.generate_auth_url()
        print("In order to be able to publish pins using a code, you need to log in. Please paste the link into the browser where you have an authorized pinterest account.")
        print(auth_url)

    def get_access_token(self):
        code = input("Please enter the code that you received as a result of authorization, it is in the search bar after 'code=':")
        url = "https://api.pinterest.com/v5/oauth/token"
        auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")

        headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
          'grant_type': 'authorization_code',
          'code': f'{code}',
          'redirect_uri': self.redirect_url
        }

        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if 'access_token' in response_json:
            print("Great! now you can upload your pins to pinterest")
            print(response_json['access_token'])
            return response_json['access_token']
        else:
            print("Error: ", response_json)
            return None
