# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""
import logging
import re

from django.core.paginator import Paginator, EmptyPage
from django.db.models import F

from ..models import Thread
# from ..models import Thread, ThreadTagMapping, ThreadExtendField
from ..services.thread_extend_service_v2 import ThreadExtendService
from ..services.thread_auth_service import ThreadAuthService
from ..services.thread_category_service import ThreadCategoryService
from ..services.thread_category_tree_service import ThreadCategoryTreeServices

from ..utils.custom_tool import (
    filter_result_field,
    format_params_handle,
    force_transform_type,
    filter_fields_handler,
)
from ..utils.j_join_list import JJoinList
from ..utils.j_transform_type import JTransformType

log = logging.getLogger()


# 信息服务CURD(支持扩展字段配置)
class ThreadListService:
    # 查询字段说明
    __support_queries = {
        "access_level": "访问级别",
        "classify_parent_id": "分类父级id",
        "create_time_end|date": "创建开始时间",
        "create_time_start|date": "创建结束时间",
        "exclude_category_list": '''排除分类列表 使用 列表["real_name","sex","user_id"]   或者 使用";"分割''',
        "filter_fields": '''返回字段筛选，使用 列表["real_name","sex","user_id"] 或者 使用";"分割如：id;category_name，或者在默认的基础上新增使用***update_time;减少则!!!nickname;username''',
        "has_comment": "是否开启评论",
        "has_enroll": "开启报名",
        "has_fee": "开启小费",
        "id_list": "ID列表",
        "main_extend_field_1": "",
        # "need_auth": "是否需要权限",
        "need_child": "是否需要搜索子类别",
        "need_location": "申请获取信息的定位相关的信息",
        "page": "页号，默认第1页",
        "platform_code": "平台编码（绑定类别）",
        "size": "行数，默认10行",
        "sort": '''排序。支持["id", "-id", "sort", "-sort", "create_time", "-create_time", "update_time", "-update_time","publish_time", "-publish_time", ]''',
        "title": "标题",
        "user_id|int": "用户ID",
        "user_id_list|list": "",
    }

    # 导出字段列表
    __all_fields = [
        "id",
        "uuid",
        "is_delete",
        "category_id",
        "classify_id",
        "show_id",
        "region_code",
        "user_id",
        "with_user_id",
        "group_id",
        "thread_no",
        "title",
        "subtitle",
        # "content",  # 列表页禁止显示内容，会太长
        "summary",
        "access_level",
        "author",
        "ip",
        # "has_enroll",
        # "has_fee",
        # "has_comment",
        # "has_location",
        "cover",
        "photos",
        "video",
        "files",
        "price",
        "is_original",
        "link",
        "create_time",
        "update_time",
        "publish_time",
        # "logs",
        "remark",
        # "more",
        "sort",
        "language_code",
        "category_value",
        "category_name",
        # "need_auth",
        "classify_value",
        "classify_name",
        "show_value",
    ]

    # 搜索条件映射
    __condition_alias = {
        # "id_list": "id__in",
        "user_id_list": "user_id__in",
        # "category_id_list": "category_id__in",
        "category_value": "category__value",
        "category_parent_id": "category__parent_id",
        "platform_code": "category__platform_code",
        "classify_value": "classify__value",
        "classify_id_list": "classify__in",
        "classify_parent_id": "classify__parent_id",
        "title": "title__contains",
        "create_time_start": "create_time__gte",
        "create_time_end": "create_time__lte",
        "publish_time_start": "publish_time__gte",
        "publish_time_end": "publish_time__lte",
        "region_code": "region_code__regex",
    }

    # 默认字段类型。格式：字段名+管道声明符+类型，如id|int，默认str类型
    filter_filed_list = [
        # "id_list|list",
        "category_id|int",
        # "category_id_list|list",
        "category_name",
        "category_value",
        "category_parent_id|int",
        "platform_code",
        "classify_id|int",
        "classify_name",
        "classify_value",
        "classify_id_list|list",
        "classify_parent_id|int",
        "show_value",
        "user_id|int",
        "user_id_list|list",
        'user_uuid|str',
        "title",
        "region_code",
        "publish_time_start|date",
        "publish_time_end|date",
        "create_time_start|date",
        "create_time_end|date",
        "access_level",
        "has_enroll",
        "sort",
        "has_fee",
        "has_comment",
        # "need_auth",
        # "is_subitem_thread",
        "thread_no",
        "remark",
    ]

    thread_fields = [i.name for i in Thread._meta.fields] + [
        "category_id",
        "classify_id",
        "show_id",
    ]
    # todo: 迁移不支持在此执行list()强制转换，故需修改语法，否则迁移时报表不存在，已注释，并在方法中引用。20230824 by Sieyoo。
    # extend_fields = [i.get("field") for i in list(ThreadExtendField.objects.values("field").distinct())]

    @staticmethod
    def list(
            category_value: str = '',
            id_list: list = None,
            uuid_list: list = None,
            query_params: dict = None,
            page: int = 1,
            size: int = 10,
            sort: str = "-id",
            need_child: bool = False,
            need_auth: bool = False,
    ):
        """
        信息列表
        @param category_value 类别值
        @param id_list 信息id列表
        @param uuid_list 信息uuid列表
        @param query_params 筛选条件
        @param page 页号
        @param size 行数
        @param sort 排序
        @param need_child 需要子类列表
        @param need_auth 需要登陆权限
        @description
        [2024.12.03] 第二版起，取消exclude_category_list功能、直接改传参功能。
        [2024.12.03] 第二版起，只能分页显示、取消全部显示功能。
        """
        # print('> ThreadListService:', page, size, sort, need_auth, query_params, )


        # ========== 参数类型处理 ==========
        # 检查字段冲突
        if (id_list or uuid_list) and category_value:
            return None, f"查询字段冲突。当按信息ID列表(id_list, uuid_list)查询时，不能同时按类别值(category_value)查询，二者选一。"
        # 检查排序有效性
        sort_choices = ["id", "-id", "sort", "-sort", "create_time", "-create_time", "update_time", "-update_time",
                        "publish_time", "-publish_time", ]
        if sort not in sort_choices:
            return None, f"排序字段无效，可选值：{'、'.join(sort_choices)}。"

        # 去除杂参
        # non_queries = ["page", "size", "sort"]
        # query_params = {k: v for k, v in query_params.items() if k not in non_queries}

        # ========== 获取子类别树 ==========
        category_id_list = []
        if need_child and not category_value:
            return None, "您需要搜索子类别(need_child)时，则类别(category_value)为必填项"
        if need_child:
            category_id_list, err = ThreadCategoryTreeServices.get_child_ids(category_value=category_value)
            if err:
                return None, "获取类别子节点错误：" + err

        '''
        # 检查行政区码有效性。因为长度可能不统一，兼容处理使用正则匹配。
        region_code, err = JTransformType.to(params.get("region_code", None), "int")
        if region_code:
            query_params["region_code"] = re.sub("0.$", "", str(region_code))
        '''


        '''
        # ========== 标签搜索 ==========
        # TODO 修改建议修改主表，使用外键查询。
        tag_id_list = params.get("tag_id_list") if params.get("tag_id_list") else None
        if tag_id_list:
            try:
                id_list = params.pop("id_list", None)
                if not id_list or not isinstance(id_list, list):
                    id_list = []
                params["id_list"] = list(
                    set(
                        id_list
                        + ThreadTagMapping.objects.filter(
                            tag_id__in=tag_id_list
                        ).values_list("thread_id", flat=True)
                    )
                )
            except ValueError as e:
                log.error(f"信息表标签查询{e}")

        thread_set = Thread.objects.order_by(sort)
        '''

        # ==================== 准备执行查询列表 start ====================
        # 声明查询集
        thread_set = Thread.objects

        # 排序条件。
        thread_set = thread_set.order_by(sort)
        # 过滤已删除。注意：为空和0认为是未删除的数据，为1代表删除的
        thread_set = thread_set.exclude(is_delete=True)

        # 需要登陆权限。
        thread_set = thread_set.exclude(category_id__need_auth=not need_auth)
        # 如果need_child为假则查询全部
        if need_child:
            thread_set = thread_set.filter(category__id__in=category_id_list)
        elif id_list and len(id_list) > 0:
            thread_set = thread_set.filter(id__in=id_list)
        elif uuid_list and len(uuid_list) > 0:
            thread_set = thread_set.filter(uuid__in=id_list)
        else:
            thread_set = thread_set.filter(category__value=category_value)

        # 格式化日期。
        thread_set = thread_set.extra(select={
            "create_time": 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
            "update_time": 'DATE_FORMAT(update_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
            "publish_time": 'DATE_FORMAT(publish_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
        })

        # 新增连表字段。
        thread_set = thread_set.annotate(
            category_value=F("category_id__value"),
            category_name=F("category_id__name"),
            classify_value=F("classify_id__value"),
            classify_name=F("classify_id__name"),
            show_value=F("show_id__value"),
        )

        # 设置查询条件
        conditions = format_params_handle(
            param_dict=query_params,
            filter_filed_list=ThreadListService.filter_filed_list,
            alias_dict=ThreadListService.__condition_alias,
            split_list=["id_list", "classify_id_list", "user_id_list", ],
            is_remove_empty=True,
        )

        # print('> ThreadListService: conditions:', conditions)
        # 添加搜索条件。
        thread_set = thread_set.filter(**conditions)
        # 记录查询语句。
        thread_query = thread_set.query
        # ==================== 准备执行查询列表 end ====================

        # ========== 执行分页查询 ==========
        # 用分页器分页
        paginator = Paginator(thread_set, per_page=size)
        # 正式请求数据
        try:
            total = paginator.count
            # 页号溢出返回
            if page > paginator.num_pages:
                return {"page": page, "size": size, "total": total, "list": []}, None
            # 获取当前页。返回<Page>类
            paginator_set = paginator.page(page)
        except Exception as e:
            return None, "Error: thread_list_service.py - ThreadListService::list: " + \
                   e.__str__() + ", line:" + str(e.__traceback__.tb_lineno)

        # 更新类别总计（仅单独查找类别时才会生效）
        if need_child and category_value:
            ThreadCategoryService.set_total(category_value, total)

        # ========== 导出分页结果 ==========
        # 返回<QuerySet>列表。为了使用values方法
        main_set = paginator_set.object_list

        # 获取结果数据
        main_list = list(main_set.values(*ThreadListService.__all_fields))

        # print('> ThreadListService: main_list:', main_list)
        whole_list = main_list.copy()

        # 扩展字段数据
        thread_id_list = [it["id"] for it in main_list if it["id"]]
        # print('> ThreadListService: thread_id_list:', thread_id_list)

        # ===== 拼接扩展数据 =====
        extend_list, err = ThreadExtendService.get_extend_list(thread_id_list)
        # print(">>> ThreadItemService: extend_list", extend_list)
        if err:
            return None, err

        whole_list = JJoinList.join(whole_list, extend_list, l_key="id", r_key="thread_id")

        # ===== 权限可见字段 =====
        # TODO 允许外部传入auth_level参数
        all_auth_fields, err = ThreadAuthService.get_all_auth_fields(auth_level='EVERYONE', crud='R', is_list=True)
        # print(">>> ThreadItemService: all_auth_fields", all_auth_fields)
        # 逐行处理
        result_list = []
        for row in whole_list:
            auth_fields = all_auth_fields.get(str(row['category_id']))
            if not auth_fields:
                result_list.append(row)
                continue

            allow_fields = [it for it in auth_fields['allow_fields'] if it in row.keys()]
            ban_fields = [it for it in auth_fields['ban_fields'] if it in row.keys()]
            if not allow_fields:
                allow_fields = row.keys()

            # 列表减法，允许字段减去禁用字段
            filter_fields = [it for it in allow_fields if it not in ban_fields]
            # 字典减法，全部字段减去禁用字段
            result_item = {k: row.get(k, None) for k in filter_fields}
            result_list.append(result_item)

        return {
            "page": int(page),
            "size": int(size),
            "total": total,
            "list": result_list,
            "query": str(thread_query),
       }, None

    @staticmethod
    def search(
            id_list: list = None, need_map: bool = False, filter_fields: "list|str" = None
    ):
        """
        按照ID搜索信息
        :param id_list: 信息ID列表
        :param need_map: True: {"thead_id":thread_item,...}, False: [thread_item,....]
        :param filter_fields: 过滤字段
        :return: data, err
        """
        id_list, is_void = force_transform_type(variable=id_list, var_type="list")
        if not id_list:
            return [], None
        # 主表select字段筛选
        main_filter_fields = filter_fields_handler(
            input_field_expression=filter_fields,
            all_field_list=ThreadListService.thread_fields
                           + [
                               "thread_category_value",
                               "thread_category_name",
                               "category_value",
                               "category_name",
                               "need_auth",
                               "thread_classify_value",
                               "thread_classify_name",
                               "classify_value",
                               "classify_name",
                               "show_value",
                           ],
        )
        main_filter_fields = list(
            set(main_filter_fields + ["id", "category_id", "classify_id", "show_id"])
        )
        # 开始按过滤条件
        thread_set = Thread.objects.filter(id__in=id_list).extra(
            select={
                "create_time": 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                "update_time": 'DATE_FORMAT(update_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
            }
        )
        try:
            thread_set = thread_set.annotate(
                thread_category_value=F("category_id__value"),
                thread_category_name=F("category_id__name"),
                category_value=F("category_id__value"),
                category_name=F("category_id__name"),
                need_auth=F("category_id__need_auth"),
                thread_classify_value=F("classify_id__value"),
                thread_classify_name=F("classify_id__name"),
                classify_value=F("classify_id__value"),
                classify_name=F("classify_id__name"),
                show_value=F("show_id__value"),
            )
            thread_set = thread_set.filter(is_delete=0)
            # TODO 后期迭代计划：删除调thread前缀，与前端沟通一致 2023/3/29
            thread_set = thread_set.values(*main_filter_fields)
        except Exception as e:
            return None, "err:" + e.__str__()
        thread_set = list(thread_set)
        # 主表扩展字段替换
        thread_set, err = ThreadMainExtendService.replace_list_extend(thread_set)

        # ================= 扩展数据拼接  start=================
        extend_filed_fields = filter_fields_handler(
            input_field_expression=filter_fields,
            all_field_list=[
                i.get("field")
                for i in list(ThreadExtendField.objects.values("field").distinct())
            ],
        )
        if extend_filed_fields:
            thread_extend_list, err = ThreadExtendService.get_extend_info(
                thread_id_list=list(
                    set([item["id"] for item in thread_set if item["id"]])
                )
            )
            thread_extend_list = filter_result_field(
                result_list=thread_extend_list,
                filter_filed_list=list(set(extend_filed_fields + ["thread_id"])),
            )
            JoinList(
                thread_set, thread_extend_list, l_key="id", r_key="thread_id"
            ).join()
        # ================= 扩展数据拼接  end  =================

        # 由于有字段冲突，所以这里做一次字段别名处理
        finish_set = filter_result_field(
            result_list=thread_set,
            alias_dict={
                "price": "thread_price",
                "category": "category_id",
                "classify": "classify_id",
            },
        )
        # 以字典形式返回{"主键"：{数据...}}
        need_map, is_void = force_transform_type(
            variable=need_map, var_type="bool", default=False
        )
        if need_map:
            finish_set = {i["id"]: i for i in finish_set}
        return finish_set, None

    @staticmethod
    def search_ids(search_prams: dict = None, is_strict_mode: bool = False):
        """
        根据搜索条件查search_prams，询信息表ID
        :param is_strict_mode: 是否严格模式，如果严格模式则超过100条则不返回。非严格模式则进行返回前100条
        :param search_prams: 搜素参数
        :return: list, err
        """
        search_prams, is_void = force_transform_type(
            variable=search_prams, var_type="dict", default={}
        )
        # 定位搜索 因为长度可能不统一，兼容处理使用正则匹配。
        region_code, is_void = force_transform_type(
            variable=search_prams.pop("region_code", None), var_type="int"
        )
        if region_code:
            search_prams["region_code"] = re.sub("0.$", "", str(region_code))
        # 用于条件搜索
        search_prams = format_params_handle(
            param_dict=search_prams,
            filter_filed_list=[
                "title",
                "user_id",
                "subtitle",
                "access_level",
                "author",
                "has_enroll",
                "has_fee",
                "has_comment",
                "has_location",
                "is_original",
                "finance_invoicing_code",
                "category_value",
                "classify_value" "thread_category_value",
                "thread_classify_value",
                "platform_code",
                "need_auth",
                "show_value",
                "region_code",
            ],
            __condition_alias={
                "title": "title__contains",
                "subtitle": "subtitle__contains",
                "region_code": "region_code__regex",
            },
            is_remove_empty=True,
        )
        if not search_prams:
            return [], None
        thread_set = Thread.objects
        try:
            thread_set = (
                thread_set.annotate(thread_category_value=F("category__value"))
                    .annotate(category_value=F("category__value"))
                    .annotate(platform_code=F("category__platform_code"))
                    .annotate(need_auth=F("category__need_auth"))
                    .annotate(thread_classify_value=F("classify__value"))
                    .annotate(classify_value=F("classify__value"))
                    .annotate(show_value=F("show__value"))
                    .filter(is_delete=0)
            )
            thread_set = thread_set.filter(**search_prams)
            count = thread_set.count()

            # 严格模式进行查询保护，如果筛选条件超出100条,则不返回。
            if count >= 100 and is_strict_mode:
                return [], None
            thread_set = thread_set.values("id")

            # 如果非严格模式，则取前100条
            if count >= 100 and not is_strict_mode:
                thread_set = Paginator(thread_set, 100).page(1)
                thread_set = list(thread_set.object_list)
        except Exception as e:
            return None, "err:" + e.__str__()

        # 返回ID序列
        thread_id_list = [i["id"] for i in list(thread_set)]
        return thread_id_list, None
