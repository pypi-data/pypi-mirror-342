# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     test_soft_assert.py
    Description:   
 -------------------------------------------------
 """
from _hellchin.assertion import MethodAssert


def test_soft_assert():
    method_assert = MethodAssert()
    # 1. 直接调用方法断言的方法，手动输出断言结果
    method_assert.equal(1, 1, assert_name="test")
    method_assert.not_equal(1, "2", jsonpath="$.a")
    method_assert.check(1 == 3)
    # method_assert.report()  # 调用方法断言的report方法，输出断言结果
