# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     __init__.py.py
    Description:   
 -------------------------------------------------
 """

from .base_soft_assert import SoftAssert
from .method_assert import MethodAssert

# 定义包的统一接口
__all__ = [
    "SoftAssert",
    "MethodAssert"
]
