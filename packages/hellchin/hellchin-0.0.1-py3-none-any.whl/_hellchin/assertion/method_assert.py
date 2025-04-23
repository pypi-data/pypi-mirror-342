# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     method_assert.py
    Description:   具体断言逻辑实现
 -------------------------------------------------

 继承 SoftAssert 类，扩展出具体的断言方法。
 如 equal、not_equal、greater_than 等。
 """

from typing import Union, Any

import requests
from box import Box

from _hellchin.assertion.base_soft_assert import SoftAssert


class AssertMsg:

    def __init__(self, *args, actual, expected, context):
        self.msg = args[0]
        self.actual = actual
        self.expected = expected
        self.context = context

    def __call__(self, *args, **kwargs):
        # 对象() 把对象当作函数调用，相当于执行对象.__call__()
        return self.msg  # 默认返回第一个参数作为断言信息


class AssertionUndefinedError(AssertionError):
    pass


class Undefined:
    def __repr__(self):
        return "undefined"


# 实例化一个特殊对象
UNDEFINED = Undefined()


class BaseMethodAssert:
    """
    BaseMethodAssert 类，用于实现具体的断言方法。硬断言方法。
    """

    def __init__(self, expected_value: Any = None):
        super().__init__()

        self.IS_UNDEFINED = isinstance(expected_value, Undefined)  # 判断是否是未定义的对象

        self.expected = expected_value

    @staticmethod
    def _parse_assert_data(assert_data: Union[str, dict]) -> dict:
        """
        解析断言数据，支持字符串或 pydantic 模型

        :param assert_data: 可能是字符串表达式或 pydantic 模型
        :return: 解析后的 Assertion 对象
        """
        if isinstance(assert_data, dict):  # Assertion
            return assert_data
        elif isinstance(assert_data, str):
            # 解析字符串格式，比如 `$.code > "200"`
            # return self._parse_string_assert(assert_data)
            raise ValueError(f"Unsupported assert_data type: {type(assert_data)}")
        else:
            raise ValueError(f"Unsupported assert_data type: {type(assert_data)}")

    def _generate_assert_messages(self, success_condition: str, fail_message: str, actual=None, expected=None) -> tuple:
        """
        生成断言的成功和失败信息。

        :param success_condition: 成功条件描述
        :param fail_message: 失败消息模板
        :param actual: 实际值
        :param expected: 预期值
        :return: 成功信息和失败信息
        """

        assert_info_success = success_condition
        fail_message = fail_message.format(actual=repr(actual), expected=repr(expected))
        assert_info_fail = f"{assert_info_success} | AssertionError: {fail_message}"
        assert_raise_msg = AssertMsg(assert_info_fail, actual=actual, expected=expected, context=fail_message)
        # print(f"assert_raise_msg: {assert_raise_msg()}")

        # 如果实际值是未定义的，则抛出 AssertionUndefinedError
        if self.IS_UNDEFINED:
            raise AssertionUndefinedError(assert_raise_msg)  # 抛出一个错误对象，具体的错误信息由 assert_raise_msg 提供

        return assert_info_success, assert_raise_msg

    def equal(self, actual, /, expected=None, *, assert_name=None, jsonpath: str = None):
        """
        判断响应相等的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{repr(expected)} == {jsonpath or actual}",
            "expected {expected} to deeply equal {actual} ",
            actual, expected
        )

        assert actual == expected, fail_message

        return success_message

    def not_equal(self, actual, expected=None, assert_name=None, jsonpath: str = None):
        """
        判断响应不相等的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{repr(expected)} != {jsonpath or actual}",
            "expected {actual} not to deeply equal {expected} ",
            actual, expected
        )

        assert actual != expected, fail_message

        return success_message

    def greater_than(self, actual, expected=None, assert_name=None, jsonpath: str = None):
        """
        判断响应大于的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} > {repr(expected)}",
            "expected {actual} to be greater than {expected} ",
            actual, expected
        )

        assert actual > expected, fail_message

        return success_message

    def greater_than_or_equal(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应值是否大于或等于预期值的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} >= {repr(expected)}",
            "expected {actual} to be greater than or equal to {expected} ",
            actual, expected
        )

        assert actual >= expected, fail_message

        return success_message

    def greater_than_or_equal_v2(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应值是否大于或等于预期值的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} >= {repr(expected)}",
            "expected {actual} to be greater than or equal to {expected} ",
            actual, expected
        )

        assert actual >= expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual >= expected, success_message, fail_message)

    def less_than(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应小于的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} < {repr(expected)}",
            "expected {actual} to be less than {expected} ",
            actual, expected
        )

        assert actual < expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual < expected, success_message, fail_message)

    def less_than_or_equal(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应小于或等于的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} <= {repr(expected)}",
            "expected {actual} to be less than or equal to {expected} ",
            actual, expected
        )

        assert actual <= expected, fail_message

        return success_message

    @property
    def exists(self):
        """
        判断 key 是否存在的逻辑。
        self, expected=None, *, assert_name=None, jsonpath: str = None
        """

        def func(*args, **kwargs):
            print(f"IS_UNDEFINED: {self.IS_UNDEFINED}")

            expected = self.expected or args[0]

            desc = kwargs.get("desc", None)

            if expected is None:
                raise ValueError("Expected value cannot be None.")

            success_message, fail_message = self._generate_assert_messages(
                desc or f"{expected} exists",
                "expected {expected} to exist",
                expected=expected
            )

            assert bool(expected), fail_message

            return success_message

        return func

    @property
    def not_exists(self):
        """
        判断 key 不存在的逻辑。
        """

        def func(*args, **kwargs) -> str:
            expected = self.expected or args[0]

            desc = kwargs.get("desc", None)

            if expected is None:
                raise ValueError("Expected value cannot be None.")

            success_message, fail_message = self._generate_assert_messages(
                desc or f"{expected} does not exist",
                "expected {expected} to not exist",
                expected=expected
            )

            assert not bool(expected), fail_message

            return success_message

        return func


class Expect:
    """
    Expect 类，用于创建一个 to 属性，该属性包含一个 BaseMethodAssert 对象，
    """

    def __init__(self, expected_value: Any):
        try:
            self.to = BaseMethodAssert(expected_value)
        except Exception as e:
            print("到Expect了", e)


class PostManAssertMethod:

    def __init__(self):
        # self.expect = Expect  # 初始化Expect对象
        self._response = dict()  # 初始化响应对象
        self.__success_icon = "✅ "
        self.__failure_icon = "❌ "
        self.test_results_list = []  # 初始化结果列表

    @staticmethod
    def _format_assert_error(desc: str, error_message: str) -> str:
        """
        格式化断言错误信息。
        """
        if desc:
            error_message = error_message.split('|')[1]
            return f"❌ {desc} |{error_message}"
        return f"❌ {error_message}"

    @staticmethod
    def test(desc, test_func=None):
        """
        测试方法，用于执行测试函数，并打印测试结果。

        test 方法要对抛出的异常信息做特殊化处理，用来区分硬断言。
        对所有的异常都捕获，因为它们都在test中，不需要在函数外处理
        :param desc:
        :param test_func:
        :return:
        """
        try:
            assert_result = test_func()
            print(f"✅ {desc if desc else assert_result}")

        # 自定义异常类，捕捉 expect(参数) 参数为正确传入的情况
        except AssertionUndefinedError as e:
            print(PostManAssertMethod._format_assert_error(desc, e.args[0].msg))

        except AssertionError as e:
            # 如果断言失败，我们需要处理下断言信息
            print(PostManAssertMethod._format_assert_error(desc, e.args[0].msg))

        except AttributeError as e:
            print("❌ {desc} | {exception_type}: {exception_msg}".format(
                desc=desc,
                exception_type="AssertionError",
                exception_msg=e.args[0]
            ))

        except Exception as e:
            print("⚠️ 未处理的异常错误，请检查: {}".format(e))

    @property
    def response(self):
        """获取响应"""

        class ResponseProxy:
            def __init__(self, response):
                self._response = response

            def json(self):

                # 判断响应类型
                if isinstance(self._response, requests.Response):
                    dict_response = self._response.json()
                elif isinstance(self._response, dict):
                    dict_response = self._response
                else:
                    raise TypeError(f"Invalid response type: {type(self._response)}")

                return Box(
                    dict_response,
                    default_box=True,  # 是否在访问不存在的键时返回空的 Box 对象
                    default_box_attr=UNDEFINED,  # 不存在的键返回默认值 undefined
                )

            def __getattr__(self, item):
                # 代理其他属性和方法到原始 response 对象
                return getattr(self._response, item)

        return ResponseProxy(self._response)

    @response.setter
    def response(self, value):
        """设置响应"""
        self._response = value

    @staticmethod
    def expect(expected_value: Any):
        """
        断言方法
        需要捕获异常信息，处理后返回断言结果，这里是硬断言
        :param expected_value:
        :return:
        """
        try:
            return Expect(expected_value)
        except AssertionError as e:
            print(f"expect: ", e)
        except Exception as e:
            print(f"断言异常！！！检查代码", e)


class MethodAssert(SoftAssert):
    def __init__(self, expected_value: Any = None):
        super().__init__()
        self.__base_assert = BaseMethodAssert(expected_value)
        self.expected = expected_value  # 期望值

    def _proxy_method(self, method_name, *args, **kwargs):
        """代理方法，用于调用指定方法并捕获其中的异常"""
        method = getattr(self.__base_assert, method_name)
        try:
            success_result = method(*args, **kwargs)
            self.results_list.append(self.success_icon + success_result)
        except AssertionError as e:
            self.results_list.append(self.failure_icon + e.args[0])

    def __getattr__(self, name):
        """获取属性时自动调用代理方法"""
        if name.startswith('_'):  # 如果方法名以'_'开头，则不进行代理
            pass
        elif hasattr(self.__base_assert, name):
            return lambda *args, **kwargs: self._proxy_method(name, *args, **kwargs)
        else:
            # 如果没有找到指定的方法，则抛出AttributeError异常
            raise AttributeError(f"{type(self).__name__} object has no attribute {name}")


if __name__ == '__main__':
    pm = PostManAssertMethod()
    # pm.expect(1).to.equal(2)
    pm.test("", lambda: pm.expect(1).to.equal(2))
    pm.test("失败断言", lambda: pm.expect(1).to.equal(2))
    pm.test("", lambda: pm.expect(1).to.equal(1))
    pm.test("成功断言", lambda: pm.expect(1).to.equal(1))

    method_assert = MethodAssert()
    method_assert.check(1 == 1)
    method_assert.check(1 == 2)
    method_assert.equal(1, 1)
    method_assert.equal(1, 2)
    method_assert.fail()
