# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""
import re
from django.db.models import F

from ..models import Thread, ThreadExtendField, ThreadCategory
from ..services.thread_extend_service_v2 import ThreadExtendService
from ..services.thread_auth_service import ThreadAuthService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_tool import (
    format_params_handle,
    force_transform_type,
)
from ..utils.j_transform_type import JTransformType
from ..utils.j_parameter import JParameter
from ..utils.j_ulid_field import JULIDField

from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_service import UserService

all_fields = [
    "id", "uuid", "thread_no",
    "category_id", "category_value", "category_name",
    "classify_id", "classify_value", "classify_name",
    "show_id", "show_value", "show_name",
    "user_id", "user_uuid", "with_user_id", "group_id",
    "title", "subtitle", "summary", "content", "content_coding", "author",
    "access_level", "region_code", "ip",
    # "has_enroll", "has_fee", "has_comment", "has_location",
    "cover", "photos", "video", "files",
    "price", "is_original", "link", "keywords",
    "logs", "more",
    "sort", "language_code", "remark",
    "create_time", "update_time", "publish_time",
    "is_delete",
]
add_fields = [
    "thread_no",
    # "category_id", "category_value",
    "classify_id", "show_id", "group_id",
    # "user_id", "user_uuid", "with_user_uuid",
    "title", "subtitle", "summary", "content", "keywords",  # "content_coding",
    "access_level", "author", "region_code",
    "cover", "photos", "video", "files",
    "price", "is_original", "link",
    "logs", "more",
    "sort", "language_code", "remark",
    "create_time", "update_time", "publish_time",
    "is_delete",
]
edit_fields = [
    "thread_no",
    # "category_value",
    "classify_id", "show_id", "group_id",
    "user_uuid", "with_user_uuid",
    "title", "subtitle", "summary", "content", "keywords",  # "content_coding",
    "access_level", "author", "region_code",
    "cover", "photos", "video", "files",
    "price", "is_original", "link",
    "logs", "more",
    "sort", "language_code", "remark",
    "create_time", "update_time", "publish_time",
    "is_delete",
]
format_fields = [
    "id|int",
    "uuid|int",
    "thread_no",
    "category_value|str",
    "classify_id|int",
    "show_id|int",
    "group_id|int",
    # "user_id|int",
    "user_uuid|str",
    # "with_user_id|int",
    "with_user_uuid|str",
    "title|str",
    "subtitle|str",
    "summary|str",
    "content|str",
    "keywords|str",
    "access_level|int",
    "author|str",
    "region_code|int",
    "ip|str",
    "cover|str",
    "photos|dict",
    "video|str",
    "files|dict",
    "price|float",
    "is_original|bool",
    "link|str",
    "logs|dict",
    "more|dict",
    "sort|int",
    "language_code|str",
    "create_time|date",
    "update_time|date",
    "publish_time|date",
    "remark|str",
]

aliases = {
    "category_value": "category__value",
}


class ThreadItemService:
    """
    信息表新增、修改、详情服务
    """

    # todo: 迁移不支持在此执行list()强制转换，故需修改语法，否则迁移时报表不存在，已注释，但该变量未使用？20230824 by Sieyoo。
    # extend_fields = [i.get("field") for i in list(ThreadExtendField.objects.values("field").distinct())]

    @staticmethod
    def add(user_uuid: str, category_value: str, params: dict = None, **kwargs):
        """
        信息添加
        :param user_uuid: 用户UUID
        :param category_value: 信息类别值
        :param params: 添加参数子字典
        :param kwargs:
        :return:
        """
        # 参数整合与空值验证
        whole, is_void = JTransformType.to(params, "dict", {})
        args, is_void = JTransformType.to(kwargs, "dict", {})
        whole.update(args)
        # print(">>> whole:", whole)

        # 检查类别参数
        # category_value = whole.get("category_value")
        if not category_value:
            return None, f"类别值({category_value})必填。"
        # if type(category_value) is not str:
        #     return None, f"类别值({str(category_value)})非字符串。"
        category_set = ThreadCategory.objects.filter(value=category_value).first()
        # print(">>> category_set:", category_set)
        if not category_set:
            return None, f"类别值({category_value})不存在。"
        category_value = category_set.value

        # 检查扩展参数
        extend_fields = ThreadExtendService.get_extend_fields(category_value)
        # print(">>> extend_fields:", extend_fields)

        # 检查用户参数
        # if not whole.get("user_uuid") and not whole.get("user_id"):
        #     return None, "用户码(user_uuid)必填。(备用user_id)"
        if not user_uuid:
            return None, f"用户UUID({user_uuid})必填。"

        query_params = JParameter.format(whole, filter_fields=format_fields)
        query_params = {k: v for k,v in query_params.items() if k in add_fields}
        # print(">>> query_params:", query_params)

        # IO操作
        # try:
        # 主表插入数据
        thread_set = Thread.objects.create(
            uuid=JULIDField.get_u12(),  # TODO 不给uuid传值, 相同接口会报重复uuid, 找不到原因
            user_uuid=user_uuid,
            category_id=category_set.id,
            **query_params,
        )
        # print(">>> thread_set:", thread_set)
        # 扩展表 插入或更新
        # add_extend_res, err = ThreadExtendService.create_or_update(
        #     whole, thread_set.id
        # )
        # except Exception as e:
        #     return (
        #         None,
        #         f"""{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(e.__traceback__.tb_lineno)}""",
        #     )

        # print(">>> ThreadItemService::add: thread_set:", thread_set)
        # return {"id": thread_set.id, "title": thread_set.title}, None
        return thread_set.to_json(), None

    @staticmethod
    def detail(pk: int = None, uuid: str = None, auth_level: str = None):
        """
        获取信息内容
        :param pk: 信息表主键ID
        :param uuid: 信息表主键UUID
        :param auth_level: 信息表主键访问权限
        :return: data_dict,err
        """
        # print(">>> ThreadItemService::detail：", pk, uuid)
        if pk is None and uuid is None:
            return None, "缺少UUID 或 ID字段。"

        main_set = Thread.objects;
        if uuid:
            main_set = main_set.filter(uuid=uuid)
        else:
            main_set = main_set.filter(id=pk)

        # ===== 查找主表数据 =====
        main_item = main_set.annotate(
            category_value=F("category__value"),
            category_name=F("category__name"),
            category_platform_code=F("category__platform_code"),
            classify_value=F("classify__value"),
            classify_name=F("classify__name"),
            show_value=F("show__value"),
            show_name=F("show__name"),
        ).extra(
            select={
                "uuid": 'REPLACE(uuid, "-", "")',
                "update_time": 'DATE_FORMAT(update_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                "create_time": 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                "publish_time": 'DATE_FORMAT(publish_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
            }
        )
        main_query = main_item.query
        # print(">>> ThreadItemService: main_query", main_query)
        main_item = main_item.values(*all_fields).first()

        # print(">>> ThreadItemService: main_item", main_item)

        if not main_item:
            return None, f"数据不存在，uuid：{str(uuid)}。"
        if main_item.get("is_delete", False):
            return None, f"该数据已删除。"
        # 存储完整数据
        whole_item = main_item.copy()

        # ===== 拼接扩展数据 =====
        extend_item, err = ThreadExtendService.get_extend_item(main_item.get('uuid'), main_item.get('category_value'))
        # print(">>> ThreadItemService: extend_item", extend_item)
        if extend_item:
            whole_item.update(extend_item)

        # ===== 拼接用户信息 =====
        user_uuid = main_item.get("user_uuid", None)
        # print(">>> ThreadItemService: user_uuid", user_uuid)
        user_dict, err = UserService.detail(user_uuid)
        user_info_dict, err = DetailInfoService.get_detail(user_id=user_uuid)
        # print(">>> ThreadItemService: user_info_dict", user_info_dict)
        # if not user_info_dict:
        #     return None, f"用户不存在。({str(main_item['user_uuid'])})"
        if user_info_dict:
            aliases = {
                "tags": "user_tags",
                "sex": "user_sex",
                "signature": "user_signature",
                "uuid": "user_uuid",
            }
            user_item = {(aliases[k] if aliases.get(k) else k): v for k, v in user_info_dict.items() if k not in whole_item.keys()}
            # print(">>> ThreadItemService: user_item", user_item)
            whole_item.update(user_item)

        # ===== 拼接统计更新 =====
        statistic_list = StatisticsService.statistic_list(id_list=[main_item.get('id')])
        if isinstance(statistic_list, list) and len(statistic_list) == 1:
            whole_item.update(statistic_list[0])

        # ===== 权限可见字段 =====
        # TODO 允许外部传入auth_level参数
        auth_fields, err = ThreadAuthService.get_auth_fields(main_item.get('category_id'), auth_level='EVERYONE',
                                                             crud='R')
        # print(">>> ThreadItemService: auth_fields", auth_fields)
        allow_fields = [it for it in auth_fields['allow_fields'] if it in whole_item.keys()]
        ban_fields = [it for it in auth_fields['ban_fields'] if it in whole_item.keys()]
        if not allow_fields:
            allow_fields = whole_item.keys()

        # 列表减法，允许字段减去禁用字段
        filter_fields = [it for it in allow_fields if it not in ban_fields]
        # print(">>> ThreadAuthService: filter_fields", filter_fields)
        # 字典减法，全部字段减去禁用字段
        result_item = {k: whole_item.get(k, None) for k in filter_fields}

        return result_item, None

    @staticmethod
    def edit(pk: int = None, uuid: str = None, params: dict = None):
        """
        信息编辑服务
        :param pk: 信息表需要修改的主键
        :param uuid: 信息表需要修改的主键UUID
        :param params: 信息编辑的字段
        :return: instance，error
        """
        # print("> ThreadItemService:", pk, uuid, params)

        if pk is None and uuid is None:
            return None, "缺少UUID 或 ID字段。"

        # 参数转换校验
        params, error = JTransformType.to(params, "dict", {})
        if error:
            return None, error

        # 检查受否是有效的信息主键
        exist_set = Thread.objects;
        if uuid:
            exist_set = exist_set.filter(uuid=uuid)
        else:
            exist_set = exist_set.filter(id=pk)
        exist_set = exist_set.first()
        # print('> ThreadItemService::edit: exist_set:', exist_set)
        if not exist_set:
            return None, f"信息({uuid or id})不存在，无法进行修改"

        # 获取类别
        category_value = params.get('category_value') or exist_set.category.value
        category_set = ThreadCategory.objects.filter(value=category_value).first()
        if not category_set:
            return None, f"编辑信息内容中的类别值{category_value}不存在"

        # 主表修改。写入数据库
        main_params = {k: v for k, v in params.items() if k in edit_fields}
        main_params = JParameter.format(main_params, filter_fields=format_fields, is_remove_null=True)
        # print("> ThreadItemService::edit: main_params:", main_params)

        for k, v in main_params.items():
            if k not in ['category_value']:
                setattr(exist_set, k, v)
        exist_set.category = category_set
        exist_set.save()
        # print("> ThreadItemService::edit: exist_set:", type(exist_set), exist_set.to_json())

        # 检查信息UUID
        if not exist_set.uuid:
            return None, f"信息内容中未设置UUID，请联系管理员添加"

        # 扩展数据修改
        expend_result, error = ThreadExtendService.create_or_update(exist_set.uuid, exist_set.category.value, params.copy())
        if error:
            return None, error

        return exist_set.to_json(), None

    @staticmethod
    def delete(pk: int = None):
        """
        软删除信息
        :param pk: 主键ID
        :return: None,err
        """
        pk, is_void = force_transform_type(variable=pk, var_type="int")
        if not pk:
            return None, "非法请求"
        main_res = Thread.objects.filter(id=pk, is_delete=0)
        if not main_res:
            return None, "数据不存在，无法进行删除"

        main_res.update(is_delete=1)
        return None, None
