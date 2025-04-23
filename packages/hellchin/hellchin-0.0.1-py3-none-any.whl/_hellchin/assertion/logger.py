# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     logger.py
    Description:   日志配置
 -------------------------------------------------
 """

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("SoftAssert")
