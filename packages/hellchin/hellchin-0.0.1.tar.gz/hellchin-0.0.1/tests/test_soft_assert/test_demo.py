# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     test_demo.py
    Description:   
 -------------------------------------------------
 """

from hellchin import PostManAssertMethod, MethodAssert

pm = PostManAssertMethod()
pm.response = {
    "a": 1
}

# raise Exception("测试")
pm_code_test = """
# pm.expect(1).to.equal(2)
pm.test("", lambda: pm.expect('1').to.equal(1))
pm.test("失败断言", lambda: pm.expect(1).to.equal(2))
pm.test("", lambda: pm.expect(1).to.equal(1))
pm.test("成功断言", lambda: pm.expect(1).to.equal(1))
res = pm.response.json()
pm.test("undefined 测试", lambda: pm.expect(res.b).to.equal(1))
pm.expect(1).to.equal(2)
"""

exec(pm_code_test, {"pm": pm})

ma_code_test = """
method_assert.check(1 == 1)
method_assert.check(1 == 2)
method_assert.equal(1, 1)
method_assert.equal(1, 2)
method_assert.exists(1)
method_assert.fail()
"""

# exec(ma_code_test, {"method_assert": MethodAssert()})
