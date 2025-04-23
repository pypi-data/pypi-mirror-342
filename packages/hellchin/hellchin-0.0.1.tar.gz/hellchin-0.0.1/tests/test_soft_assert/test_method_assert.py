# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     test_method_assert.py
    Description:   测试代码
 -------------------------------------------------
 """
import unittest

import pytest

from _hellchin.assertion.method_assert import MethodAssert


class TestMethodAssert:
    def setUp(self) -> None:
        self.expect = MethodAssert()

    def tearDown(self) -> None:
        pass

    def test_equal(self):
        expect = MethodAssert()
        expect.equal(1, 1, assert_name="Check if 1 equals 1")
        expect.result()

    def test_equal_2(self):
        expect = MethodAssert
        expect(1).equal(2)

    def test_not_equal(self):
        expect = MethodAssert()
        expect.not_equal(1, 1, "Check if 1 does not equal 2")
        expect.result()


if __name__ == '__main__':
    pytest.main()
