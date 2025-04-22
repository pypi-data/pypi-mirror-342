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


# 请求参数解析
def parse_data(request):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
    method = request.method
    if content_type == "text/plain" or method == "GET":
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
        except Exception:
            data = request.GET
            if not data:
                data = request.POST
            if not data:
                data = {}
    elif content_type == "application/json":
        return json.loads(request.body)
    elif content_type == "multipart/form-data":
        data = request.POST
    # elif content_type == "application/xml":
    #     try:
    #         data = xmltodict.parse(request.body)
    #         return data.get("body") or data.get("data", {})
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
    return {k: v for k, v in data.items()}
