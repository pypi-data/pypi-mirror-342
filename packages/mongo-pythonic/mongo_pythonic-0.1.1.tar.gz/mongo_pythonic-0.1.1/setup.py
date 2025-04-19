from setuptools import setup, find_packages

setup(
    name="mongo_pythonic",  # 项目名称
    version="0.1.1",  # 版本号
    author="guai_xiao",  # 作者姓名
    license="GPL-3.0",
    author_email="guai-xiao@hotmail.com",  # 作者邮箱
    description="Repackage pymongo to make it more pythonic",  # 简短描述
    long_description=open("README.md", "r", encoding="utf-8").read(),  # 详细描述
    long_description_content_type="text/markdown",  # 描述文件格式
    url="https://github.com/guaixiao7720/mongohelper",  # 项目主页链接
    packages = find_packages(),  # 自动发现项目中的包
    classifiers=[
        "Programming Language :: Python :: 3",  # 适用的 Python 版本
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # 项目许可证类型
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # 要求的最低 Python 版本
    install_requires=[
        "pymongo",  # 列出项目的依赖项
    ],
)
