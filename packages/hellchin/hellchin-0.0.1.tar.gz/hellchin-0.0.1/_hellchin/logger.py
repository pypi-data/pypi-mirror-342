# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     logger.py
    Description:   基于 loguru 的企业级日志工具
 -------------------------------------------------
 """

from __future__ import annotations

from typing import TYPE_CHECKING

import os
import sys

from loguru import logger
from typing import Optional

__all__ = ["LoggerManager"]

if TYPE_CHECKING:
    import loguru


class LoggerManager:
    """企业级日志管理器，负责配置日志、清理过期日志、控制台和文件日志的处理"""

    def __init__(
            self,
            log_path: Optional[str] = None,
            level: str = "DEBUG",
            retention: str = "7 days",
            rotation: str = "00:00",
            format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <level>{message}</level>",
            compress: str = "zip",
            async_write: bool = True,
            log_size: str = "100 MB",
            error_level: str = "WARNING",
    ):
        """
        初始化日志管理器，支持灵活配置。

        :param log_path: 日志保存路径，如果为空使用默认路径
        :param level: 日志记录级别
        :param retention: 日志保留期限
        :param rotation: 日志切割条件
        :param format: 日志输出格式
        :param compress: 日志压缩格式
        :param async_write: 是否启用异步写入日志
        :param log_size: 单个日志文件最大大小
        :param error_level: 错误日志记录级别
        """

        self.log_path = log_path
        self.level = level
        self.retention = retention
        self.rotation = rotation
        self.format = format
        self.compress = compress
        self.async_write = async_write
        self.log_size = log_size
        self.error_level = error_level

    def configure(self) -> loguru.Logger:
        """
        配置日志记录器，设置控制台输出和文件输出。
        """

        # 移除默认的日志配置
        logger.remove()

        # 控制台输出配置
        logger.add(
            sys.stdout,
            level="DEBUG",
            format="<level>{message}</level>",
            colorize=True,
            enqueue=True,
        )

        # 如果日志路径不为空，则进行文件输出配置
        if self.log_path:
            # 创建日志目录(如果不存在)
            os.makedirs(self.log_path, exist_ok=True)

            # 文件输出配置: 记录所有日志
            logger.add(
                os.path.join(self.log_path, '{time:YYYY-MM-DD}/logs.log'),
                level=self.level,
                format=self.format,
                rotation=self.rotation,  # 每天 00:00 分进行日志切割
                compression=self.compress,  # 压缩格式
                retention=self.retention,  # 日志保留期限
                enqueue=self.async_write,  # 异步日志写入
                # max_size=self.log_size,  # 单个日志文件最大大小
            )

            # 日志只记录错误及以上：默认仅记录 WARNING 及以上日志
            logger.add(
                os.path.join(self.log_path, '{time:YYYY-MM-DD}/error.log'),
                level=self.error_level,
                format=self.format,
                rotation=self.rotation,  # 每天 00:00 分进行日志切割
                compression=self.compress,  # 压缩格式
                retention=self.retention,  # 日志保留期限
                enqueue=self.async_write,  # 异步日志写入
                # max_size=self.log_size,  # 单个日志文件最大大小
            )

        return logger


# 示例
if __name__ == "__main__":
    # 创建日志记录器实例
    log = LoggerManager().configure()

    log.debug("This is a debug message")
    log.info("This is an info message")
    log.warning("This is a warning message")
    log.error("This is an error message")
    log.success("This is a success message")
