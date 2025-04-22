# encoding: utf-8
"""
@project: djangoModel->thread_category_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 类别api
@created_time: 2022/10/25 14:40
"""
from rest_framework.views import APIView

from ..services.thread_category_service import ThreadCategoryService
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper


class ThreadCategoryApis(APIView):
    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        """
        获取一个类别
        - category_value {str} 类别值，必填
        """
        category_value = kwargs.get('category_value')
        data, err = ThreadCategoryService.detail(category_value)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def post(self, *args, request_params=None, **kwargs):
        data, err = ThreadCategoryService.add(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        pk = kwargs.get("pk") or request_params.get("id") or request_params.get("category_id")
        data, err = ThreadCategoryService.delete(pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def put(self, *args, request_params=None, **kwargs):
        category_value = kwargs.get('category_value')
        data, err = ThreadCategoryService.edit(category_value, request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
