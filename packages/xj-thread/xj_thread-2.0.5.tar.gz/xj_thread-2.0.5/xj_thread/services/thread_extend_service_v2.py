# encoding: utf-8
"""
@project: djangoModel->extend_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 扩展服务
@created_time: 2022/7/29 15:14
"""
from django.db.models import F

from ..models import ThreadExtendField, Thread, ThreadExtendData, ThreadCategory
from ..utils.custom_tool import write_to_log, force_transform_type, filter_result_field, format_params_handle


# TODO 后面的版本会删除ThreadExtendInputService 和 ThreadExtendOutPutService
# 服务提供 扩展表的字段映射关系，返回映射后KEY名。
# 达意最好是ThreadExtendInsertService:
class ThreadExtendInputService:
    thread_extend_filed = None

    def __init__(self, form_data):
        """
        :param form_data: 表单
        :param need_all_field: 是否需要全部的扩展字段（查询的时候会用到）
        """
        self.form_data = form_data
        self.form_data['category_id_id'] = self.form_data.pop("category_id", None)
        self.form_data['classify_id_id'] = self.form_data.pop("classify_id", None)
        # 新增或者修改的时候
        self.thread_extend_filed = {}
        category_id = None
        if "id" in self.form_data.keys():  # 修改时候：传了id,没有传classify_id
            category_id = Thread.objects.filter(id=self.form_data.detail('id')).first().category_id

        if self.form_data.detail('category_id_id', None):
            category_id = self.form_data.detail('category_id_id')

        if category_id:
            self.thread_extend_filed = {
                item["field"]: item["field_index"] for item in
                ThreadExtendField.objects.filter(category_id_id=category_id).values('field', 'field_index')
            }

    # 请求参数转换
    # TODO 弃用 sieyoo
    def transform_param(self):
        # 没有定义扩展映射直接返回，不进行扩展操作
        if self.thread_extend_filed is None:
            return self.form_data, None
        extend_data = {self.thread_extend_filed[k]: self.form_data.pop(k) for k, v in self.form_data.copy().items() if
                       k in self.thread_extend_filed.keys()}
        return self.form_data, extend_data


# 所有的输出信息服务都需要有统一的公共方法
# 暂时定位 output
class ThreadExtendOutPutService():
    # extend_field:扩展数据表的字段如field_1,field_2....
    # field:配置的字段映射
    field_list = None
    extend_field_map = None  # {extend_field:field}
    field_map = None  # {field:extend_field}
    finish_data = None  # 最终完成映射的扩展数据字典

    def __init__(self, category_id_list=None, thread_id_list=None):
        if category_id_list is None:
            raise Exception("category_id_list 必传")
        if thread_id_list is None:
            raise Exception("thread_id_list 必传")
        self.category_id_list = category_id_list
        self.thread_id_list = thread_id_list

        # 字段映射关系
        self.field_list = list(ThreadExtendField.objects.values())
        self.field_map = {}  # {i["category_id"]: {i["field_index"]: i["field"],....},....}
        for item in self.field_list:
            if self.field_map.get(item["category_id"]):
                self.field_map[item["category_id"]].update({item["field_index"]: item["field"]})
            else:
                self.field_map[item["category_id"]] = {item["field_index"]: item["field"]}

    def out_put(self):
        self.finish_data = {}  # 返回 self.finish_data：{thread_id:{扩展数据},.....} {thread_id:{扩展数据},.....}
        # 获取扩展数据
        extend_data = list(ThreadExtendData.objects.filter(thread_id__in=self.thread_id_list).annotate(
            category_id=F("thread_id__category_id")).values())
        extend_data = [(i.pop("thread_id_id"), i.pop("category_id"), i) for i in extend_data]
        # 扩展数据 替换KEY
        for thread_id, category_id, item in extend_data:
            category_field = self.field_map.get(category_id, None)
            if category_field is None:
                continue
            remove_none = {k: v for k, v in item.items() if v}
            temp_dict = {}
            for k, v in remove_none.items():
                if category_field.get(k):
                    temp_dict.update({category_field[k]: v})
            self.finish_data[thread_id] = temp_dict
        return self.finish_data

    def merge(self, merge_set, merge_set_key='id'):
        # 把结果集和{thread_id:{扩展数据}}，拼接到 merge_set
        extend_map = self.out_put()
        for item in merge_set:
            if item.detail(merge_set_key) and extend_map.get(item[merge_set_key]):
                item.update(extend_map[item[merge_set_key]])
        return merge_set


# 扩展字段增删改查
class ThreadExtendService:
    __number_fields = ["field_1", "field_2", "field_3", "field_4", "field_5",
                       "field_6", "field_7", "field_8", "field_9", "field_10", ]
    __char_fields = ["field_11", "field_12", "field_13", "field_14", "field_15",
                     "field_16", "field_17", "field_18", "field_19", "field_20", ]
    __text_fields = ["field_21", "field_22", ]
    # 扩展类型
    extend_types = ['str', 'int', 'bool', 'float', 'dict', 'list', 'date']
    __all_extend_fields = __number_fields + __char_fields + __text_fields
    extend_fields = []

    def __init__(self, category_id: int):
        if not category_id:
            self.extend_fields = []
        else:
            self.extend_fields = list(ThreadMainExtendField.objects.filter(category_id=category_id).values(
                "id", "category_id", "field", "field_index", "value", "type", "unit", "config", "default"
            ))

    @staticmethod
    def get_extend_fields(category_value: str = None) -> list:
        """
        获取指定类别下的扩展字段配置
        @param category_value 类别唯一值
        @return list<dict>
        """
        extend_set = ThreadExtendField.objects.filter(enable=True)
        if category_value:
            extend_set = extend_set.filter(category__value=category_value)
        extend_configs = list(extend_set.values())
        return extend_configs, None

    @staticmethod
    def get_extend_item(thread_uuid: str, category_value: int):
        """
        获取指定信息ID和类别后的一行扩展字段数据
        @param thread_uuid 信息UUID
        @param category_value 类别值
        @return list<dict>
        """
        extend_data = ThreadExtendData.objects.filter(thread_uuid=thread_uuid).values().first()
        if not extend_data:
            return None, None
        # 指定类别下的扩展字段配置
        extend_fields, error_text = ThreadExtendService.get_extend_fields(category_value)
        # 转换成field_x为键名、配置为值的扩展字段字典
        field_indexes = {it["field_index"]: it for it in extend_fields}
        # 根据扩展字段并更名，提取有效的结果字段
        result_item = {field_indexes[k]["field"]: v for k, v in extend_data.items() if field_indexes.get(k)}

        return result_item, None

    @staticmethod
    def get_extend_list(thread_id_list: list):
        extend_data_table = ThreadExtendData.objects.filter(thread_id__in=thread_id_list).values()
        if not extend_data_table:
            return [], None
        # print("> ThreadExtendService: extend_data_table:", extend_data_table)
        # 获取所有字段配置
        extend_fields, error_text = ThreadExtendService.get_extend_fields()
        # print("> ThreadExtendService: extend_fields:", extend_fields)
        # 转换成field_x为键名、配置为值的扩展字段字典。数据类型：dict<category_id, dict<field_x, config>>
        category_indexes = {str(cid): {} for cid in set([it['category_id'] for it in extend_fields])}
        for it in extend_fields:
            category_indexes[str(it["category_id"])].setdefault(it["field_index"], it)
        # print("> ThreadExtendService: category_indexes:", category_indexes)
        # 根据扩展字段并更名，提取有效的结果字段。
        result_list = []
        for row in extend_data_table:
            # 类别ID。字符串类型
            cid = str(row['category_id'])
            # 扩展字段配置。dict<field_x, config>类型
            field_indexes = category_indexes[cid]
            if not field_indexes:
                continue
            result_item = {field_indexes[k]["field"]: v for k, v in row.items() if field_indexes.get(k)}
            result_item.update({'thread_id': row['thread_id'], 'category_id': row['category_id'], })
            result_list.append(result_item)
        # print("> ThreadExtendService: result_list:", result_list)

        return result_list, None

    def format_params_beforehand(self):
        """
        数据过滤预先处理
        :return:(filter_filed_list,alias_dict), err_info
        """
        # 获取过滤字段以及映射字典
        alias_dict = {}
        filter_filed_list = []
        for field in self.extend_fields:
            if not field["field_index"] in ThreadExtendService.__all_extend_fields:
                continue
            filter_filed_key = field["field"] + (f'|{field["type"]}' if field["type"] and field["type"] in self.extend_types else
                                             "|float" if field["field_index"] in ThreadExtendService.__number_fields
                                             else "|str")
            filter_filed_list.append(filter_filed_key)
            alias_dict[field["field"]] = field["field_index"]
        return (filter_filed_list, alias_dict), None

    def validate(self, params: dict):
        """
        验证长度验证，默认值处理
        :return: params
        """
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        if err:
            return params, err

        field_map = {i["field_index"]: i for i in self.extend_fields if
                     i["field_index"] in ThreadExtendService.__all_extend_fields}
        for field_index, map in field_map.items():
            # 判断字符串字段是否超出长度
            if params.detail(field_index) and field_index in self.__char_fields and len(
                    params.detail(field_index)) > 255:
                return None, (map.detail("field") + " 长度不可以超过255个字符串")

            # 如果该字段为空或者未传，又配置了扩展字段德默认值，则字段进行赋值
            elif (not params.detail(field_index) and map.detail("default")):
                params[field_index] = map.detail("default")

        return params, None

    @staticmethod
    def replace_list_extend(result_list: list):
        """
        转换主表的扩展字段
        :param result_list: 列表字典
        :return: data,err
        """
        try:
            main_extend_list = list(ThreadExtendField.objects.all().values(
                "id", "category_id", "field", "field_index", "value", "type", "unit", "config", "default"
            ))
            main_extend_category_map = {}
            for i in main_extend_list:
                if not main_extend_category_map.get(i["category_id"]):
                    main_extend_category_map[i["category_id"]] = {i["field_index"]: i["field"]}
                else:
                    main_extend_category_map[i["category_id"]][i["field_index"]] = i["field"]

            new_result_list = []
            for result in result_list:
                result = format_params_handle(
                    param_dict=result,
                    is_remove_null=False,
                    alias_dict=main_extend_category_map.get(result["category_id"], {})
                )
                result = format_params_handle(
                    param_dict=result,
                    is_remove_null=False,
                    remove_filed_list=ThreadMainExtendService.__all_extend_fields
                )
                new_result_list.append(result)
            return new_result_list, None

        except Exception as e:
            return result_list, str(e)

    @staticmethod
    def create_or_update(thread_uuid:str, category_value: str, params:dict):
        """
        信息表扩展信息新增或者修改。本方法不必检查thread_uuid存在
        :param thread_uuid: 信息UUID，必填
        :param category_value: 分类值, 非必填
        :param params: 扩展数据，必填
        :return: None，err
        """
        # 获取扩展配置
        expend_configs, error = ThreadExtendService.get_extend_fields(category_value=category_value)
        if error:
            return None, error
        expend_fields = [it['field'] for it in expend_configs]
        expend_dict = {k:v for k,v in params.items() if k in expend_fields}
        if len(expend_dict.keys()) == 0:
            return {}, error

        # 获取历史数据
        extend_set = ThreadExtendData.objects.filter(thread_uuid=thread_uuid).filter()
        if not extend_set:
            extend_set = ThreadExtendData()
            extend_set.thread = Thread.objects.filter(uuid=thread_uuid).first()
            extend_set.thread_uuid = thread_uuid
            extend_set.category = ThreadCategory.objects.filter(value=category_value).first()

        # 添改数据写入。如有默认值则写默认值
        # extend_aliases = {it['field']: it['field_index'] for it in expend_configs}
        for it in expend_configs:
            if it['field'] in expend_fields or it['default'] is not None:
                setattr(extend_set, it['field'], expend_dict.get('field', it['default']))
        extend_set.save()
        return extend_set.to_json(), None

