"""
用于从 csv excel 日志等中提取数据，并根据指定的 key 列 对指定的 value 列进行比较，打印比较结果
"""

import json
from typing import List

from little_finger.utils.list_util import flatten
from little_finger.utils.list_util import convert_list_2_dict
from little_finger.utils.data_util import convert_csv_list
from little_finger.utils.data_util import covert_excel_list
from little_finger.log_reader import LogReader


def convert_dict(path, key_column) -> dict:
    """
    读取数据并转换为 dict
    :param path: 数据文件 path
    :param key_column: 作为key的列名
    :return:
    """
    data = {}
    if path.__contains__('.xls'):
        data = covert_excel_list(path)
    elif path.__contains__('.csv'):
        data = convert_csv_list(path)
    elif path.__contains__('.json'):
        data = LogReader.read_log_from_json(
            path,
            LogReader.filter_method_by_contains('<--response start'),
            LogReader.reg_method_by_regex('body:(.*?),tookMs', 1),
            lambda x: json.loads(x)['dataList'],
            flatten
        )
    return convert_list_2_dict(data, key_column)


def compare_raw(key, left_raw, right_raw, compare_column) -> None:
    """
    比较单条数据
    :param key: key 列名
    :param left_raw: 单条数据
    :param right_raw: 单条数据
    :param compare_column: 需要比较的列名
    :return: None
    """
    # print("--------------------------------------")
    for t in compare_column:
        left_val = left_raw[t[0]]
        right_val = right_raw[t[1]]
        if left_val != right_val:
            print(f"key = {key}, {t[0]} = {left_val} 与 {t[1]} = {right_val}不匹配")
        else:
            print(f"数据一致, key = {key}, left = {left_val}, right = {right_val}")


def compare_data(left_dict, right_dict, compare_column) -> None:
    """
    比较一组数据
    :param left_dict: key -> datum
    :param right_dict: key -> datum
    :param compare_column: 需要比较的列名
    :return: None
    """
    print("以左边为准比较是否一致")
    for key, left_raw in left_dict.items():
        if key not in right_dict:
            print(f"右边数据 key = {key} 不存在")
            continue
        right_raw = right_dict[key]
        compare_raw(key, left_raw, right_raw, compare_column)

    print("以右边为准比较是否存在")
    for key, _ in right_dict.items():
        if key not in left_dict:
            print(f"左边数据 key = {key} 不存在")
    ...


def compare(left_path: str, right_path: str, relate_column: List[str], compare_column: str) -> None:
    """
    比较数据
    :param left_path: 数据文件路径
    :param right_path: 数据文件路径
    :param relate_column: 关联的列 key 列名列表
    :param compare_column: 需要比较的列名
    :return: None
    """
    # left_dict = convert_map(left_path, map(lambda x: x[0], relate_column))
    # right_dict = convert_map(right_path, map(lambda x: x[0], relate_column))
    left_dict = convert_dict(left_path, relate_column[0])
    right_dict = convert_dict(right_path, relate_column[1])

    compare_data(left_dict, right_dict, compare_column)


if __name__ == '__main__':
    # compare('XingRen_Data.csv', 'yinte.xlsx', ('skuId', 'interface_code'), [('totalRemaining', 'stock')])
    # read_from_json()
    # compare('XingRen_Data.csv', 'log.json', ('skuId', 'code'), [('totalRemaining', 'stock')])
    # compare('XingRen_Data.csv', 'XingRen_Data2.csv', ('skuId', 'skuId'), [('totalRemaining', 'totalRemaining')])

    # l1 = LogReader.read_log_from_json(
    #     'message_log.json',
    #     LogReader.filter_method_by_contains('收到西药服务推送的消息，但是渠道不是企杏大药房下渠道，message: '),
    #     LogReader.reg_method_by_split('收到西药服务推送的消息，但是渠道不是企杏大药房下渠道，message: ', 1),
    #     json.loads
    # )
    ...
