# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
import json
from urllib.parse import parse_qs
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request
from ..utils.parse_json import parse_json
import functools
# import xmltodict


# 请求参数解析
def request_params_wrapper(func):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    @functools.wraps(func)  # 更新 wrapper 函数的 __name__、__doc__、__module__ 和 __annotations__ 属性
    def wrapper(instance, arg_request=None, *args, request=None, **kwargs):
        """
        解析request参数，适配多种body格式。
        PS :注意使用该装饰器之后必搭配*args，**kwargs须使用
        @param instance 实例是一个APIView的实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance, request, *args, request=request, request_params={}, **kwargs, )

        # 参数解析
        content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
        method = request.method
        if content_type == "text/plain" or method == "GET":  # 不指定则默认这种content-type
            try:
                body = request.body.decode("utf-8")
                data = json.loads(body)
            except Exception as e:
                # 允许get请求的query参数传json格式字符串，如：?group_list=["basics","bid-online"]
                data = parse_json(request.GET.dict())
                if not data:
                    data = request.POST
                if not data:
                    data = {}
        elif content_type == "application/json":
            data = json.loads(request.body)
        elif content_type == "multipart/form-data":
            data = request.POST
        # elif content_type == "application/xml":
        #     try:
        #         data = xmltodict.parse(request.body)
        #         data = data.get("body") or data.get("data", {})
        #     except Exception as e:
        #         data = {}
        elif content_type == "application/x-www-form-urlencoded":
            data = parse_qs(request.body.decode())
            if data:
                data = {k: v[0] for k, v in data.items()}
            else:
                data = {}
        else:
            data = getattr(request, 'data', {})

        # 闭包抛出
        kwargs.pop("request_params", None)  # 避免重复执行报错
        kwargs.pop("request", None)  # 避免重复执行报错
        return func(instance, request, *args, request=request, request_params={k: v for k, v in data.items()}, **kwargs)

    return wrapper
