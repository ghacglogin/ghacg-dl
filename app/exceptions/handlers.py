"""统一异常处理器。

将服务端各类错误统一渲染为 HTML 错误页：
- 根据 HTTP 状态码从 :data:`ERROR_DISPLAY` 中取出脱敏的标题/消息；
- 注入通用模板 ``templates/error.html`` 并以对应状态码返回；
- 不向客户端泄漏内部异常的具体细节。
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.codes import ErrorCode, get_display
from utils.exceptions import IllegalDownloadRequestException

_TEMPLATE_PATH: Path = Path(__file__).resolve().parent / "templates" / "error.html"
_TEMPLATE: str = _TEMPLATE_PATH.read_text(encoding="utf-8")


def render_error(status_code: int) -> HTMLResponse:
    """根据状态码渲染统一错误页。"""
    display = get_display(status_code)
    html = _TEMPLATE.format(
        code=int(status_code),
        title=display.title,
        message=display.message,
    )
    return HTMLResponse(content=html, status_code=int(status_code))


async def illegal_download_request_handler(
    request: Request, exc: IllegalDownloadRequestException
) -> HTMLResponse:
    """非法下载请求统一返回 403，避免泄漏内部判定细节。"""
    return render_error(ErrorCode.FORBIDDEN)


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> HTMLResponse:
    """统一接管 FastAPI/Starlette 抛出的 HTTPException。"""
    return render_error(exc.status_code)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> HTMLResponse:
    """请求参数校验失败统一返回 422 脱敏页面。"""
    return render_error(ErrorCode.VALIDATION_ERROR)


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> HTMLResponse:
    """兜底处理未捕获异常，避免堆栈信息泄漏。"""
    return render_error(ErrorCode.INTERNAL_ERROR)


def register_exception_handlers(app: FastAPI) -> None:
    """向 FastAPI 应用注册全部自定义异常处理器。"""
    app.add_exception_handler(
        IllegalDownloadRequestException, illegal_download_request_handler
    )
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


__all__ = [
    "register_exception_handlers",
    "render_error",
    "illegal_download_request_handler",
    "http_exception_handler",
    "validation_exception_handler",
    "unhandled_exception_handler",
]
