"""日期时间工具"""
import json
from datetime import datetime, date


class DateTimeEncoder(json.JSONEncoder):
    """json 序列化时间"""
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, o)


DEFAULT_FMT = "%Y-%m-%d %H:%M:%S"


def serialize(time: datetime):
    """序列化时间到字符串"""
    return time.strftime(DEFAULT_FMT)


def unserialize(time_str: str):
    """反序列化时间字符串到时间"""
    return datetime.strptime(time_str, DEFAULT_FMT)
