"""日期时间工具"""
import json
from datetime import datetime, date

import pytz


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


def format_now_with_zone(zone='Asia/Shanghai'):
    """
    格式化当前时间
    :param zone: 当前时区
    :return: 输出格式 2019-10-23T16:00:00+08:00
    """
    now = datetime.now(pytz.timezone(zone))
    offset = now.utcoffset()
    # 将时区偏移格式化为+08:00形式
    offset_str = "{:+03}:{:02}".format(offset.seconds // 3600, (offset.seconds // 60) % 60)
    # 输出带时区偏移的时间
    formatted_time = now.strftime('%Y-%m-%dT%H:%M:%S') + "" + offset_str
    return formatted_time


def format_now():
    """
    格式化当前时间
    :return: 输出格式 2019-10-23 16:00:00
    """
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')
