import pandas as pd
import matplotlib.pyplot as plt


def line_chart(df: pd.DataFrame, x: str, y: str, title: str, x_ascending=True, **kwargs):
    """
    绘制折线图
    :param df: pandas DataFrame
    :param x: x 轴字段
    :param y: y 轴字段
    :param title: 图表标题
    :param x_ascending: x 轴是否升序
    :param kwargs: 其他参数
    :return: None
    """
    df.sort_values(x, ascending=x_ascending, inplace=True)
    df.plot(x=x, y=y, figsize=(20, 10), title=title, **kwargs)
    plt.show()


def file_line_chart(path: str, x: str, y: str, title: str, read_method=pd.read_csv, x_ascending=True, **kwargs):
    """
    从数据文件读取数据，绘制折线图
    :param path: 数据文件路径
    :param x: x 轴字段
    :param y: y 轴字段
    :param title: 图表标题
    :param read_method: 读取方法，例：pd.read_excel
    :param x_ascending: x 轴是否升序
    :param kwargs: 其他参数
    :return: None
    """
    line_chart(read_method(path), x, y, title, x_ascending=x_ascending, **kwargs)


def histogram_chart(df: pd.DataFrame, x: str, y: str, title: str, x_ascending=True):
    """
    绘制柱状图
    :param df: pandas DataFrame
    :param x: x 轴字段
    :param y: y 轴字段
    :param title: 图表标题
    :param x_ascending: x 轴是否升序
    :return: None
    """
    df.sort_values(x, ascending=x_ascending, inplace=True)
    df.plot.bar(x=x, y=y, figsize=(20, 10), title=title)
    plt.show()
    df.sort_values(x, ascending=x_ascending, inplace=True)
    df.plot.bar(x=x, y=y, title=title)
    plt.show()


def file_histogram_chart(path: str, x: str, y: str, title: str, read_method=pd.read_csv, x_ascending=True):
    """
    从数据文件读取数据，绘制柱状图
    :param path: 数据文件路径
    :param x: x 轴字段
    :param y: y 轴字段
    :param title: 图表标题
    :param read_method: 读取方法，例：pd.read_excel
    :param x_ascending: x 轴是否升序
    :return: None
    """
    histogram_chart(read_method(path), x, y, title, x_ascending=x_ascending)


if __name__ == '__main__':
    file_line_chart('2023_06_24_23_37_12_S202306242337073069-2.csv', 'date', 'order count', 'Volume vs. Time')
