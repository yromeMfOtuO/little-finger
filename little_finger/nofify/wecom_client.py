"""
通过企微实现微信通知，

需要注册企微企业获取企业id，创建应用获取应用 id 和 secret，
通过企业 id 和 应用secret 获取 access_token，
通过 access_token 和 应用id 请求企微开放 api，

微信绑定企微后消息可以同步发送至企微和微信

TIPS:
    1. access_token 是应用维度而不是企业维度
    2. 注意部分消息类型不支持在微信上查看
    3. 图片 音频 视频 文件 等媒体消息，需要先 上传临时素材 再使用 素材id 作为消息参数发送
"""
import enum
import json
import os

from typing import List
import requests
from requests_toolbelt import MultipartEncoder


class WecomConfig:
    """
    企微配置类
    """

    class WecomAppConfig:
        """
        企微应用配置类
        """

        def __init__(self, app_id: int, app_secret: str):
            self.app_id = app_id
            self.app_secret = app_secret
            self.access_token = None

    def __init__(self, corp_id: str, apps: List[WecomAppConfig]):
        self.corp_id = corp_id
        self.apps = apps


class MediaType(enum.Enum):
    """媒体类型"""

    IMAGE = ('image',)
    VOICE = ('voice',)
    VIDEO = ('video',)
    FILE = ('file',)


class WecomClient:
    """
    企微 api 客户端
    """

    host = "https://qyapi.weixin.qq.com"

    bpath = f"{host}/cgi-bin"

    def __init__(self, config: WecomConfig):
        if config is None:
            raise Exception('获取企微配置失败')
        self.config = config
        self.app_index = {app.app_id: app for app in config.apps}
        self.refresh_token()

    def get_corp_id(self) -> str:
        """
        获取企业 id
        :return: corp_id
        """
        return self.config.corp_id

    def get_access_token(self, app_id: int):
        """
        根据应用 id 获取对应 access_token
        :param app_id: 应用 id
        :return: access_token
        """
        if app_id not in self.app_index:
            raise Exception("非法应用id")
        return self.app_index.get(app_id).access_token

    def refresh_token(self):
        """
        获取 应用access_token，作为后续接口请求的凭证
        :return: None
        """
        for app in self.config.apps:
            resp = requests.get(
                f"{self.bpath}/gettoken",
                params=[
                    ("corpid", self.get_corp_id()),
                    ("corpsecret", app.app_secret)
                ]
            )
            app.access_token = resp.json()['access_token']

    def send(self, app_id, data):
        """发送消息"""
        resp = requests.post(
            f'{self.bpath}/message/send',
            params=[
                ("access_token", self.get_access_token(app_id))
            ],
            data=json.dumps(data)
        )
        print(resp.json())

    def upload(self, app_id: int, media_type: MediaType, media_path: str, media_name: str) -> str:
        """
        上传临时素材
        client.upload(
            1000002,
            MediaType.IMAGE,
            '/Users/weihao.lv/Desktop/壁纸/表情包',
            'WX20210701-153912@2x.png'
        )

        TIPS：
            1. 素材上传得到media_id，该media_id仅三天内有效
            2. media_id在同一企业内应用之间可以共享
        :param app_id: 应用 id
        :param media_type: 媒体类型
        :param media_name: 媒体文件名
        :param media_path: 媒体文件路径
        :return: 临时素材 id
        """

        full_path = (media_path if media_path.endswith(os.sep) else (media_path + os.sep)) + media_name
        with open(full_path, 'rb') as media:
            data = MultipartEncoder(
                fields={media_name: ('file', media, 'text/plain')},
            )
            print(data)
            resp = requests.post(
                url=f"{self.bpath}/media/upload",
                params=[
                    ("access_token", self.get_access_token(app_id)),
                    ("type", media_type.value[0])
                ],
                headers={'Content-Type': data.content_type},
                data=data
            )
            print(resp.json())
            return resp.json()['media_id']

    def send_text(self, app_id: int, user_ids: List[str], content: str,
                  part_ids: List[str] = None, tag_ids: List[str] = None):
        """
        发送文本消息
        :param user_ids: 企微中的 成员id 列表
        :param app_id: 发送消息的 应用id
        :param content: 发送的文本消息内容
        :param part_ids: 部门 id 列表
        :param tag_ids: 标签 id 列表
        :return: none
        """
        data = {
            # 接受消息用户列表，为”@all”标示所有人
            "touser": "|".join(user_ids),
            # 部门ID列表，多个接收者用‘|’分隔，最多支持100个，当touser为”@all”时忽略
            "toparty": "|".join(part_ids) if part_ids else None,
            # 标签ID列表，多个接收者用‘|’分隔，最多支持100个，当touser为”@all”时忽略
            "totag": "|".join(tag_ids) if tag_ids else None,
            "msgtype": "text",
            "agentid": app_id,
            "text": {
                "content": content
            },
            "safe": 0
        }
        self.send(app_id, data)

    def send_md(self, app_id: int, user_ids: List[str], content: str,
                part_ids: List[str] = None, tag_ids: List[str] = None):
        """
        发送文本消息
        :param app_id: 发送消息的 应用id
        :param user_ids: 企微中的 成员id 列表
        :param content: 发送的文本消息内容
        :param part_ids: 部门 id 列表
        :param tag_ids: 标签 id 列表
        :return: none
        """
        data = {
            # 接受消息用户列表，为”@all”标示所有人
            "touser": "|".join(user_ids),
            # 部门ID列表，多个接收者用‘|’分隔，最多支持100个，当touser为”@all”时忽略
            "toparty": "|".join(part_ids) if part_ids else None,
            # 标签ID列表，多个接收者用‘|’分隔，最多支持100个，当touser为”@all”时忽略
            "totag": "|".join(tag_ids) if tag_ids else None,
            "msgtype": "markdown",
            "agentid": app_id,
            "markdown": {
                "content": content
            },
            "enable_duplicate_check": 1,  # 标示开启重复消息检查
            "duplicate_check_interval": 1800  # 标示在时间间隔内不会收到重复消息
        }
        self.send(app_id, data)

    def send_media(self, app_id: int, user_ids: List[str],
                   media_type: MediaType, media_path: str, media_name: str,
                   part_ids: List[str] = None, tag_ids: List[str] = None):
        """
        发送媒体消息：1.上传临时素材获取素材 id 2.发送消息
        client.send_media(
            1000002,
            ['weihao.lv'],
            MediaType.IMAGE,
            '/Users/weihao.lv/Desktop/壁纸/表情包',
            'WX20210701-153912@2x.png'
        )

        :param app_id: 发送消息的 应用id
        :param user_ids: 企微中的 成员id 列表
        :param media_type: 媒体类型
        :param media_path: 媒体文件路径
        :param media_name: 媒体文件名
        :param part_ids: 部门 id 列表
        :param tag_ids: 标签 id 列表
        :return: none
        """
        media_id = self.upload(app_id, media_type, media_path, media_name)

        data = {
            # 接受消息用户列表，为”@all”标示所有人
            "touser": "|".join(user_ids),
            # 部门ID列表，多个接收者用‘|’分隔，最多支持100个，当touser为”@all”时忽略
            "toparty": "|".join(part_ids) if part_ids else None,
            # 标签ID列表，多个接收者用‘|’分隔，最多支持100个，当touser为”@all”时忽略
            "totag": "|".join(tag_ids) if tag_ids else None,
            "msgtype": media_type.value[0],
            "agentid": app_id,
            media_type.value[0]: {
                "media_id": media_id,
                "title": "Title",
                "description": "Description"
            },
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        self.send(app_id, data)


if __name__ == '__main__':
    config_ = WecomConfig(
        'corp_id',
        [
            WecomConfig.WecomAppConfig(
                1000002,
                'app_secret'
            )
        ]
    )

    client = WecomClient(config_)
    client.send('user_id', 1000002, 'multi app client test')
