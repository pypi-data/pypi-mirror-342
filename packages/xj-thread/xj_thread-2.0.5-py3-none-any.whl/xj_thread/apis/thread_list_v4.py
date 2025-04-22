"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块逻辑分发
"""

from rest_framework.views import APIView

from ..services.thread_category_tree_service import ThreadCategoryTreeServices
from ..services.thread_list_service_v2 import ThreadListService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, filter_fields_handler, filter_result_field
from ..utils.join_list import JoinList
from ..utils.dynamic_load_class import dynamic_load_class
from ..utils.user_wrapper import user_authentication_wrapper
from ..utils.j_transform_type import JTransformType


class ThreadListAPIView(APIView):
    """
    get: 信息表列表
    post: 信息表新增
    """

    # 我们更希望通过装饰器来做权限验证，这样可以更好的精简API层的代码量 2022.10.3 by Sieyoo
    @user_authentication_wrapper  # 如果有token则返回user_info，无则返回空
    @request_params_wrapper
    def get(self, *args, user_info=None, request_params, **kwargs):
        """
        信息列表
        修订：
        [2024.12.03] 第二版起，取消类别ID查找功能，只允许路径拼接类别值查找。
        """
        # print('> ThreadListAPIView:', user_info, request_params, kwargs)
        category_value = kwargs.get("category_value", None)
        id_list = kwargs.get("id_list", None)
        need_child = request_params.get('need_child', None)
        sort = request_params.get("sort", "-id")

        # 去除杂参
        non_queries = ["category_value", "id_list", "page", "size", "sort", "need_child"]
        query_params = {k: v for k, v in request_params.items() if k not in non_queries}
        # print('> ThreadListAPIView: query_params:', query_params)

        # 检查页号、行数
        page, page_err = JTransformType.to(request_params.get("page", 1), "int", 1)
        if page_err:
            return util_response(err=1000, msg=f"页号(page)不合法。{page_err}。")
        size, size_err = JTransformType.to(request_params.get("size", 10), "int", 10)
        if size_err:
            return util_response(err=1000, msg=f"行数(size)不合法。{size_err}。")
        if size > 100:
            return util_response(err=1000, msg="请求行数(size)不可以超过100条")


        # # 不用在这里写，ThreadListService 服务内自行处理
        # # ========== 获取子类别树 start ==========
        # # 如果category_value没传则查询全部
        # if need_child and not category_value:
        #     return util_response(msg="您需要搜索子类别(need_child)时，则类别(category_value)为必填项")
        # if need_child:
        #     category_ids, category_tree_err = ThreadCategoryTreeServices.get_child_ids(category_value=category_value)
        #     if category_tree_err:
        #         return util_response(err=1000, msg="获取类别子节点错误：" + category_tree_err)
        #     # print('> ThreadListAPIView: category_ids:', category_ids)
        #     query_params.setdefault("category_id_list", category_ids)
        # else:
        #     query_params.setdefault("category_id__value", category_value)
        # ========== 获取子类别树 end ==========

        # ========== 查询信息列表 ==========
        thread_serv, error_text = ThreadListService.list(
            category_value=category_value,
            id_list=id_list,
            query_params=query_params,
            page=page,
            size=size,
            sort=sort,
            need_child=need_child,
            need_auth=False,
        )
        # print('> ThreadListAPIView: thread_serv:', thread_serv)
        if error_text:
            return util_response(err=1002, msg=error_text)

        # # ======================= section 其他模块信息拼接 合并 start ================================
        # thread_id_list = list(set([item['id'] for item in thread_serv['list'] if item['id']]))
        # # 统计信息拼接
        # try:
        #     statistic_list = StatisticsService.statistic_list(id_list=thread_id_list)
        #     thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=statistic_list, l_key="id",
        #                                    r_key='thread_id').join()
        # except:
        #     pass
        # # 拼接用户信息
        # DetailInfoService, import_err = dynamic_load_class(import_path="xj_user.services.user_detail_info_service",
        #                                                    class_name="DetailInfoService")
        # if not import_err:
        #     with_user_id_list = list(
        #         set([item['with_user_id'] for item in thread_serv['list'] if item['with_user_id']]))
        #     with_user_info_list, err = DetailInfoService.get_list_detail(user_id_list=with_user_id_list,
        #                                                                  filter_fields=request_params.get(
        #                                                                      'filter_fields'))  # 请注意 返回协议存在问题
        #     thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=with_user_info_list, l_key="with_user_id",
        #                                    r_key='user_id').join()
        #
        #     thread_serv['list'] = filter_result_field(
        #         result_list=filter_result_field(  # 扩展字段替换
        #             result_list=thread_serv['list'],
        #             alias_dict={"nickname": "salesman"},
        #         ),
        #     )
        #
        #     user_id_list = list(set([item['user_id'] for item in thread_serv['list'] if item['user_id']]))
        #     user_info_list, err = DetailInfoService.get_list_detail(user_id_list=user_id_list,
        #                                                             filter_fields=request_params.get(
        #                                                                 'filter_fields'))  # 请注意 返回协议存在问题
        #     thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=user_info_list, l_key="user_id",
        #                                    r_key='user_id').join()
        #
        # UserGroupService, group_import_err = dynamic_load_class(import_path="xj_role.services.user_group_service",
        #                                                         class_name="UserGroupService")
        # if not group_import_err:
        #     group_id_list = list(set([item['group_id'] for item in thread_serv['list'] if item['group_id']]))
        #     group_list, group_err = UserGroupService.group_list(
        #         params={"id_list": group_id_list}
        #     )
        #     # print(group_list)
        #     thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=group_list['list'], l_key="group_id",
        #                                    r_key='id').join()
        #
        # # 判断是否需要展示定位信息
        # LocationService, import_err = dynamic_load_class(import_path="xj_location.services.location_service",
        #                                                  class_name="LocationService")
        # if request_params.get("need_location") and not import_err:
        #     location_list, err = LocationService.location_list(
        #         params={"thread_id_list": thread_id_list},
        #         need_pagination=False,
        #         filter_fields=[
        #             "name", "thread_id", "longitude", "latitude", "altitude", "coordinate_type"
        #         ]
        #     )
        #     if isinstance(location_list, list) and not err:
        #         thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=location_list, l_key="id",
        #                                        r_key='thread_id').join()
        # # ======================= section 其他模块信息拼接 合并 end ================================
        #
        # filter_fields = filter_fields_handler(
        #     default_field_list=[
        #         "group_name", "id", "category_name", "classify_name", "show_value", "title", "subtitle", "summary",
        #         "cover", "photos", "video", "author", "avatar", "username", "nickname", "region_code",
        #         "weight", "views", "plays", "comments", "likes", "favorite", "shares", "create_time", "update_time",
        #         'name', 'altitude', 'coordinate_type', 'longitude', 'created_time', 'region_code', 'latitude',
        #         'publish_time', "remark", "sort", "real_name"
        #     ],
        #     input_field_expression=request_params.get('filter_fields', None)
        # )
        # # 过滤出需要展示的字段
        # thread_serv['list'] = filter_result_field(
        #     result_list=thread_serv['list'],
        #     filter_filed_list=filter_fields,
        # )

        return util_response(data=thread_serv, is_need_parse_json=True)
