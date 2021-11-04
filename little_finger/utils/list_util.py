"""
列表操作工具
"""

from operator import itemgetter
from itertools import groupby

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


if __name__ == '__main__':
    d = {"name": "weihao.lv", "age": 1}
    print(itemgetter("name")(d))
