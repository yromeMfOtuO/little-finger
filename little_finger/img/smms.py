"""
sm.ms 图床
"""

import requests

from little_finger.utils import check_flag, check_flag_export_data, check_status


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
        data = check_flag_export_data(resp, err_msg="获取token请求异常")
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
        check_flag_export_data(resp)

    def upload_online_img(self, img_url: str, img_name: str = None):
        """
        upload online img
        :param img_url: img url
        :param img_name: img name if None will parse from url
        """
        respd = requests.get(img_url)
        check_status(respd)
        print(respd)
        # img_name = img_name if img_name else img_url.split('/')[-1]
        respu = requests.post(
            url=self.host + '/upload',
            files={
                # TODO
                # 这里上传之后 smfile被当作了文件名，但是不使用smfile作为key会导致上传失败，目前可能只能先保存图片再上传可以解决
                # 获取直接代码生成markdown图片链接，添加图片名
                'smfile': respd.content
            },
            headers=self.headers,
        )
        return check_flag_export_data(respu)

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
        '4b7d21ec3fdaf5d613941b37968ffb534cf48577'  # pragma: allowlist secret
    )
    # r = client.upload_img('image_path')
    # print(r)
    # client.delete_img("hash")
    # imgs = client.upload_history()
    # print(imgs)
    client.upload_online_img("http://tupian.qqjay.com/u/2016/0919/1_171052_5.jpg")
