"""
通过 ifttt 实现手机通知，依赖 ifttt 网站及 app 实现推送通知到手机 ifttt app。需要注册 ifttt 并配置 action, 并安装手机 app 登录。
依然没有微信通知方便~
"""

import json
import requests


class IftttClient:
    """
    ifttt 请求封装 client
    """

    host = "https://maker.ifttt.com"

    def __init__(self, config):
        """
        初始化，通过 event 和 key 绑定一个唯一的 action trigger
        """
        if config is None:
            raise Exception('获取ifttt配置失败')
        self.event = config['event']
        self.key = config['key']

    def notify(self, **kwargs):
        """
        发送通知：
            请求 trigger 接口 -> 获取 action -> 发送对应 app 账户通知
        """
        url_ = f"{IftttClient.host}/trigger/{self.event}/with/key/{self.key}"
        headers_ = {
            'Content-Type': 'application/json'
        }
        payload = {
            "value1": kwargs['content'] if 'content' in kwargs else None,
            "value2": kwargs['sender'] if 'sender' in kwargs else None,
        }
        resp = requests.post(url_, data=json.dumps(payload), headers=headers_)
        print(resp.text)


if __name__ == '__main__':
    client = IftttClient({
        "event": "",
        "key": ""
    })
    client.notify(content="""
test content
    """)
