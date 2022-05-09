"""
sm.ms 图床
"""

import requests

from little_finger.utils import check_flag, check_flag_export_data


class SMMSClient:
    """
    SM.MS 客户端，接入图床API：https://doc.sm.ms/
    """

    host = 'https://sm.ms/api/v2'

    def __init__(self, username: str, passwd: str):
        self.username = username
        self.passwd = passwd
        self.token = self.get_token()
        self.headers  = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': self.token
        }

    def get_token(self):
        """
        获取用户token
        """
        resp = requests.post(
            url=self.host + '/token',
            data={'username': self.username, 'password': self.passwd}
        )
        data = check_flag_export_data(resp, "获取token请求异常")
        return data['token']

    def upload_img(self, img_path: str):
        """
        上传本地图片
        :param img_path: 上传图片路径
        :return: 返回数据示例如下
        {
            "file_id": 0,
            "width": 4677,
            "height": 3307,
            "filename": "luo.jpg",
            "storename": "D5VpWCKFElUsPcR.jpg",
            "size": 801933,
            "path": "/2019/12/16/D5VpWCKFElUsPcR.jpg",
            "hash": "Q6vLIbCGZojrMhO2e7BmgFuXRV",
            "url": "https://vip1.loli.net/2019/12/16/D5VpWCKFElUsPcR.jpg",
            "delete": "https://sm.ms/delete/Q6vLIbCGZojrMhO2e7BmgFuXRV",
            "page": "https://sm.ms/image/D5VpWCKFElUsPcR"
        }
        """

        # requests 对form-data支持不友好，
        # 1. 可以通过手动构建字符串payload通过data参数传递
        # 2. 通过files参数传递，这里上传文件，适合用files参数传递
        files = {
            'smfile': open(img_path, 'rb')
        }
        resp = requests.post(
            url=self.host + '/upload',
            files=files,
            headers=self.headers,
        )
        result = resp.json()
        print(result)
        if not result:
            raise Exception('上传图片请求异常')
        if not result['success']:
            raise Exception(f"上传图片失败：{result['message']}")
        return result['data']

    def delete_img(self, img_hash: str):
        """
        delete img by img hashcode which is returned by upload endpoint
        no need to login
        :param img_hash: img hashcode
        """
        resp = requests.get(
            url=self.host + f"/delete/{img_hash}",
        )
        check_flag(resp, f"删除图片失败，hash：{img_hash}")

    def upload_history(self) -> list:
        """
        query upload history
        no page limit
        """
        resp = requests.get(
            url=self.host + "/upload_history",
            headers=self.headers,
        )
        return check_flag_export_data(resp)


if __name__ == '__main__':
    client = SMMSClient(
        'username',
        'password'
    )
    # r = client.upload_img('image_path')
    # print(r)
    # client.delete_img("hash")
    imgs = client.upload_history()
    print(imgs)
