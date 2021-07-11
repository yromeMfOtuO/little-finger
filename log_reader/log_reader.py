__author__ = 'weihao.lv'

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
                           convert_method=lambda x: x):
        """
        这里的取值 key 与kibana 的日志格式有关，日志格式不同则不适用
        :param convert_method: 转换方法 例如 json.loads()
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
            data = list(map(convert_method, map(reg_method, log_sources)))
            return data

    @staticmethod
    def filter_method_by_contains(content: str):
        return lambda x: x['_source']['log'].__contains__(content)

    @staticmethod
    def reg_method_by_split(splitter: str, index: int):
        return lambda x: x.split(splitter)[index]

    @staticmethod
    def reg_method_by_regex(regex: str, index: int):
        return lambda x: re.findall(regex, x.replace('\n', '').replace(' ', '').replace('\t', ''), 0)[index]






