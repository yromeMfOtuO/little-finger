"""
数据读写操作，主要包含 csv ， excel
"""

import pandas as pd


def convert_data_file_2_list(path: str, read_method) -> list:
    """
    从数据文件读取数据，转换为 list
    :param path: 数据文件路径
    :param read_method: 读取方法，例：pd.read_excel
    :return: 数据列表 list[dict]
    """
    df = read_method(path)
    df_list = []
    for i in df.index.values:
        # loc为按列名索引 iloc 为按位置索引，使用的是 [[行号], [列名]]
        df_line = df.loc[i].to_dict()
        # 将每一行转换成字典后添加到列表
        df_list.append(df_line)
    return df_list


def covert_excel_list(path: str) -> list:
    """
    pandas 读取 excel 内容转换为 List
    :param path: 数据文件路径
    :return: 数据列表 list[dict]
    """
    return convert_data_file_2_list(path, pd.read_excel)


def convert_csv_list(path: str) -> list:
    """
    pandas 读取 csv 内容转换为 list
    :param path: 数据文件路径
    :return: 数据列表 list[dict]
    """
    return convert_data_file_2_list(path, pd.read_csv)
