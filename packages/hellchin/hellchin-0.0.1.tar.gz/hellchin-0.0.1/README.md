# hellchin-lib

## 简介
个人开发使用的一些工具包，主要用于自动化测试，目前主要开发断言功能，支持软硬断言。

## 安装
```bash
pip install hellchin-lib
```

## 项目关键结构

项目文件结构如下：

```aiignore
my_tool/
├── my_tool/            # 项目的源代码目录。
│   ├── __init__.py
│   ├── main.py
├── setup.py            # 项目的安装脚本，用于将项目打包为可安装的包。
├── pyproject.toml      # 项目配置文件，用于定义项目信息、依赖项等。
├── README.md           # 项目说明文件。
├── LICENSE             # 项目许可证文件。
└── requirements.txt    # 项目依赖的第三方库列表。
```




## 使用方法

！！！详细教程有空的时候再进行更新

建议教程如下：

示例代码：

```python
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
# pm.expect(res.b).to.equal(1)
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

```


## 文档链接

更多文档请访问：None
