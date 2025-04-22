# encoding: utf-8
"""
@project: djangoModel->thread_category_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 类别api
@created_time: 2022/10/25 14:40
"""
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..services.thread_category_service import ThreadCategoryService
from ..services.thread_category_list_service import ThreadCategoryListService
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper


class ThreadCategoryListApis(APIView):
    # @api_view(['GET'])
    # @swagger_auto_schema(
    #     tags=['Thread Category 信息类别'],
    #     operation_summary="获取类别列表",
    #     responses={200: openapi.Response('成功响应', examples={'application/json': '{"key": "value"}'})},
    #     description="获取类别列表的描述",
    #     required=['category_value'],
    #     manual_parameters=[
    #         openapi.Parameter(name='category_value', in_=openapi.IN_QUERY, description='Search query',
    #                           type=openapi.TYPE_STRING),
    #         openapi.Parameter(name='need_child', in_=openapi.IN_QUERY, description='Number of items to return',
    #                           type=openapi.TYPE_BOOLEAN)
    #     ],
    #     properties={
    #         'category_value': openapi.Schema(type=openapi.TYPE_STRING),
    #         "need_child": "是否需要子类。默认 False"
    #     },
    # )
    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        """
        ## 获取类别列表
        ### Path:
        - category_value (str) 类别唯一值。必选
        ### Param:
        - id {bool} 类别ID。即将弃用
        - name {bool} 类别名称。支持模糊搜索
        - platform_code {str} 平台码
        - need_child {bool} 是否需要子类。默认 False
        - sort {enum<str>} 排序字段。默认 -id，可选 id, -id, sort, -sort
        - need_pagination {bool} 是否需要分页，默认 False
        - page {int} 页号。默认 1，要求启用 need_pagination
        - size {int} 页数。默认 10，要求启用 need_pagination
        ### Return:
        - list<category_dict>
        """
        need_child = request_params.pop("need_child", False)
        need_pagination = request_params.pop("need_pagination", False)
        request_params.setdefault("category_value", kwargs.get("category_value", None))

        data, err = ThreadCategoryListService.list(
            params=request_params,
            need_pagination=need_pagination,
            filter_fields=request_params.pop("filter_fields", None),
            need_child=need_child
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
