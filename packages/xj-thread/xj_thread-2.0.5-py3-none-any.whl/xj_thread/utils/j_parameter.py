# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
import datetime
from .j_transform_type import JTransformType


class JParameter:
    # 处理字典：白名单、黑名单、别名、移除空值、筛选类型
    @staticmethod
    def format(
        source: dict,
        filter_fields: list = None,
        remove_fields: list = None,
        aliases: dict = None,
        split_fields: list = None,
        split: str = ";",
        is_remove_null: bool = False,
        is_remove_empty: bool = False,
        date_format_dict: dict = None,
        is_validate_type: bool = False,
    ) -> dict:
        """
        字段筛选并替换成别名
        @param source: {dict} 来源参数
        @param filter_fields: {list<key>} 字段白名单。如 ["id|int", "uid"]
        @param remove_fields: {list<key>} 字段黑名单。["id", ...]
        @param aliases: {dict<source_key, target_key>} 字段别名。如 {"id": "user_id"}
        @param split_fields: {list<key>} 指定拆分字段。该参数为了适配使用符号分割成列表。["id_list", ...]
        @param split: {str} 字符串拆分依据。默认分号";"
        @param is_remove_null: {bool} 是否移除值为None字段。默认False
        @param is_remove_empty: {bool} 是否移除值为空值字段。即移除值为 "", 0, "0", None字段；value类型等于False的字段,
        @param date_format_dict: 日期格式化 日期列表，{field：(from_format,to_format),}如：{"field":("%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M:%S")}
        @param is_validate_type: 是否验证数据合法性
        @return: param_dict
        """

        result = source.copy()
        # 过滤字段并且得数据类型映射
        new_filter_fields = []  # 拆分字段类型的白名单
        must_type_map = {}  # 从白名单中拆分出字段与类型的映射
        if filter_fields and isinstance(filter_fields, list):
            for ff in filter_fields:
                key_type_pair = ff.split("|", 1)
                [key, key_type] = key_type_pair if len(key_type_pair) == 2 else [key_type_pair[0], None]  # 如果为类型None，则默认是字符串
                must_type_map[key] = key_type
                new_filter_fields.append(key)
            result = {k: v for k, v in result.items() if k in new_filter_fields and (not is_remove_empty or v) and (not is_remove_null or v is not None)}
        # 剔除字段
        if remove_fields and isinstance(remove_fields, list):
            result = {k: v for k, v in result.items() if not k in remove_fields and (not is_remove_empty or v) and (not is_remove_null or v is not None)}
        # 字段拆分
        if split_fields and isinstance(split_fields, list):
            result = {k: (str(v).split(split) if k in split_fields and not isinstance(v, list) else v) for k, v in result.copy().items()}
        # 类型转换
        if must_type_map and isinstance(must_type_map, dict):
            for k, v in result.copy().items():
                v, is_err = JTransformType.to(v, must_type_map.get(k, None))
                if is_err and not is_validate_type:
                    result.pop(k)
                elif is_err and is_validate_type:
                    raise ValueError(k + ":" + is_err)
                else:
                    # 覆盖掉转换的值
                    result[k] = v

        # 日期字段格式转换
        if date_format_dict and isinstance(date_format_dict, dict):
            for k, v in result.copy().items():
                if not date_format_dict.get(k):
                    continue
                try:
                    from_format, to_format = date_format_dict[k]
                    if not isinstance(v, datetime.datetime) and isinstance(v, str):
                        parse_date_obj = datetime.datetime.strptime(v, from_format)
                    else:
                        parse_date_obj = v
                    result[k] = parse_date_obj.strftime(to_format)
                except Exception as e:
                    pass

        # 别名替换
        if aliases and isinstance(aliases, dict):
            result = {aliases.get(k, k): v for k, v in result.copy().items()}

        return result
