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
from datetime import datetime, date
from typing import List

import requests
from requests_toolbelt import MultipartEncoder

from little_finger.logg import logger
from little_finger.utils import date_util


class WecomConfig:
    """
    企微配置类
    """

    class WecomAppConfig:
        """
        企微应用配置类
        """

        def __init__(self, app_id: int, app_secret: str,
                     access_token: str = None, expire_time: datetime = None):
            self.app_id = app_id
            self.app_secret = app_secret
            self.access_token = access_token
            self.expire_time = expire_time

        @classmethod
        def decode(cls, json_array: List[dict]):
            """decode"""
            if not json_array:
                return []
            return [
                cls(
                    app_id=i['app_id'],
                    app_secret=i['app_secret'],
                    access_token=i['access_token'],
                    expire_time=date_util.unserialize(i['expire_time'])
                ) for i in json_array
            ]

    def __init__(self, corp_id: str, apps: List[WecomAppConfig]):
        self.corp_id = corp_id
        self.apps = apps

    class Encoder(json.JSONEncoder):
        """json 序列化时间"""

        def default(self, o):
            if isinstance(o, datetime):
                return o.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(o, date):
                return o.strftime('%Y-%m-%d')
            if isinstance(o, WecomConfig):
                return o.__dict__
            if isinstance(o, WecomConfig.WecomAppConfig):
                return o.__dict__
            return json.JSONEncoder.default(self, o)

    @classmethod
    def decode(cls, json_obj: dict):
        """decode"""
        if not json_obj:
            return None
        return cls(
            corp_id=json_obj['corp_id'],
            apps=WecomConfig.WecomAppConfig.decode(json_obj['apps'])
        )


class MediaType(enum.Enum):
    """媒体类型"""

    IMAGE = ('image',)
    VOICE = ('voice',)
    VIDEO = ('video',)
    FILE = ('file',)


class Article:
    """文章"""
    def __init__(self, title: str, desc: str, pic_url: str, url: str,
                 app_id: str = None, page_path: str = None):
        self.title = title  # 文章标题
        self.description = desc # 文章描述，副标题，TIPS：一次发送多篇文章时不展示
        self.picurl = pic_url   # 文章头图链接，可以使用企微文件上传接口获取，也可来自外部
        self.url = url  # 文章跳转 url
        self.appid = app_id # 文章跳转 appid，TIPS：当前企微应用未绑定则不填，否则企微校验不通过
        self.pagepath = page_path   # 文章跳转 app pagepath，TIPS：当前企微应用未绑定则不填，否则企微校验不通过
        ...


class WecomClient:
    """
    企微 api 客户端
    """

    host = "https://qyapi.weixin.qq.com"

    bpath = f"{host}/cgi-bin"

    def __init__(self, config: WecomConfig):
        if config is None:
            logger.error('wecom config empty')
            raise Exception('企微配置为空')
        self.config = config
        self.app_index = None
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
            logger.error("illegal appid %d", app_id)
            raise Exception("非法应用id")
        token = self.app_index.get(app_id).access_token
        logger.info("get access token: %s by appid: %d", token, app_id)
        return token

    def refresh_token(self):
        """
        获取 应用access_token，作为后续接口请求的凭证
        :return: None
        """
        logger.info('access token refresh by simple client')
        for app in self.config.apps:
            resp = requests.get(
                f"{self.bpath}/gettoken",
                params=[
                    ("corpid", self.get_corp_id()),
                    ("corpsecret", app.app_secret)
                ]
            )
            app.access_token = resp.json()['access_token']
        self.app_index = {app.app_id: app for app in self.config.apps}

    def send(self, app_id, data):
        """发送消息"""
        data = json.dumps(data, default=lambda obj: obj.__dict__)
        logger.info('send to appid: %d, message: %s', app_id, data)
        resp = requests.post(
            f'{self.bpath}/message/send',
            params=[
                ("access_token", self.get_access_token(app_id))
            ],
            data=data
        )
        logger.info('send to appid: %d, message: %s, resp: %s', app_id, data, resp.text)
        # print(resp.json())

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
                   media_type: MediaType, media_path: str, media_name: str, title: str = None, desc: str = None,
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
        :param title: 媒体标题，仅视频消息有效
        :param desc: 媒体描述，仅视频消息有效
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
                "title": title,
                "description": desc
            },
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        self.send(app_id, data)

    def send_textcard(self, app_id: int, user_ids: List[str],
                      title: str, desc: str, url: str, btntxt: str = '详情',
                      part_ids: List[str] = None, tag_ids: List[str] = None):
        """
        发送文本卡片消息，示例：
        client.send_textcard(
            1000002,
            ['weihao.lv'],
            '领奖通知',
            '<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">恭喜你抽中iPhone 7一台，领奖码：xxxx</div>'
            '<div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>',
            'https://baidu.com'
        )

        TIPS：
            1. 文本卡片描述中的高亮等在同步微信时不支持，只能作无效果的文本显示
            2. 卡片下方的按钮在微信中也不支持，不作显示

        :param app_id: 发送消息的 应用id
        :param user_ids: 企微中的 成员id 列表
        :param title: 媒体标题，仅视频消息有效
        :param desc: 媒体描述，仅视频消息有效
        :param url: 点击卡片跳转的链接
        :param btntxt: 按钮文字
        :param part_ids: 部门 id 列表
        :param tag_ids: 标签 id 列表
        :return: none
        """
        data = {
            "touser": "|".join(user_ids),
            "toparty": "|".join(part_ids) if part_ids else None,
            "totag": "|".join(tag_ids) if tag_ids else None,
            "msgtype": "textcard",
            "agentid": app_id,
            "textcard": {
                "title": title,
                "description": desc,
                "url": url,
                "btntxt": btntxt
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }

        self.send(1000002, data)

    def send_articles(self, app_id: int, user_ids: List[str], articles: List[Article],
                      part_ids: List[str] = None, tag_ids: List[str] = None):
        """
        发送图文文章消息，示例：
        client.send_articles(
            1000002,
            ['weihao.lv'],
            [
                Article(
                    "触发续方通知推送",
                    "触发续方通知推送.png",
                    "https://i.loli.net/2021/08/31/3GawtLKV2XMNzgx.png",
                    "https://sm.ms/image/3GawtLKV2XMNzgx"
                ),
                Article(
                    "推送策略类图v2",
                    "推送策略类图v2.png",
                    "https://i.loli.net/2021/08/31/42e81J6oEN7CZ39.png",
                    "https://sm.ms/image/42e81J6oEN7CZ39"
                )
            ]
        )

        :param app_id: 发送消息的 应用id
        :param user_ids: 企微中的 成员id 列表
        :param articles: 文章列表
        :param part_ids: 部门 id 列表
        :param tag_ids: 标签 id 列表
        :return: none
        """
        data = {
            "touser": "|".join(user_ids),
            "toparty": "|".join(part_ids) if part_ids else None,
            "totag": "|".join(tag_ids) if tag_ids else None,
            "msgtype": "news",
            "agentid": app_id,
            "news": {
                "articles": articles
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        self.send(1000002, data)


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
    client.send_text(1000002, ['user_id'], 'multi app client test')
