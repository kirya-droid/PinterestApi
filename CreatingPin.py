import base64
import requests
import json

class PinterestPinCreator:
    def __init__(self, token, use_proxy=False):
        self.token = token
        self.use_proxy = use_proxy
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _request(self, method, url, data=None, files=None):
        if self.use_proxy:
            proxies = self.proxy()
            if method == 'GET':
                response = requests.get(url, headers=self.headers, proxies=proxies)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, data=json.dumps(data), files=files, proxies=proxies)
            else:
                raise ValueError("Unsupported method")
        else:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, data=json.dumps(data), files=files)
            else:
                raise ValueError("Unsupported method")

        return response.json()

    def create_pin(self, board_id, description, title, img_url, link):
        url = "https://api.pinterest.com/v5/pins"
        data = {
            "link": link,
            "title": title,
            "description": description,
            "board_id": board_id,
            "media_source": {
                "source_type": "image_url",
                "url": img_url
            }
        }
        return self._request('POST', url, data)

    def create_video_pin(self, title, description, board_id, link, filepath, cover_image):
        # Регистрируем намерение загрузки видео
        data = self.register_intention()

        # Загружаем видео
        self.upload_videofile(filepath, data)

        # Подтверждаем загрузку
        self.confirm_the_download(data)

        # Создаем пин
        status_code = self.post_pin(title, description, board_id, data, link, cover_image)

        return status_code

    def register_intention(self):
        url = 'https://api.pinterest.com/v5/media'
        data = {'media_type': 'video'}
        return self._request('POST', url, data)

    def upload_videofile(self, filepath, response_data):

        url = response_data['upload_url']
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
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, data=data, files=files)
            return response.status_code

    def confirm_the_download(self, response_data):

        media_id = response_data['media_id']

        url = f'https://api.pinterest.com/v5/media/{media_id}'
        return self._request('GET', url)

    def post_pin(self, title, description, board_id, response_data, link, cover_image):
        media_id = response_data['media_id']
        url = 'https://api.pinterest.com/v5/pins'
        data = {
            "link": link,
            "title": title,
            "description": description,
            "board_id": board_id,
            "media_source": {
                "source_type": "video_id",
                "cover_image_content_type": "image/jpeg",
                "cover_image_data": self.encod(cover_image),
                "media_id": media_id
            }
        }
        return self._request('POST', url, data)

    def get_boards(self):
        url = "https://api.pinterest.com/v5/boards"
        return self._request('GET', url)

    def proxy(self):
        return {}

    def encod(self, cover_image):
        with open(cover_image, 'rb') as image_file:
            bs_code = base64.b64encode(image_file.read()).decode('utf-8')
        return bs_code
