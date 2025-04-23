# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     setup.py
    Description:   包的元信息
 -------------------------------------------------
 """
from pathlib import Path

from setuptools import setup, find_packages

# 确保路径基于 setup.py 所在目录
here = Path(__file__).parent
print(here)
readme = (here / "README.md").read_text(encoding="utf-8")
changelog = (here / "CHANGELOG.md").read_text(encoding="utf-8")

setup(
    name="hellchin",  # 包名
    version="0.0.1",  # 版本号 主版本号.次版本号.修订号 重大更新.小更新.小修订
    description="一个属于软件测试工程师使用的工具库.",  # 描述
    author="hellchin",  # 作者
    author_email="zhuangyuqiu986@163.com",  # 作者邮箱
    packages=find_packages(),  # 包列表: 自动查找所有包含__init__.py文件的目录
    install_requires=[
        "pytest>=6.0.0",  # 依赖的包
    ],
    classifiers=[  # 分类器列表
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=readme + "\n\n" + changelog,
    long_description_content_type="text/markdown",
)
