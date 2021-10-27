"""
列表操作工具
"""


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
    List 转换成 dict
    :param data: 数据列表
    :param key_column: key 列列名
    :return: str(key) -> datum
    """
    # return {i[key_column]: i for i in data} # 列表展开式实现
    result = {}
    for i in data:
        result[str(i[key_column])] = i
    return result
