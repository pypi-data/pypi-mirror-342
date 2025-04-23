# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     base_soft_assert.py
    Description:   自定义软断言类，支持灵活调用和集成
 -------------------------------------------------
1. 提供基础的断言功能，包括记录、检查和报告断言结果。
2. 支持单独使用或作为上下文管理器使用。
 """

import inspect
import weakref
from typing import Any

import pytest


class SoftAssert:
    """自定义软断言类，支持灵活调用和集成"""

    def __init__(self):
        self.results_list = []  # 记录所有断言的结果
        self.has_failures = False  # 是否存在失败断言
        self.success_icon = "✅ "
        self.failure_icon = "❌ "

    def check(self, condition, assert_name=None, error_message=None):
        """
        记录断言结果。

        :param condition: 表达式或条件，结果应为布尔值
        :param assert_name: 断言名称，默认为None，自动生成
        :param error_message: 如果断言失败时的错误消息
        """
        # 获取调用代码的表达式
        frame = inspect.currentframe().f_back
        code_context = inspect.getframeinfo(frame).code_context
        if code_context:
            expression = code_context[0].strip()
            # print(expression)
            # 提取传入的第一个参数（表达式）
            expression = expression[expression.find("(") + 1: expression.rfind(",", 0)]
            # print(expression)
        else:
            expression = str(condition)

        # 如果断言名称为None，则使用表达式作为断言名称
        # print(type(assert_name))
        assert_info = assert_name or f"{expression}"

        error_message = f"AssertionError: {error_message}" if error_message else error_message

        # 执行断言
        try:
            assert condition, error_message
            # 记录成功的断言
            self.results_list.append("✅ " + assert_info)
        except AssertionError as ae:
            # 记录失败的断言
            if error_message:
                failure_message = self.failure_icon + ' | '.join([assert_info, error_message])
            else:
                failure_message = self.failure_icon + assert_info
            self.results_list.append(failure_message)
            self.has_failures = True  # 标记存在失败断言

        return self.results_list[-1]

    def result(self, clear=True):
        """
        报告所有断言结果。
        "主动调用表示将所有的结果输出"

        :param clear: 是否清空历史结果，默认清空
        :raises AssertionError: 如果有失败断言
        """
        failure_count = len([r for r in self.results_list if r.startswith("❌")])
        success_count = len([r for r in self.results_list if r.startswith("✅")])

        # 报告结果
        report_messages = "\n".join([f"    [{i + 1}] {msg}" for i, msg in enumerate(self.results_list)])

        if clear:
            self.results_list = []  # 清空结果

        return (
            f"Soft assertion summary:\n"
            f"""{success_count} success(es){f', {failure_count} failure(s)' if failure_count == 0 else ''}: \n"""
            f"{report_messages}"
        )

    def fail(self):
        assert_results = self.result()
        # 判断 AssertionError 是否包含在列表字符串中
        contains_assertion_error = "AssertionError" in assert_results
        # 如果断言结果中包含 "AssertionError" 字符串，或者存在失败断言，则抛出异常
        if contains_assertion_error or self.has_failures:
            # 使用 pytest.fail 避免过多堆栈信息
            pytest.fail(
                reason=assert_results,
                # 可选参数，默认为True。
                pytrace=False,  # 是否显示完整的 Python 跟踪信息（traceback）。设置为 False 可以隐藏 Python 栈信息，直接显示失败原因。
                # msg="test failed"
            )
        else:
            print(assert_results)

    def __enter__(self):
        """进入上下文"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动报告断言结果"""
        self.result()

    # def __del__(self):
    #     """
    #     析构函数，在对象被销毁时自动报告断言结果，
    #     当对象不再被引用时，Python会自动调用该方法来释放资源
    #     如果不想手动调用fail(), 可以重写del方法，在对象销毁时自动调用fail()方法
    #     注意: 异常无法被外部捕捉，
    #     """
    #     self.fail()


if __name__ == '__main__':
    expect = SoftAssert()
    expect.check(1 == 1, "1==1")
    expect.check(1 == 2, "1==2")
    expect.check(1 == 3, "1==3")
