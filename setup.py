__author__ = 'weihao.lv'

from setuptools import setup, find_packages


def long_description():
    with open("README.md", "r") as fh:
        long_desc = fh.read()
        return long_desc


def requirements():
    with open("requirements.txt", "r") as fh:
        reqs = [line.strip() for line in fh]
        return reqs


setup(
    name='little-finger',
    version='0.0.9',  # 版本号
    description='tool pkg.',  # 包的介绍
    author='yromeMfOtuO',  # 作者 就是我啦～
    author_email='weihao.lv@outlook.com',  # 你的邮箱
    url='',  # 项目地址，一般的填git地址 也可以是任意可用的url 不过我喜欢使用 git
    packages=find_packages(),  # Python导入包的列表，我们使用find_packages() 来自动收集
    long_description=long_description(),  # 项目的描述 一般是 string 上文中定义了它
    long_description_content_type="text/markdown",  # 描述文档 README 的格式 一般我喜欢MD. 也可以是你喜欢的其他格式 支不支持我就不知道了～ 估计HTML 是支持的
    license="GPLv3",  # 开源协议
    # 这 需要去官网查，在下边提供了许可证连接 或者 你可以直接把我的粘贴走
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"],

    python_requires='>=3.6',  # Python 的版本约束
    # 其他依赖的约束
    install_requires=requirements()
)

