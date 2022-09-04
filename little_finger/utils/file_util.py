"""
文件操作
"""

import os

import requests


def download_file(url: str, path: str, http_args: dict):
    """
    下载文件，存储到本地，本地路径不存在时主动创建
    :param url: 文件网络 url
    :param path: 文件存储在本地的路径
    :param http_args: http 请求需要携带的参数
    :return: None
    """
    response = requests.get(url, **http_args)
    # 获取的文本实际上是图片的二进制文本
    file_content = response.content
    # 图片路径不存在则创建
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # 将他拷贝到本地文件 w 写 b 二进制  wb代表写入二进制文本
    with open(path, 'wb') as f:
        f.write(file_content)
        f.flush()


def get_file_format(path: str) -> str:
    return path.split('.')[-1]
