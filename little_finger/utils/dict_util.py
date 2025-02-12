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


def get_with_default(data: dict, key, default=None):
    """
    :param data: source data
    :param key: key
    :param default: default value if key not in data
    :return: match item
    """
    if data is None or key not in data:
        return default
    return data[key]


def get(data: dict, key):
    return get_with_default(data, key)


def foreach(data, func):
    """
    :param data: source data
    :param func: func to process key,value
    :return: None
    """
    if func is None:
        return
    for key, value in data.items():
        func(key, value)


if __name__ == '__main__':
    data_i = {
        "1": "a",
        "2": "b",
        "3": "c",
    }

    def func_i(key, value):
        print(f'key:{key}, value:{value}')

    foreach(data_i, func_i)
