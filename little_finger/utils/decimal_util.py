from _decimal import Decimal, getcontext


def to_decimal(value, scale=6):
    """

    :param value: 需要转换成decimal的数值
    :param scale: 需要转换成decimal的精度
    :return:
    """
    getcontext().prec = scale
    return Decimal(str(value))

