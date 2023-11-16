import subprocess
import base64
import os
import time


def cover(owner,file_name):
    video_input_path = f'accounts/{owner}/content/{file_name}'
    img_output_path = f'accounts/{owner}/content/image.jpg'
    print("creating a cover...")
    result = subprocess.run(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path], check=True)


def encod(owner):
    with open(f'accounts/{owner}/content/image.jpg', 'rb') as image_file:
        bs_code = base64.b64encode(image_file.read()).decode('utf-8')
    os.remove(f'accounts/{owner}/content/image.jpg')
    return bs_code
