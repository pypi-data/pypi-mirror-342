"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块逻辑分发
"""
from rest_framework.views import APIView

from ..services.thread_other_list_service import ThreadOtherListServices
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper
from ..utils.parse_data import parse_data

t = ThreadOtherListServices()


class CategoryListAPIView(APIView):
    """
    get:类别列表
    """

    @request_params_wrapper
    def get(self, request=None, request_params=None, *args, **kwargs):
        data, error_text = t.thread_category(request_params)
        return util_response(data=data)


class ClassifyListAPIView(APIView):
    """
    get:分类列表
    """

    def get(self, request, *args, **kwargs):
        request_params = parse_data(request)
        category_id = request_params.detail('category_id', None)
        category_value = request_params.detail('category_value', None)
        classify_id = request_params.detail('classify_id', None)
        classify_value = request_params.detail('classify_value', None)
        data, error_text = t.thread_classify(category_id=category_id, category_value=category_value, classify_id=classify_id, classify_value=classify_value)
        return util_response(data=data)


class ShowListAPIView(APIView):
    """
    get:展示类型列表
    """

    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}

        try:
            need_pagination = int(request_params.get("need_pagination", 0))
        except ValueError:
            need_pagination = 0

        data, error_text = t.thread_show(request_params, need_pagination)
        if error_text:
            return util_response(err=1000, msg=error_text)
        return util_response(data=data)


class AuthListAPIView(APIView):
    """
    get:访问权限列表
    """

    def get(self, request, *args, **kwargs):
        data, error_text = t.thread_auth()
        return util_response(data=data)


class TagListAPIView(APIView):
    """
    get:标签列表
    """

    def get(self, request):
        params = parse_data(request)
        data, error_text = t.thread_tag(params)
        return util_response(data=data)


class ThreadExtendFieldList(APIView):
    """扩展字段列表"""

    def get(self, request):
        params = parse_data(request)
        data, err = t.thread_extend_field_list(params)
        if err:
            return util_response(err=54555, msg=err)
        return util_response(data=data)
