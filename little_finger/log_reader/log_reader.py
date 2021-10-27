"""
日志读取相关，主要用于从日志中提取返回字符串
"""

import json
import re


class LogReader:
    """
    日志读取，读取从kibana控制台获取的日志查询结果json，保存到的 .json 文件中
    """

    @staticmethod
    def read_log_from_json(log_path='log.json',
                           filter_method=lambda x: x,
                           reg_method=lambda x: x,
                           single_convert_method=lambda x: x,
                           total_convert_method=lambda x: x):
        """
        这里的取值 key 与kibana 的日志格式有关，日志格式不同则不适用
        :param total_convert_method: 整体数据转换方法
        :param single_convert_method: 单条数据转换方法 例如 json.loads()
        :param log_path: 日志 json 文件路径
        :param filter_method: 日志过滤方法，用于过滤在 kibana 中不方便过滤的日志
        :param reg_method: 日志截取匹配方法，用于在日志中截取或者匹配到需要的 数据 json
        :return: 数据列表
        """
        if log_path.__contains__('.json') is False:
            return []
        with open(log_path) as f:
            load_ = json.load(f)
            hits_ = load_['hits']['hits']
            # 过滤日志
            logs = list(filter(filter_method, hits_))
            log_sources = list(map(lambda x: x['_source']['log'], logs))
            # 日志内容匹配
            data = list(map(single_convert_method, map(reg_method, log_sources)))
            return total_convert_method(data)

    @staticmethod
    def filter_method_by_contains(content: str):
        """
        通过包含关系过滤，结果必须包含 给出的字符串

        :param content: 被包含的字符串
        :return: 筛选 lambda 参数
        """
        return lambda x: x['_source']['log'].__contains__(content)

    @staticmethod
    def reg_method_by_split(splitter: str, index: int):
        """
        根据切分内容进行字符串内容转换

        :param splitter: 用于切分的子串
        :param index: 切分后目标内容在 list 中的索引
        :return: 转换后的字符串
        """
        return lambda x: x.split(splitter)[index]

    @staticmethod
    def reg_method_by_regex(regex: str, index: int):
        """
        通过正则匹配进行字符串内容转换

        :param regex: 正则表达式, 例：'body:(.*?),protocol' 匹配 body: 和 ,protocol 之间的内容
        :param index: 目标子串在正则匹配结果 list 中的索引
        :return: 转换后的字符串
        """
        return lambda x: re.findall(
            regex,
            # 替换空白字符
            x.replace('\n', '').replace(' ', '').replace('\t', ''), 0
        )[index]
