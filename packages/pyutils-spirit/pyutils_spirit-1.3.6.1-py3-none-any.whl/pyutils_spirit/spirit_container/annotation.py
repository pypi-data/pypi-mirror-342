# @Coding: UTF-8
# @Time: 2024/9/24 12:58
# @Author: xieyang_ls
# @Filename: annotation.py
from abc import ABC
from argparse import ArgumentTypeError

from http.server import BaseHTTPRequestHandler


def Get(path: str):
    if not isinstance(path, str):
        raise ValueError('GET Method: path should be a string')
    if len(path) == 0:
        raise ValueError('GET Method: path should not be empty')

    def decorator_get_func(func):
        func.__decorator__ = "GET"
        func.__decorator_path__ = path
        return func

    return decorator_get_func


def Post(path: str):
    if not isinstance(path, str):
        raise ValueError('POST Method: path should be a string')
    if len(path) == 0:
        raise ValueError('POST Method: path should not be empty')

    def decorator_post_func(func):
        func.__decorator__ = "POST"
        func.__decorator_path__ = path
        return func

    return decorator_post_func


def Put(path: str):
    if not isinstance(path, str):
        raise ValueError('PUT Method: path should be a string')
    if len(path) == 0:
        raise ValueError('PUT Method: path should not be empty')

    def decorator_put_func(func):
        func.__decorator__ = "PUT"
        func.__decorator_path__ = path
        return func

    return decorator_put_func


def Delete(path: str):
    if not isinstance(path, str):
        raise ValueError('DELETE Method: path should be a string')
    if len(path) == 0:
        raise ValueError('DELETE Method: path should not be empty')

    def decorator_delete_func(func):
        func.__decorator__ = "DELETE"
        func.__decorator_path__ = path
        return func

    return decorator_delete_func


def ExceptionAdvice() -> callable:
    def decorator_advice_func(other_cls) -> type:
        if not isinstance(other_cls, type):
            raise TypeError('ExceptionAdvice can only be applied to classes')
        other_cls.__decorator__ = "ExceptionAdvice"
        return other_cls

    return decorator_advice_func


def ThrowsException(ex_type: type):
    if not isinstance(ex_type, type):
        raise TypeError("ThrowsException: argument 'ex' must be a type")

    def decorator_throws_exception_func(func) -> callable:
        func.__decorator__ = "ThrowsException"
        func.__decorator_params__ = ex_type
        return func

    return decorator_throws_exception_func


def RequestInterceptor(interceptor_paths: set[str]) -> callable:
    if not isinstance(interceptor_paths, set):
        raise TypeError('RequestInterceptor: interceptor_paths must be a set')
    for interceptor_path in interceptor_paths:
        if not isinstance(interceptor_path, str):
            raise TypeError('RequestInterceptor: interceptor_paths must be a string set')

    def decorator_request_func(other_cls) -> type:
        if not isinstance(other_cls, type):
            raise TypeError('RequestInterceptor can only be applied to classes')
        other_cls.__decorator__ = "RequestInterceptor"
        other_cls.__decorator_params__ = interceptor_paths
        return other_cls

    return decorator_request_func


def InterceptorBefore() -> callable:
    def decorator_request_func(func) -> callable:

        def interceptor_before(it_self: object, request: BaseHTTPRequestHandler) -> tuple[int, bool]:
            if not isinstance(request, BaseHTTPRequestHandler) and not isinstance(it_self, BaseHTTPRequestHandler):
                raise ArgumentTypeError('InterceptorBefore: argument must be BaseHTTPRequestHandler Type')
            request.headers["X-Intercepted"] = "True"
            response_code, response_status = func(it_self, request)
            if not isinstance(response_code, int) or not isinstance(response_status, bool):
                err: str = 'InterceptorBefore: return value must be (response_code: int, response_status: bool)'
                raise ValueError(err)
            return response_code, response_status

        interceptor_before.__decorator__ = "InterceptorBefore"
        return interceptor_before

    return decorator_request_func


def InterceptorAfter() -> callable:
    def decorator_request_func(func) -> callable:
        def interceptor_after(it_self: object, request: BaseHTTPRequestHandler) -> None:
            if not isinstance(request, BaseHTTPRequestHandler) and not isinstance(it_self, BaseHTTPRequestHandler):
                raise ArgumentTypeError('InterceptorAfter: argument should be BaseHTTPRequestHandler Type')
            func(it_self, request)
            return None

        interceptor_after.__decorator__ = "InterceptorAfter"
        return interceptor_after

    return decorator_request_func
