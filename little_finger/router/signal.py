"""
用于减少编码中的多个简单条件if分支,
实现类似 java spring 中通过 application context 生命周期回调实现的工厂路由

实例见下方test
"""

import functools

from blinker import Signal


def dispatch(func):
    """
    入口方法装饰器
    :param func: 入口方法
    :return: 装饰后的方法
    """

    # 路由表
    signal_ = Signal()

    @functools.wraps(func)
    def wrapper(arg0, *args, **kwargs):
        """获取分支方法，获取失败则使用入口方法做兜底"""
        if signal_.receivers and signal_.has_receivers_for(arg0):
            # hard code。。
            return signal_.send(arg0, *args, **kwargs)[0][1]
        return func(arg0, *args, **kwargs)

    def mapping(key):

        def wrap(branch_func):
            @signal_.connect_via(key)
            def do_branch_func(arg0, *args, **kwargs):
                return branch_func(arg0, *args, **kwargs)

            return do_branch_func
        return wrap

    wrapper.mapping = mapping
    return wrapper


if __name__ == '__main__':
    # pylint: disable = E, W, R, C
    @dispatch
    def fun(key):
        raise ValueError(f'key error, key: {key}')


    @fun.mapping(1)
    def __fun1(key):
        return 1 + key


    @fun.mapping(2)
    def __fun2(key):
        return 2 + key


    @fun.mapping(3)
    @fun.mapping(4)
    def __fun34(key):
        return 3 + key


    print(f'result：{fun(1)}')
    print(f'result：{fun(3)}')
    print(f'result：{fun(5)}')
