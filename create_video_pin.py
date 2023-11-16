import time

import requests
import json
from ip import proxy
from create_cover import cover, encod
from config import get_token_from_file
import re

def register_intention(token, use_proxy, owner):
    url = 'https://api.pinterest.com/v5/media'
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {'media_type': 'video'}
    if use_proxy:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy(owner))
    else:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    if response_data.get('status') == 'failure':
        print(f"Authentication error: {response_data.get('message')}")
        return None

    return response_data


def upload_videfile(filepath, response_data, use_proxy, owner):
    print(response_data)
    url = response_data['upload_url']
    print(url)
    video_input_path = f'accounts/{owner}/content/{filepath}'
    data = {
        'x-amz-date': response_data['upload_parameters']['x-amz-date'],
        'x-amz-signature': response_data['upload_parameters']['x-amz-signature'],
        'x-amz-security-token': response_data['upload_parameters']['x-amz-security-token'],
        'x-amz-algorithm': response_data['upload_parameters']['x-amz-algorithm'],
        'key': response_data['upload_parameters']['key'],
        'policy': response_data['upload_parameters']['policy'],
        'x-amz-credential': response_data['upload_parameters']['x-amz-credential'],
        'Content-Type': response_data['upload_parameters']['Content-Type'],
    }
    with open(video_input_path, 'rb') as f:
        video_input_path = {'file': f}
        if use_proxy:
            response = requests.post(url, data=data, files=video_input_path, proxies=proxy(owner))
        else:
            response = requests.post(url, data=data, files=video_input_path)
    status_code = print(response.status_code)
    return status_code


def confirm_the_download(response_data, token, use_proxy, owner):
    media_id = response_data['media_id']
    url = f'https://api.pinterest.com/v5/media/{media_id}'
    headers = {
        "Authorization": f"Bearer {token}"}
    if use_proxy:
        response = requests.get(url, headers=headers, proxies=proxy(owner))
    else:
        response = requests.get(url, headers=headers)

    print(response.json())


def post_pin(title, description, board_id, response_data, token, link, owner, filepath, use_proxy):
    media_id = response_data['media_id']
    url = 'https://api.pinterest.com/v5/pins'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    data = {
        "link": link,
        "title": title,
        "description": description,
        "board_id": board_id,
        "media_source": {
            "source_type": "video_id",
            "cover_image_content_type": "image/jpeg",
            "cover_image_data": f"{encod(owner)}",
            "media_id": media_id
        }
    }

    if use_proxy:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy(owner))
    else:
        response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.json())
    status_code = response.status_code
    return status_code


def all_steps_upload_video(owner, title, description, board_id, link, filepath, use_proxy):
    token = get_token_from_file(f"accounts/{owner}/access_token.txt")

    # Add a new parameter `use_proxy` to the function call
    cover(owner, filepath)

    data = register_intention(token, use_proxy, owner)

    upload_videfile(filepath, data, use_proxy, owner)

    confirm_the_download(data,token, use_proxy, owner)

    res = post_pin(title,
             description,
             board_id,
             data,
             token,
             link,
             owner,
             filepath, use_proxy)
    return res

