"""
日志读取相关，主要用于从日志中提取返回字符串
"""

import json
import re


class LogReaderV2:
    """
    日志读取，需要从kibana控制台获取的日志查询结果response json，保存到的 .json 文件中
    """

    @staticmethod
    def read_log_from_json_v2(log_path='log.json',
                              log_list_func=lambda x: x['rawResponse']['hits']['hits'],
                              log_text_func=lambda x: x['_source']['message'],
                              filter_func=lambda x: x,
                              reg_func=lambda x: x,
                              single_convert_func=lambda x: x,
                              total_convert_func=lambda x: x):
        """
        这里的取值 key 与kibana 的日志格式有关，日志格式不同则不适用
        :param log_path: 日志 json 文件路径
        :param log_list_func: 获取日志 json 中日志条目 list 的函数
        :param log_text_func: 获取日志条目中 日志文本 的函数
        :param filter_func: 日志过滤函数，用于过滤在 kibana 中不方便过滤的日志
        :param reg_func: 日志截取匹配函数，用于在日志中截取或者匹配到需要的 数据 json
        :param single_convert_func: 单条数据转换函数 例如 json.loads()
        :param total_convert_func: 整体数据转换函数
        :return: 数据列表
        """
        if log_path.__contains__('.json') is False:
            return []
        with open(log_path) as f:
            load_ = json.load(f)
            hits_ = log_list_func(load_)
            # 过滤日志
            logs = list(filter(filter_func, hits_))
            log_sources = list(map(log_text_func, logs))
            # 日志内容匹配
            data = list(map(single_convert_func, map(reg_func, log_sources)))
            return total_convert_func(data)

    @staticmethod
    def filter_func_by_contains_v2(content: str, log_text_func=lambda x: x['_source']['message']):
        """
        通过包含关系过滤，结果必须包含 给出的字符串

        :param content: 被包含的字符串
        :param log_text_func: 从日志条目对象中获取日志文本
        :return: 筛选 lambda 参数
        """
        return lambda x: log_text_func(x).__contains__(content)
