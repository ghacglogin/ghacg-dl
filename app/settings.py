"""应用运行时设置。

通过环境变量 ``APP_ENV`` 控制运行环境，默认 ``production``。
生产环境下关闭 OpenAPI 文档与调试接口，避免暴露项目细节。
"""

from __future__ import annotations

import os
from typing import Literal

Env = Literal["production", "development"]


def get_env() -> Env:
    """读取当前运行环境，默认 ``production``。"""
    value = os.getenv("APP_ENV", "production").strip().lower()
    if value in ("dev", "development", "debug"):
        return "development"
    return "production"


def is_production() -> bool:
    """判断是否处于生产环境。"""
    return get_env() == "production"


__all__ = ["Env", "get_env", "is_production"]
