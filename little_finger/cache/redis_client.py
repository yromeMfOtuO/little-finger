"""redis 客户端"""
from typing import List

import redis


class RedisClient:
    """redis 客户端"""

    def __init__(self, host: str, port: int = 6379, db: int = 0, password: str = None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.conn = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )

        # 已上传的脚本的索引，名称索引
        self.script_name_index = {}
        # 已上传的脚本的索引，内容索引
        self.script_sha_index = {}

    def set(self, key: str, value: str):
        """set"""
        self.conn.set(key, value)

    def set_ex(self, key: str, value: str, time: int):
        """set with expire time"""
        self.conn.setex(key, time, value)

    def get(self, key: str):
        """get"""
        return self.conn.get(key)

    def upload_script(self, script: str, script_name: str = None):
        """
        上传脚本，方便手续使用 eval_sha 调用
        :param script: 脚本内容
        :param script_name: 脚本名称
        :return: sha
        """
        sha = self.conn.execute_command("SCRIPT", 'LOAD', script, parse='LOAD')
        self.script_sha_index[script] = sha
        if script_name:
            self.script_name_index[script_name] = sha
        return sha

    def exec_script(self, sha: str, script: str, script_name: str, keys: List, args: List):
        """

        :param sha:
        :param script:
        :param script_name:
        :param keys:
        :param args:
        :return:
        """
        if sha:
            if sha not in self.script_sha_index.values():
                raise Exception('illegal script sha')
        if script_name:
            if script_name not in self.script_name_index:
                return Exception('illegal script name')
        if script:
            if script not in self.script_sha_index:
                sha = self.upload_script(script)
            else:
                sha = self.script_sha_index.get(script)
        if not sha:
            raise Exception('illegal script')
        return self.conn.execute_command("EVALSHA", sha, len(keys), *(keys + args))


if __name__ == '__main__':
    client = RedisClient(host='<host>', password='<passwd>')
    client.setex('name', 'weihao.lv', 10)
    print(client.get('name'))
    print(client.get('name'))
