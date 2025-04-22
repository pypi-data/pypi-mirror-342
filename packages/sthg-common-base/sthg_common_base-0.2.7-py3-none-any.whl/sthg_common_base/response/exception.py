#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：DongQing
@File    ：exception.py
@Time    ：2025/3/31
@Desc    ：
"""
__all__ = [
    'BaseException',
    'CustomException',
    'register_exception_handlers'
]

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError,StarletteHTTPException
from pydantic import ValidationError
from starlette.responses import JSONResponse

from sthg_common_base.response.httpCodeEnum import HttpStatus, ResponseEnum
from sthg_common_base.utils.constants import Constants
from sthg_common_base.utils.log_util import Logger, LoggerUtil

ERROR_TYPE_MAPPING = {
    "value_error.number.not_ge": "{},值不能小于:{}",
    "value_error.list.min_items": "{},元素个数至少为:{}",
    "value_error.str": "{},元素个数至少为:{}",
    "value_error.missing": "字段必填",
    "type_error.integer": "必须是整数类型",
    "value_error.number.not_gt": "必须大于 {limit_value}",
}

KeyErrorChineseDict = {
    "": ""
}

# 定义一个自定义异常类
class BaseException(Exception):
    code: int
    busiMsg: str
    busiCode: str

    def __init__(self, resEnmu: ResponseEnum, msg: str = None, *args):
        if msg and args:
            msg = msg.format(*args)
        self.code = resEnmu.getHttpCode
        self.busiCode = resEnmu.getBusiCode
        if msg:
            self.busiMsg = f"{resEnmu.getBusiMsg},{msg}"
        else:
            self.busiMsg = resEnmu.getBusiMsg

        super().__init__(self.busiMsg)

    def __call__(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.code,
            content={
                "code": self.code,
                "busiCode": self.busiCode,
                "busiMsg": self.busiMsg,
                "data": None,
            }
        )

class CustomException(BaseException):
    """自定义异常类，继承自 BaseException"""
    pass

def register_exception_handlers(app: FastAPI):
    # 覆盖原生 HTTPException 处理器（处理其他 HTTP 错误）
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        LoggerUtil.error_log(f"Unhandled http_exception_handler: {exc}")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "busiMsg": str(exc.detail),
                "busiCode": exc.status_code,
                "data":None
            },
        )

    # Pydantic 模型校验错误（如直接调用 Pydantic 模型时）
    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError):
        error_details = [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()]
        return JSONResponse(
            status_code=HttpStatus.BAD_REQUEST,
            content={
                "code": HttpStatus.BAD_REQUEST,
                "busiMsg": f"{ResponseEnum.InvalidRequest.getBusiMsg},{error_details}",
                "busiCode": ResponseEnum.InvalidRequest.getBusiCode,
                "data": None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        LoggerUtil.error_log(f"Unhandled validation_exception_handler: {exc}")
        error_messages = ""

        try:
            errors = exc.errors()
            error_messages = []
            for error in errors:
                error_type = error.get("type")
                msg_template = ERROR_TYPE_MAPPING.get(error_type, "{},验证失败")
                msg = msg_template.format(error_type + " " + error.get("msg"), error.get("ctx", {}).get("limit_value", ""))
                error_messages.append(msg)
        except Exception as ex:
            LoggerUtil.error_log(f"捕获异常逻辑失败: {ex}")

        return JSONResponse(
            status_code=HttpStatus.BAD_REQUEST,
            content={
                "code": HttpStatus.BAD_REQUEST,
                "busiMsg": "; ".join(error_messages),
                "busiCode": ResponseEnum.InvalidArgument.getBusiCode,
                "data": None
            },
        )

    # 自定义异常处理
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        LoggerUtil.error_log(f"Unhandled custom_exception_handler: {exc}")
        res = ResponseEnum.from_code(exc.busiCode)
        status_code = HttpStatus.INTERNAL_SERVER_ERROR
        busiMsg = ResponseEnum.InternalError.getBusiMsg
        busiCode = ResponseEnum.InternalError.getBusiCode
        if not res:
            status_code = res.getHttpCode
            busiMsg = res.getBusiMsg
            busiCode = res.getBusiCode

        return JSONResponse(
            status_code=status_code,
            content={
                "code": status_code,
                "busiMsg": busiMsg,
                "busiCode": busiCode,
                "data": None
            }
        )

    # 自定义异常处理
    @app.exception_handler(BaseException)
    async def custom_exception_handler(request: Request, exc: BaseException):
        LoggerUtil.error_log(f"Unhandled custom_exception_handler: {exc}")
        res = ResponseEnum.from_code(exc.busiCode)
        status_code = HttpStatus.INTERNAL_SERVER_ERROR
        busiMsg = ResponseEnum.InternalError.getBusiMsg
        busiCode = ResponseEnum.InternalError.getBusiCode
        if not res:
            status_code = res.getHttpCode
            busiMsg = res.getBusiMsg
            busiCode = res.getBusiCode

        return JSONResponse(
            status_code=status_code,
            content={
                "code": status_code,
                "busiMsg": busiMsg,
                "busiCode": busiCode,
                "data": None
            }
        )

    # 全局异常兜底处理
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # 记录完整的错误堆栈
        LoggerUtil.error_log(f"Unhandled exception: {exc}")

        return JSONResponse(
            status_code=ResponseEnum.InternalError.getHttpCode,
            content={
                "code": ResponseEnum.InternalError.getHttpCode,
                "busiMsg": ResponseEnum.InternalError.getBusiMsg,
                "busiCode": ResponseEnum.InternalError.getBusiCode,
                "data": None
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # 记录完整的错误堆栈
        uri = request.url.path
        if Constants.Favicon != uri:
            LoggerUtil.error_log(f"Unhandled exception: {uri},{exc}")

        return JSONResponse(
            status_code=ResponseEnum.InvalidRequest.getHttpCode,
            content={
                "code": ResponseEnum.InvalidRequest.getHttpCode,
                "busiMsg": exc.detail,
                "busiCode": ResponseEnum.InvalidRequest.getBusiCode,
                "data": None
            }
        )