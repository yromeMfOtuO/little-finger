"""
json 工具类
"""

import json
import re


def is_number(s):
    """
    判断一个字符串是否是数字
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    # try:
    #     import unicodedata
    #     unicodedata.numeric(s)
    #     return True
    # except (TypeError, ValueError):
    #     pass

    return False


def to_number(r):
    # 判断是否为正整数
    if r.isdigit():
        return int(r)
    else:
        return float(r)


def is_bool(s):
    """
        判断一个字符串是否是bool
        :param s:
        :return:
        """
    if s.title() in ("True", "False"):  # title()函数将字符串的首字母大写，其余字母全小写
        return True
    else:
        return False


def to_bool(s):
    if s.title() == "True":  # title()函数将字符串的首字母大写，其余字母全小写
        return True
    elif s.title() == "False":
        return False
    else:
        return s


def convert_from_tostring(obj_str: str):
    """
    不包含对象嵌套的单层对象字tostring 字符串转换为 json
    :param obj_str: 对象字符串
    :return:
    """
    if not obj_str:
        return None

    # 去除前后的空白字符及 ()
    strip_ = obj_str.strip()[1:-1]
    findall = re.findall('(.*?)=(.*?),', obj_str.strip()[1:-1]+',')
    result = []
    for item in findall:
        l = item[0].strip()
        r = item[1]
        if r == 'null':
            r = None
        elif is_bool(r):
            r = to_bool(r)
        elif is_number(r):
            r = to_number(r)
        result.append((l, r))
    json_dict = dict(result)
    return json.dumps(json_dict)


def from_tostring(obj_str: str):
    """
    不包含对象嵌套的单层对象字tostring 字符串转换为 json
    :param obj_str: 对象字符串
    :return:
    """
    return convert_from_tostring(obj_str)


def convert_from_tostring_level(obj_str: str):
    """
    包含对象嵌套的单层对象字tostring 字符串转换为 json
    :param obj_str: 嵌套对象字符串
    :return:
    """
    # TODO
    return None


def parse_json_str(json_str: str) -> dict:
    """
    parse json string to dict
    :param json_str: json string
    :return:
    """
    return {}


def pretty_json_string(json_str: str) -> str:
    """
    parse json to pretty format
    :param json_str: json string
    :return:
    """
    return ""


if __name__ == '__main__':
    tostring = convert_from_tostring("(id=2112492, userId=35018924, orderId=fa2e034ad5944ece87144b50f5cf5a23, type=0, sourceAmount=87.51000000, tradeFee=0.45000000, railFee=3.29000000, price=7536.49649220, obtainAmount=0.01111478, status=4, fiatChargeStatus=null, payType=1, createTime=Thu Feb 02 10:26:34 UTC 2023, updateTime=Thu Feb 02 10:28:00 UTC 2023, completedTime=Thu Feb 02 10:28:00 UTC 2023, quoteId=ef048b4a2b7e4274a7cc4bb7c3ebd6f0, cryptoCurrency=BTC, fiatCurrency=USD, startDate=null, endDate=null, tranId=319173599, rversion=6, executePrice=7043.30000000, executeQty=0.01230700, usdToUsdtRate=null, usdtToUsdRate=null, forexRate=null, dForexRate=null, profitAndLoss=null, channelQuotePrice=7432.44230000, spreadCoin=USD, spreadAmount=1.16000000, email=null, rail=CHECKOUT, mode=GOOGLE_PAY, desc=, ext1=null, ext2=null, referNo=, clientType=android, paymentId=85a16768359d462ba8e9c73d548fd0e4, errorCode=null, errorReason=null, isErrorReasonChanged=false, recurringBuyId=8325, purchaseTypeId=8008e07679ea469ea31bc19c20b4cc51, versionType=null, versionNum=null, transferSource=null, transferStatus=null)")
    print(tostring)
