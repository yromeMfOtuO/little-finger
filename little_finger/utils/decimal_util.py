from _decimal import Decimal, getcontext


def to_decimal(value, scale=6):
    """

    :param value: 需要转换成decimal的数值
    :param scale: 需要转换成decimal的精度
    :return:
    """
    getcontext().prec = scale
    return Decimal(str(value))


def to_decimal_str(value, scale=6):
    """

    :param value: 需要转换成decimal的数值
    :param scale: 需要转换成decimal的精度
    :return:
    """
    return str(to_decimal(value, scale))


def to_str(num: Decimal) -> str:
    """
    decimal to str
    :param num: decimal
    :return: str
    """
    return format(num, 'f')
