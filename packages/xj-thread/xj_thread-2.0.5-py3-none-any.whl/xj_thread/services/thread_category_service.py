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
from ..models import ThreadCategory
from ..services.thread_category_tree_service import ThreadCategoryTreeServices
from ..utils.custom_tool import format_params_handle, filter_fields_handler, force_transform_type
from ..utils.j_parameter import JParameter
from ..utils.j_parameter import JParameter

aliases = {'category_value': 'value'}


class ThreadCategoryService():
    __all_fields = ["id", "parent_id", "parent_value", "platform_code", "category_value", "name", "description",
                    "icon", "config", "total", "need_auth", "sort", "disable", ]
    __add_fields = ["parent_value", "category_value", "name", "description",
                    "icon", "config", "need_auth", "sort", "disable", ]
    __edit_fields = ["parent_value|str", "category_value|str", "name|str", "description|str",
                    "icon|str", "config|json", "need_auth|bool", "sort|int", "disable|bool", ]

    @staticmethod
    def add(params: dict = None):
        """
        添加类别接口服务
        @param params: {dict} 添加参数字典
        @return: dict, err
        """
        valid_params = {k: v for k, v in params.items() if k in ThreadCategoryService.__add_fields}
        valid_params = {aliases[k] if k in aliases.keys() else k: v for k, v in valid_params.items()}

        category_value = params.get("category_value")
        if not category_value:
            return None, "类别值必填"

        category_set = ThreadCategory.objects.filter(value=category_value).first()
        if category_set:
            return None, f"类别值{category_value}已经存在，请勿重复添加"

        parent_value = valid_params.get("parent_value")
        if parent_value:
            valid_params.pop('parent_value')
            parent_set = ThreadCategory.objects.filter(value=parent_value).first()
            if not parent_set:
                return None, f"父类别值{category_value}不存在"
            valid_params['parent_id'] = parent_set.id

        try:
            instance = ThreadCategory.objects.create(**valid_params)
            print()
        except Exception as e:
            return None, str(e)
        return instance.to_json(), None

    @staticmethod
    def detail(category_value: str):
        """
        类别。
        @param category_value {str} 类别值
        """
        if not category_value:
            return None, "缺少类别值"

        category_dict = ThreadCategory.objects.filter(value=category_value) \
            .annotate(category_value=F('value'), parent_value=F('parent__value')) \
            .values(*ThreadCategoryService.__all_fields).first()
        if not category_dict:
            return None, f"类别值({category_value})不存在"

        return category_dict, None

    @staticmethod
    def edit(category_value: str, params: dict = None):
        """
        类别修改
        :param params: 修改参数
        :param category_value: 类别值
        :param search_params: 批量修改入口
        :return: data, err
        """
        # 参数初始化
        if not category_value:
            return None, "类别值必填"
        if params is None and not isinstance(params, dict):
            params = {}

        valid_params = JParameter.format(
            params, ThreadCategoryService.__edit_fields, aliases=aliases, is_remove_null=True, is_remove_empty=False,)

        # 搜索可修改的数据
        category_set = ThreadCategory.objects.filter(value=category_value).first()
        if not category_set:
            return None, "找不到类别值"

        # 检查父类别存在
        if valid_params.get('parent_value'):
            parent_value = valid_params.pop('parent_value')  # 这里剔除数据，update无法连表赋值
            parent_set = ThreadCategory.objects.filter(value=parent_value).first()
            if not parent_set:
                return None, "找不到父类别值"
            category_set.parent = parent_set

        for k, v in valid_params.items():
            setattr(category_set, k, v)
        category_set.save()
        return None, None

    @staticmethod
    def delete(value: str):
        # 删除类别
        if not value:
            return None, "缺少类别值"

        category_set = ThreadCategory.objects.filter(value=value)
        if not category_set:
            return None, f"类别值({value})不存在"

        category_set.delete()
        return value, None

    @staticmethod
    def set_total(category_value: str, total: int):
        category_set = ThreadCategory.objects.filter(value=category_value)
        if not category_set:
            return None, '更新信息数时，类别值不存在' + category_value
        if category_set.first().total != total:
            category_set.update(total=total)
        return None, None
