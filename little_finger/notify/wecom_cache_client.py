"""文件缓存企微 access_token"""

import datetime
import json

import requests

from little_finger.cache import RedisClient
from little_finger.logg import logger
from little_finger.notify import WecomClient, WecomConfig


class WecomFileCacheClient(WecomClient):
    """通过文件缓存 access_token"""

    def refresh_token(self):
        """
        获取 应用access_token，作为后续接口请求的凭证
        :return: None
        """
        logger.info('access token refresh by file cache client')
        with open(f'wecom_cache_{self.config.corp_id}.json', 'r+') as f:
            config = f.read()
            if config:
                self.config = WecomConfig.decode(json.loads(config))

            if not filter(lambda x: x.expire_time < datetime.datetime.now(), self.config.apps):
                for app in self.config.apps:
                    resp = requests.get(
                        f"{self.bpath}/gettoken",
                        params=[
                            ("corpid", self.get_corp_id()),
                            ("corpsecret", app.app_secret)
                        ]
                    )
                    app.access_token = resp.json()['access_token']
                    app.expire_time = \
                        datetime.datetime.now() + datetime.timedelta(seconds=int(resp.json()['expires_in']))
                json.dump(self.config, f, cls=WecomConfig.Encoder)
                f.flush()
        self.app_index = {app.app_id: app for app in self.config.apps}

    def get_access_token(self, app_id: int):
        """
        获取 access token，若已失效则重新刷新获取
        :param app_id: 应用 id
        :return: access_token
        """
        if app_id not in self.app_index:
            logger.error("illegal appid %d", app_id)
            raise Exception("非法应用id")
        app = self.app_index.get(app_id)
        if app.expire_time < datetime.datetime.now():
            logger.info("get access token: %s by appid: %d", app.access_token, app_id)
            return app.access_token
        self.refresh_token()
        return self.get_access_token(app_id)


class WecomRedisCacheClient(WecomClient):
    """通过 redis 缓存access_token"""

    def __init__(self, config: WecomConfig, redis_client: RedisClient):
        self.redis_client = redis_client
        super().__init__(config)

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
            self.redis_client.set_ex(app.access_token, '1', int(resp.json()['expires_in']))

    def get_access_token(self, app_id: int):
        """
        获取 access token，若已失效则重新刷新获取
        :param app_id: 应用 id
        :return: access_token
        """
        if app_id not in self.app_index:
            logger.error("illegal appid %d", app_id)
            raise Exception("非法应用id")
        access_token = self.app_index.get(app_id).access_token
        # 未失效直接返回
        if self.redis_client.get(access_token):
            return access_token
        # 已失效后刷新重新获取
        self.refresh_token()
        return self.get_access_token(app_id)


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

    client = WecomFileCacheClient(config_)
    client.get_access_token(1000002)
