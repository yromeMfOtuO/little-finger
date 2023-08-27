"""
dict util
"""


def values(data: dict) -> list:
    """
    获取字典的值
    :param data: 字典
    :return: 值列表
    """
    return list(data.values())


def keys(data: dict) -> list:
    """
    获取字典的键
    :param data: 字典
    :return: 键列表
    """
    return list(data.keys())


def filter_by_key(data: dict, key_filter_func) -> dict:
    """
    根据 key 过滤字典
    :param data: 字典
    :param key_filter_func: key 过滤函数
    :return: 过滤后的字典
    """
    return {k: v for k, v in data.items() if key_filter_func(k)}


def filter_by_value(data: dict, value_filter_func) -> dict:
    """
    根据 value 过滤字典
    :param data: 字典
    :param value_filter_func: value 过滤函数
    :return: 过滤后的字典
    """
    return {k: v for k, v in data.items() if value_filter_func(v)}
