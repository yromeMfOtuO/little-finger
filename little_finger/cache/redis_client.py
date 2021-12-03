"""redis 客户端"""
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

    def set(self, key: str, value: str):
        """set"""
        self.conn.set(key, value)

    def setex(self, key: str, value: str, time: int):
        """set with expire time"""
        self.conn.setex(key, time, value)

    def get(self, key: str):
        """get"""
        return self.conn.get(key)


if __name__ == '__main__':
    client = RedisClient(host='<host>', password='<passwd>')
    client.setex('name', 'weihao.lv', 10)
    print(client.get('name'))
    print(client.get('name'))
