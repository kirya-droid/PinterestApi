
import requests
import base64
import webbrowser
import json
import os


def get_config():
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    return config


def OAuth(config):
    client_id = config['client_id']
    redirect_url = config['redirect_url']
    text = " In order to be able to publish pins using a code, you need to log in. Please paste the link into the browser where you have an authorized pinterest account."
    url = "https://www.pinterest.com/oauth/"

    # Параметры запроса
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_url,
        "response_type": "code",
        "scope": "ads:read,boards:read,boards:read_secret,boards:write,boards:write_secret,pins:read,pins:read_secret,pins:write,pins:write_secret,user_accounts:read,catalogs:read,catalogs:write"
    }

    # Создать URL-адрес для авторизации
    auth_url = requests.Request('GET', url, params=params).prepare().url

    # Открыть URL в браузере
    #webbrowser.open(auth_url)

    # Вывести URL-адрес авторизации
    print(text)
    print(auth_url)


def get_access_token(config):
    client_id = config['client_id']
    client_secret = config['client_secret']
    code = input("Please enter the code that you received as a result of authorization, it is in the search bar after 'code=':")
    url = "https://api.pinterest.com/v5/oauth/token"
    auth_string = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
      'grant_type': 'authorization_code',
      'code': f'{code}',
      'redirect_uri': 'http://localhost:8085'
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


def get_board(token):
    # Replace the following values with your own
    url = "https://api.pinterest.com/v5/boards"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    json_response = response.json()

    for item in json_response["items"]:
        name = item["name"]
        id = item["id"]
        owner = item["owner"]["username"]

        # Create a directory with the owner's name if it doesn't exist
        if not os.path.exists(f"accounts/{owner}/content"):
            os.makedirs(f"accounts/{owner}/content")

        # Add the board to a dictionary
        all_boards = {}
        if os.path.exists(f"accounts/{owner}/board_id.json"):
            with open(f"accounts/{owner}/board_id.json", 'r') as f:
                all_boards = json.load(f)

        all_boards[id] = {"board_name": name}

        # Create a JSON file with the board_id and all boards
        with open(f"accounts/{owner}/board_id.json", 'w') as f:
            json.dump(all_boards, f, indent=4)

        if not os.path.exists(f"accounts/{owner}/hashtag.txt"):
            create_file(f"accounts/{owner}/hashtag.txt", '#hashtag')

        if not os.path.exists(f"accounts/{owner}/keywords.txt"):
            create_file(f"accounts/{owner}/keywords.txt", 'keywords')

        if not os.path.exists(f"accounts/{owner}/description.txt"):
            create_file(f"accounts/{owner}/description.txt", 'description')

        if not os.path.exists(f'accounts/{owner}/access_token.txt'):
            with open(f'accounts/{owner}/access_token.txt', 'w') as f:
                f.write(token)

        default_proxy_data = {
            "proxy_host": "196.19.180.20",
            "proxy_port": "8000",
            "proxy_username": "username",
            "proxy_password": "password"
        }

        # Создаем файл proxy.json и записываем в него дефолтные параметры
        if not os.path.exists(f'accounts/{owner}/proxy.json'):
            with open(f'accounts/{owner}/proxy.json', 'w') as f:
                json.dump(default_proxy_data, f)
def create_file(filename, content):
    with open(filename, 'w') as f:
        for _ in range(3):
            f.write(content + '\n')


if __name__=="__main__":
    OAuth(get_config())
    get_board(get_access_token(get_config()))

