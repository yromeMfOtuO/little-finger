"""
sm.ms 图床
"""
import json

import requests


class SMMSClient:

    host = 'https://sm.ms/api/v2'

    def __init__(self, username: str, passwd: str):
        self.username = username
        self.passwd = passwd
        self.token = self.get_token()

    def get_token(self):
        resp = requests.post(
            url=self.host + '/token',
            data={'username': self.username, 'password': self.passwd}
        )
        result = resp.json()
        print(result)
        if not result:
            raise Exception('获取token请求异常')
        if not result['success']:
            raise Exception('获取token失败：%s' % result['message'])
        return result['data']['token']

    def upload_img(self, img_path: str):
        headers = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': self.token
        }
        # requests 对form-data支持不友好，
        # 1. 可以通过手动构建字符串payload通过data参数传递
        # 2. 通过files参数传递，这里上传文件，适合用files参数传递
        files = {
            'smfile': open(img_path, 'rb')
        }
        resp = requests.post(
            url=self.host + '/upload',
            files=files,
            headers=headers
        )
        result = resp.json()
        print(result)
        if not result:
            raise Exception('上传图片请求异常')
        if not result['success']:
            raise Exception('上传图片失败：%s' % result['message'])
        return result['data']


if __name__ == '__main__':
    client = SMMSClient('username', 'password')
    r = client.upload_img('image path')
    print(r)