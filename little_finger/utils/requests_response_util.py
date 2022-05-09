"""
requests response处理，校验状态码及成功标志
默认response content-type 为 json
"""
import requests


def check_status(response: requests.Response, err_msg: str = None):
    """
    check http response status is 200
    :param response: requests http response
    :param err_msg: exception error message
    """
    if str(response.status_code).startswith("2"):
        if not err_msg:
            err_msg = f"response status code: {response.status_code}, response content: {response.content}"
        raise Exception(err_msg)


def check_flag(response: requests.Response, flag: str = 'success', err_msg: str = None):
    """
    check http response status is 200, and check the business success flag
    :param response: requests http response
    :param flag: business flag key
    :param err_msg: exception error message
    """
    check_status(response, err_msg)
    if not response.json()[flag]:
        if not err_msg:
            err_msg = f"business code is not success, response content: {response.content}"
        raise Exception(err_msg)


def check_export(response: requests.Response, err_msg: str = None):
    """
    check http response status is 200, and export response json
    :param response: requests http response
    :param err_msg: exception error message
    :return: json
    """
    check_status(response, err_msg)
    return response.json()


def check_flag_export(response: requests.Response, flag: str = 'success', err_msg: str = None):
    """
    check http response status is 200, and check the business success flag, then export response json
    :param response: requests http response
    :param flag: business flag key
    :param err_msg: exception error message
    """
    check_flag(response, flag, err_msg)
    return response.json()