# encoding: utf-8
"""
@project: djangoModel->thread_category_item_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 类别单条服务
@created_time: 2022/10/25 14:21
"""
from django.core.paginator import Paginator
from django.db.models import F, Q

from ..models import ThreadCategory
from ..services.thread_category_tree_service import ThreadCategoryTreeServices
from ..utils.custom_tool import format_params_handle, filter_fields_handler, force_transform_type


class ThreadCategoryListService():
    @staticmethod
    def list(params: dict = None, filter_fields: "str|list" = None, need_pagination: bool = True,
             need_child: bool = None):
        """
        类别。类似于版块大类的概念.
        用于圈定信息内容所属的主要类别
        :param params: 搜索参数
        :param filter_fields: 过滤字段
        :param need_pagination: 是否需要分页
        :param need_child: 是否查询该类别树下面的所有子类别
        :return: data, err
        """
        # 参数筛选
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        need_pagination, err = force_transform_type(variable=need_pagination, var_type="bool", default=False)
        show_all = params.get("show_all", False)
        sort = params.get("sort", "-id")
        sort = sort if sort and sort in ["-id", "-sort", "id", "sort"] else "-id"
        page, err = force_transform_type(variable=params.get("page", 1), var_type="int", default=1)
        size, err = force_transform_type(variable=params.get("size", 10), var_type="int", default=10)

        # 查询参数过滤，替换
        queries = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "platform_code", "value", "category_value", "name", "need_auth", "description",
                               "parent_id", "parent_value"],
            alias_dict={"name": "name__contains", "value": "category_value"}
        )

        # 是否查询子节点,分类的数量并不多所以可以进行where in 搜索。
        if need_child:
            category_id = params.get("id", None)
            category_value = params.get("category_value", None)
            if category_value or category_id:
                queries.pop('category_value')
                id_list, err = ThreadCategoryTreeServices.get_child_ids(
                    category_id=category_id,
                    category_value=category_value,
                    show_all=show_all
                )
                queries['id__in'] = id_list

        # 查询字段处理，得出可以返回字段列表
        filter_fields_list = filter_fields_handler(
            default_field_list=[
                'id',
                'parent_id',
                'parent_value',
                'platform_code',
                'category_value',
                'name',
                'description',
                'icon',
                'config',
                'total',
                'need_auth',
                'sort',
                'disable',
            ],
            input_field_expression=filter_fields
        )

        # 数据库orm查询
        category_set = ThreadCategory.objects.annotate(
            category_value=F('value'),
            parent_value=F("parent__value")
        ).order_by(sort)
        category_set = category_set.filter(**queries)
        thread_category_obj = category_set.values(*filter_fields_list)

        # 不需要分页展示全部数据
        if not need_pagination:
            if not thread_category_obj:
                return [], None
            return list(thread_category_obj), None

        # 分页展示
        count = thread_category_obj.count()
        finish_set = list(Paginator(thread_category_obj, size).page(page))
        return {'size': int(size), 'page': int(page), 'total': count, 'list': finish_set}, None

    @staticmethod
    def edit(params: dict = None, pk: int = None, search_params: dict = None):
        """
        类别修改
        :param params: 修改参数
        :param pk: 主键修改
        :param search_params: 批量修改入口
        :return: data, err
        """
        # 参数初始化
        if params is None and not isinstance(params, dict):
            params = {}
        try:
            pk = int(pk)
        except TypeError:
            pk = None
        # 判断是否存在可编辑得到参数
        if not pk and not search_params:
            return None, "没有可编辑的数据"
        params = format_params_handle(
            param_dict=params,
            is_remove_null=True,
            is_remove_empty=False,
            filter_filed_list=["platform_code", "value", "name", "need_auth", "description", "sort", "parent_id"]
        )
        # 搜索可修改的数据
        category_set = ThreadCategory.objects
        if pk:
            category_set = category_set.filter(id=pk)
        if search_params:
            category_set = category_set.filter(**search_params)
        # 不存在可修改的类别
        if not category_set:
            return None, "没找到可修改的数据"
        instance = category_set.update(**params)
        return instance, None

    @staticmethod
    def delete(pk: int = None, id_list: list = None):
        # 删除类别
        if not pk and not id_list:
            return None, "缺少ID或ID列表(id_list)字段"
        if pk and id_list:
            return None, "参数冲突，不能同时传入删除分类ID和分类ID列表字段"

        category_set = ThreadCategory.objects
        if pk:
            category_set = category_set.filter(id=pk)
        elif id_list:
            category_set = category_set.filter(id__in=id_list)

        if not category_set:
            return None, "没找到可删除的数据"
        category_id_list = [it.id for it in category_set]
        category_set.delete()
        return category_id_list, None

