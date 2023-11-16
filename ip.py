import requests
import json



def proxy(owner):
    proxy_file_path = f"accounts/{owner}/proxy.json"
    # Загружаем данные прокси из файла
    with open(proxy_file_path, 'r') as f:
        proxy_data = json.load(f)

    # Информация о прокси
    proxy_host = proxy_data["proxy_host"]
    proxy_port = proxy_data["proxy_port"]
    proxy_username = proxy_data["proxy_username"]
    proxy_password = proxy_data["proxy_password"]

    # Создаем строку с информацией о прокси
    proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

    # Создаем словарь с информацией о прокси
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    # Отправляем GET-запрос через прокси
    response = requests.get('http://jsonip.com/', proxies=proxies)

    # Обрабатываем ответ
    data = response.json()

    return proxies