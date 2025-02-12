"""
列表操作工具
"""
from operator import itemgetter
from itertools import groupby
from collections import OrderedDict, defaultdict

from typing import Dict


def flatten(list_: list) -> list:
    """
    展开 List[List] 为 List
    :param list_: 需要展开的列表
    :return: 展开后平铺的列表
    """
    if isinstance(list_, list):
        return [a for i in list_ for a in flatten(i)]
    return [list_]


def to_dict_by_key_column(data: list, key_column: str) -> dict:
    """
    List 转换成 dict， key 转换成 str
    :param data: 数据列表
    :param key_column: key 列列名
    :return: str(key) -> datum
    """
    # return {i[key_column]: i for i in data} # 列表展开式实现
    result = {}
    for i in data:
        result[str(i[key_column])] = i
    return result


def to_dict_by_key_func(data: list, key_func) -> dict:
    """
    List 转换成 dict， key 转换成 str
    :param data: 数据列表
    :param key_func: key 生成函数
    :return: str(key) -> datum
    """
    # return {i[key_column]: i for i in data} # 列表展开式实现
    return to_dict_by_key_func_value_func(data, key_func, lambda x: x)


def to_dict_by_key_func_value_func(data: list, key_func, value_func) -> dict:
    """
    List 转换成 dict， key 转换成 str
    :param data: 数据列表
    :param key_func: key 生成函数
    :param value_func: value 生成函数
    :return: str(key) -> datum
    """
    # return {i[key_column]: i for i in data} # 列表展开式实现
    result = {}
    for i in data:
        result[key_func(i)] = value_func(i)
    return result


def to_dict(data: list, key: str):
    """
    List 转换成 dict， key 转换成 str
    :param data: data list
    :param key: key column name
    :return:
    """
    return to_dict_by_key_column(data, key)


def sort_by(data: list, key_column: str, reverse=True) -> list:
    """
    列表排序
    :param data: 原始 list
    :param key_column: 用于排序的列名
    :param reverse: 是否反向
    :return: 排序后的 list
    """
    data.sort(key=itemgetter(key_column), reverse=reverse)
    return data


def group_by(data: list, key_column: str) -> dict[object, list]:
    """
    对 list 依据 key 分组
    :param data: 原始 list
    :param key_column: 用于分组的列名
    :return: 分组数据
    """
    sort_by(data, key_column)
    lgb = groupby(data, itemgetter(key_column))
    return {key: list(group) for key, group in lgb}


def group_by_key_func(data: list, key_func) -> dict[object, list]:
    groups = defaultdict(list)

    # 遍历列表中的每个元素
    for item in data:
        # 调用函数 b，获取分组的 key
        key = key_func(item)
        # 将元素添加到对应的分组中
        groups[key].append(item)

    # 将 defaultdict 转换为普通字典并返回
    return dict(groups)


def distinct_by(data: list, key_column: str) -> list:
    """
    根据某一列去重, 保持原有数据顺序
    :param data: 数据列表
    :param key_column: 用于去重的列名
    :return: 去重后的列表
    """
    getter = itemgetter(key_column)
    od = OrderedDict()
    for i in data:
        key = getter(i)
        if key not in od:
            od.setdefault(key, i)
    return list(od.values())


def foreach(func, iterable):
    """
    模拟 foreach
    :param func: 要对每个元素执行的函数
    :param iterable: 可迭代对象
    :return: None
    """
    for i in iterable:
        func(i)


def split(data: list, count: int = 10) -> list:
    """
    将列表切分成固定大小的列表,
    使用步长遍历+列表分片
    :param data: 数据列表
    :param count: 子列表大小
    :return: 子列表列表
    """
    len_ = len(data)
    return [data[i:min(i + count, len_)] for i in range(0, len_, count)]


def filter_by(data: list, func) -> list:
    """
    过滤列表
    :param data: 数据列表
    :param func: 过滤函数
    :return: 过滤后的列表
    """
    return [i for i in data if func(i)]


def map_by(data: list, func) -> list:
    """
    对列表中的每个元素执行函数
    :param data: 数据列表
    :param func: 执行函数
    :return: 执行后的列表
    """
    return [func(i) for i in data]


if __name__ == '__main__':
    print(distinct_by([{"name": 2, "age": 3}, {"name": 2, "age": 2}, {"name": 1, "age": 2}], "name"))
    l = [i for i in range(2)]
    print(split(l, 3))
    print(filter_by([1, 2, 3, 4, 5], lambda x: x > 3))
    print(map_by([1, 2, 3, 4, 5], lambda x: x * 2))
