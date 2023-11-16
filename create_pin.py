import json
import random
import time

from ip import proxy
import requests
from config import get_token_from_file



def create_pin(board_id, description, title, img_url, link, token, use_proxy):
    # Replace the following values with your own
    board_id = board_id
    # API URL
    url = "https://api.pinterest.com/v5/pins"
    # Request headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Request data
    data = {
        "link": link,
        "title": title,
        "description": description,
        "board_id": board_id,
        "media_source": {
            "source_type": "image_url",
            "url": img_url
    },

    }
    # Send POST request
    if use_proxy:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy())
    else:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # Parse JSON response
    json_response = response.json()
    # Print response
    print(json_response)
