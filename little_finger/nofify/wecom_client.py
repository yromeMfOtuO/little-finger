"""
通过企微实现微信通知，

需要注册企微企业获取企业id，创建应用获取应用 id 和 secret，
通过企业 id 和 应用secret 获取 access_token，tips: access_token 是应用维度而不是企业维度
通过 access_token 和 应用id 请求企微开放 api，

微信绑定企微后消息可以同步发送至企微和微信
"""
import json

from typing import List
import requests


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
                f"{WecomClient.bpath}/gettoken",
                params=[
                    ("corpid", self.get_corp_id()),
                    ("corpsecret", app.app_secret)
                ]
            )
            app.access_token = resp.json()['access_token']

    def send(self, user_id: str, app_id: int, content: str):
        """
        发送消息，暂时只支持文本
        :param user_id: 企微中的 成员id
        :param app_id: 发送消息的 应用id
        :param content: 发送的文本消息内容
        :return: none
        """
        data = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": app_id,
            "text": {
                "content": content
            },
            "safe": 0
        }
        resp = requests.post(
            f'{WecomClient.bpath}/message/send',
            params=[
                ("access_token", self.get_access_token(app_id))
            ],
            data=json.dumps(data)
        )
        print(resp.json())


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
