"""
用于减少编码中的多个简单条件if分支,
实现类似 java spring 中通过 application context 生命周期回调实现的工厂路由

实例见下方test
"""

import functools


def router(func):
    """
    入口方法装饰器
    :param func: 入口方法
    :return: 装饰后的方法
    """

    # 路由表
    route_table = {}

    @functools.wraps(func)
    def wrapper(arg0, *args, **kwargs):
        """获取分支方法，获取失败则使用入口方法做兜底"""
        try:
            branch_func = route_table[arg0]
        except KeyError:
            pass
        else:
            return branch_func(arg0, *args, **kwargs)
        return func(arg0, *args, **kwargs)

    def route(key):
        # 用于将具体分支方法注册到路由表中
        def wrap(branch_func):
            """分支方法路由注册"""
            if key in route_table:
                raise ValueError(f'@route: ambiguous branch func for {key!r}')
            route_table[key] = branch_func
            return branch_func
        return wrap

    wrapper.route = route
    return wrapper


if __name__ == '__main__':
    # pylint: disable = E, W, R, C
    @router
    def fun(key):
        raise ValueError(f'key error, key: {key}')

    @fun.route(1)
    def __fun1(key):
        return 1 + key

    @fun.route(2)
    def __fun2(key):
        return 2 + key

    @fun.route(3)
    @fun.route(4)
    def __fun34(key):
        return 3 + key

    print(f'result：{fun(3)}')
    print(f'result：{fun(5)}')
