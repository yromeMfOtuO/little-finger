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


def split_decimal(num: Decimal) -> tuple[Decimal, Decimal]:
    """
    split decimal to integer part and fractional part
    :param num: source num
    :return: (integer_part_num, fractional_part_num)
    """
    # 将decimal转换为分数
    numerator, denominator = num.as_integer_ratio()
    # 分离整数部分和小数部分
    integer_part = int(num)
    decimal_part = abs(numerator - integer_part * denominator) / denominator
    return Decimal(str(integer_part)), Decimal(str(decimal_part))


if __name__ == '__main__':
    pair = split_decimal(Decimal('3.14'))
    print(pair[0])
    print(pair[1])
