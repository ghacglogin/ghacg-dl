"""统一异常处理器。

将下载请求来源校验相关的异常（非法 Referer / UA / Cookie 校验失败）
统一对外呈现为 ``403 Forbidden`` 的 HTML 页面，避免泄漏内部判定细节。
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from utils.exceptions import IllegalDownloadRequestException

_TEMPLATE_PATH: Path = Path(__file__).resolve().parent / "templates" / "403.html"
_FORBIDDEN_HTML: str = _TEMPLATE_PATH.read_text(encoding="utf-8")


async def illegal_download_request_handler(
    request: Request, exc: IllegalDownloadRequestException
) -> HTMLResponse:
    """将所有非法下载请求统一返回 403 Forbidden HTML 页面。"""
    return HTMLResponse(content=_FORBIDDEN_HTML, status_code=403)


def register_exception_handlers(app: FastAPI) -> None:
    """向 FastAPI 应用注册全部自定义异常处理器。"""
    app.add_exception_handler(
        IllegalDownloadRequestException, illegal_download_request_handler
    )


__all__ = ["register_exception_handlers", "illegal_download_request_handler"]
