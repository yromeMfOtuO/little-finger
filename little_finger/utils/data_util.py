"""
数据读写操作，主要包含 csv ， excel
"""

import json
import pandas as pd
import numpy as np


class NpEncoder(json.JSONEncoder):
    """
    用于 pandas numpy 导出的数据 转换成 json的 encoder
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def convert_data_file_2_list(path: str, read_method, sheet_name=None, fill_merged_cell=True) -> list:
    """
    从数据文件读取数据，转换为 list
    :param path: 数据文件路径
    :param read_method: 读取方法，例：pd.read_excel
    :param sheet_name: sheet 名
    :param fill_merged_cell: 是否填充合并的单元格，默认需要
    :return: 数据列表 list[dict]
    """
    if read_method == pd.read_excel and sheet_name:
        df = read_method(path, sheet_name=sheet_name)
    else:
        df = read_method(path)
    # 填充合并的单元格
    if fill_merged_cell:
        df = df.fillna(method='pad')
    df_list = []
    for i in df.index.values:
        # loc为按列名索引 iloc 为按位置索引，使用的是 [[行号], [列名]]
        df_line = df.loc[i].to_dict()
        # 将每一行转换成字典后添加到列表
        df_list.append(df_line)
    return df_list


def covert_excel_list(path: str, sheet_name=None, fill_merged_cell=True) -> list:
    """
    pandas 读取 excel 内容转换为 List
    :param path: 数据文件路径
    :param sheet_name: sheet 名
    :param fill_merged_cell: 是否填充合并的单元格，默认需要
    :return: 数据列表 list[dict]
    """
    return convert_data_file_2_list(path, pd.read_excel, sheet_name=sheet_name, fill_merged_cell=fill_merged_cell)


def convert_csv_list(path: str) -> list:
    """
    pandas 读取 csv 内容转换为 list
    :param path: 数据文件路径
    :return: 数据列表 list[dict]
    """
    return convert_data_file_2_list(path, pd.read_csv)
