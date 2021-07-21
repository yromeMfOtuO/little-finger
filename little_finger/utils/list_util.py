__author__ = 'weihao.lv'


def flatten(list_) -> list:
    """
        展开 List[List] 为 List
        :param list_:
        :param x:
        :return:
    """
    if isinstance(list_, list):
        return [a for i in list_ for a in flatten(i)]
    else:
        return [list_]
