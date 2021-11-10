"""
通过企微实现微信通知，

需要注册企微企业获取企业id，创建应用获取应用 id 和 secret，
通过企业 id 和 应用secret 获取 access_token，tips: access_token 是应用维度而不是企业维度
通过 access_token 和 应用id 请求企微开放 api，

微信绑定企微后消息可以同步发送至企微和微信
"""
import json

import requests


class WecomClient:
    """
    企微 api 客户端
    """

    host = "https://qyapi.weixin.qq.com"

    bpath = f"{host}/cgi-bin"

    def __init__(self, config: dict):
        if config is None:
            raise Exception('获取企微配置失败')
        self.corp_id = config['corpid']
        self.corp_secret = config['corpsecret']
        self.access_token = self.get_token()

    def get_token(self):
        """
        获取 access_token，作为后续接口请求的凭证
        :return: access_token
        """
        resp = requests.get(
            f"{WecomClient.bpath}/gettoken",
            params=[
                ("corpid", self.corp_id),
                ("corpsecret", self.corp_secret)
            ]
        )
        return resp.json()['access_token']

    def send(self, user_id, app_id, content):
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
                ('access_token', self.access_token)
            ],
            data=json.dumps(data)
        )
        print(resp.json())


if __name__ == '__main__':
    config_ = {
        "corpid": '<>',
        "corpsecret": '<>'
    }
    client = WecomClient(config_)
    client.send('userid', 1000002, 'wecom client test')
