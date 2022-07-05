"""
列表操作工具
"""

from operator import itemgetter
from itertools import groupby
from collections import OrderedDict

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


def convert_list_2_dict(data: list, key_column: str) -> dict:
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


def group_by(data: list, key_column: str) -> Dict[object, list]:
    """
    对 list 依据 key 分组
    :param data: 原始 list
    :param key_column: 用于分组的列名
    :return: 分组数据
    """
    sort_by(data, key_column)
    lgb = groupby(data, itemgetter(key_column))
    return {key: list(group) for key, group in lgb}


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


if __name__ == '__main__':
    print(distinct_by([{"name": 2, "age": 3}, {"name": 2, "age": 2}, {"name": 1, "age": 2}], "name"))
    l = [i for i in range(2)]
    print(split(l, 3))
