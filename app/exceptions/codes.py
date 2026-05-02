"""HTTP 错误状态码与脱敏展示文案的统一定义。

- :class:`ErrorCode` 提供 HTTP 状态码及业务语义别名（基于 RFC 7231 / RFC 7807）。
- :data:`ERROR_DISPLAY` 提供面向终端用户的「脱敏」标题与提示文案，
  统一由模板渲染层使用，避免直接回传内部异常细节。
"""

from __future__ import annotations

from enum import IntEnum
from typing import NamedTuple


class ErrorCode(IntEnum):
    """HTTP 状态码及业务语义别名。"""

    # --- 2xx Success ---
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # --- 400 Bad Request ---
    BAD_REQUEST = 400
    INVALID_PARAMETER = 400
    MALFORMED_REQUEST = 400

    # --- 401 Unauthorized ---
    UNAUTHORIZED = 401
    NOT_LOGGED_IN = 401
    TOKEN_EXPIRED = 401
    TOKEN_INVALID = 401

    # --- 403 Forbidden ---
    FORBIDDEN = 403
    PERMISSION_DENIED = 403
    ACCESS_DENIED = 403
    ACCOUNT_SUSPENDED = 403

    # --- 404 Not Found ---
    NOT_FOUND = 404
    RESOURCE_NOT_FOUND = 404

    # --- 405 Method Not Allowed ---
    METHOD_NOT_ALLOWED = 405

    # --- 409 Conflict ---
    CONFLICT = 409
    RESOURCE_ALREADY_EXISTS = 409
    STATE_CONFLICT = 409

    # --- 415 Unsupported Media Type ---
    UNSUPPORTED_MEDIA_TYPE = 415
    INVALID_FILE_TYPE = 415

    # --- 422 Unprocessable Entity ---
    VALIDATION_ERROR = 422
    BUSINESS_LOGIC_ERROR = 422

    # --- 429 Too Many Requests ---
    TOO_MANY_REQUESTS = 429
    RATE_LIMIT_EXCEEDED = 429

    # --- 500 Internal Server Error ---
    INTERNAL_ERROR = 500
    SERVER_EXCEPTION = 500

    # --- 501 Not Implemented ---
    NOT_IMPLEMENTED = 501

    # --- 502 Bad Gateway ---
    BAD_GATEWAY = 502
    UPSTREAM_ERROR = 502

    # --- 503 Service Unavailable ---
    SERVICE_UNAVAILABLE = 503
    MAINTENANCE_MODE = 503


class ErrorDisplay(NamedTuple):
    """对外展示的脱敏文案。"""

    title: str
    message: str


_DEFAULT_DISPLAY: ErrorDisplay = ErrorDisplay(
    title="出错了",
    message="服务器在处理您的请求时遇到问题。",
)

ERROR_DISPLAY: dict[int, ErrorDisplay] = {
    400: ErrorDisplay("请求无效", "请求格式有误，请检查后重试。"),
    401: ErrorDisplay("未授权", "请先登录或提供有效的身份凭证。"),
    403: ErrorDisplay("访问受限", "对不起！您没有权限访问此资源。"),
    404: ErrorDisplay("资源不存在", "您访问的页面或资源不存在。"),
    405: ErrorDisplay("方法不允许", "当前接口不支持该请求方式。"),
    409: ErrorDisplay("资源冲突", "请求与当前资源状态冲突，请稍后重试。"),
    415: ErrorDisplay("媒体类型不支持", "当前接口不支持该数据格式。"),
    422: ErrorDisplay("请求无法处理", "请求内容未通过校验，请检查后重试。"),
    429: ErrorDisplay("请求过于频繁", "您操作过于频繁，请稍后再试。"),
    500: ErrorDisplay("服务器异常", "服务器开了个小差，请稍后再试。"),
    501: ErrorDisplay("功能未实现", "该功能暂未开放，敬请期待。"),
    502: ErrorDisplay("网关错误", "上游服务暂时不可用，请稍后再试。"),
    503: ErrorDisplay("服务不可用", "服务正在维护或繁忙，请稍后再试。"),
}


def get_display(status_code: int) -> ErrorDisplay:
    """根据 HTTP 状态码获取脱敏的展示文案，未登记的状态码回退到默认提示。"""
    return ERROR_DISPLAY.get(int(status_code), _DEFAULT_DISPLAY)


__all__ = ["ErrorCode", "ErrorDisplay", "ERROR_DISPLAY", "get_display"]
