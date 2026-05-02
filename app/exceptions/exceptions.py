from app.exceptions.codes import ErrorCode
from fastapi import HTTPException


class BadRequestError(HTTPException):
    """400 Bad Request - 请求参数错误"""
    def __init__(self, detail: str = "请求参数错误"):
        super().__init__(status_code=ErrorCode.BAD_REQUEST.value, detail=detail)


class UnauthorizedError(HTTPException):
    """401 Unauthorized - 未认证"""
    def __init__(self, detail: str = "未提供认证信息"):
        super().__init__(status_code=ErrorCode.UNAUTHORIZED.value, detail=detail)


class ForbiddenError(HTTPException):
    """403 Forbidden - 禁止访问"""
    def __init__(self, detail: str = "禁止访问"):
        super().__init__(status_code=ErrorCode.FORBIDDEN.value, detail=detail)


class NotFoundError(HTTPException):
    """404 Not Found - 资源不存在"""
    def __init__(self, detail: str = "资源不存在"):
        super().__init__(status_code=ErrorCode.NOT_FOUND.value, detail=detail)


class ConflictError(HTTPException):
    """409 Conflict - 资源冲突"""
    def __init__(self, detail: str = "资源冲突"):
        super().__init__(status_code=ErrorCode.CONFLICT.value, detail=detail)


class ValidationError(HTTPException):
    """422 Unprocessable Entity - 验证错误"""
    def __init__(self, detail: str = "验证错误"):
        super().__init__(status_code=ErrorCode.VALIDATION_ERROR.value, detail=detail)