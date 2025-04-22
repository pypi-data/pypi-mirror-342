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
import functools


# import xmltodict


def x_request_wrapper(func):
    '''
    请求参数解析装饰器。
    1、基于APIView类的入参进行解析，在原参数基础上，追加 current 请求体，request_params 请求参数两个入参。
    2、将适配多种body格式。兼容 APIView与View的情况，View 没有request.data
    示例：
    原参数：def get(self, request, *args, **kwargs)
    变为：def get(self, request, request_params, *args, **kwargs)
    '''

    @functools.wraps(func)  # 更新 wrapper 函数的 __name__、__doc__、__module__ 和 __annotations__ 属性
    def wrapper(instance, request=None, *args, **kwargs):
        """
        解析request参数，适配多种body格式。兼容 APIView与View的情况，View 没有request.data
        PS :注意使用该装饰器之后必搭配*args，**kwargs须使用
        @param instance 实例是一个继承APIView基类的实例
        @param request REST封装的Request实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        # print("> x_request_wrapper: wrapper: ", instance, request, args, kwargs)
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            current = instance
        if isinstance(request, WSGIRequest) or isinstance(request, Request) or isinstance(request, ASGIRequest):
            current = request
        if current is None:
            return func(instance, *args, request=current, request_params={}, **kwargs)

        # 参数解析
        content_type = current.META.get('CONTENT_TYPE', "").split(";")[0]
        method = current.method
        if content_type == "text/plain" or method == "GET":  # 不指定则默认这种content-type
            try:
                body = current.body.decode("utf-8")
                data = json.loads(body)
            except Exception as e:
                # 允许get请求的query参数传json格式字符串，如：?group_list=["basics","bid-online"]
                data = parse_json(current.GET.dict())
                if not data:
                    data = current.POST
                if not data:
                    data = {}
        elif content_type == "application/json":
            data = json.loads(current.body)
        elif content_type == "multipart/form-data":
            data = current.POST
        # elif content_type == "application/xml":
        #     try:
        #         data = xmltodict.parse(current.body)
        #         data = data.get("body") or data.get("data", {})
        #     except Exception as e:
        #         data = {}
        elif content_type == "application/x-www-form-urlencoded":
            data = parse_qs(current.body.decode())
            if data:
                data = {k: v[0] for k, v in data.items()}
            else:
                data = {}
        else:
            data = getattr(current, 'data', {})

        # 闭包抛出
        kwargs.pop("request_params", None)  # 避免重复执行报错
        kwargs.pop("current", None)  # 避免重复执行报错

        # 克隆参数
        copy_params = {k: v for k, v in data.items()}
        return func(instance, *args, request=current, request_params=copy_params, **kwargs)

    return wrapper


# json 结果集返回
def parse_json(result):
    if result is None:
        return None

    if type(result) is str:
        try:
            result = json.loads(result.replace("'", '"').replace('\\r', "").replace('\\n', "").replace('\\t', "").replace('\\t', ""))
        except Exception as e:
            return result
    if type(result) is list:
        for i, v in enumerate(result):
            result[i] = parse_json(v)
    if type(result) is dict:
        for k, v in result.items():
            result[k] = parse_json(v)
    return result
