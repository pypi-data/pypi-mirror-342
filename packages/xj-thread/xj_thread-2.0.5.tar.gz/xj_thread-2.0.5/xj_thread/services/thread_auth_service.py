# encoding: utf-8
"""
@project: djangoModel->thread_auth_service
@author: 赵向明
@Email: sieyoo@163.com
@synopsis: 信息访问权限服务
@created_time: 2024/12/03 20:19
"""
from django.db.models import F, Q

from ..models import ThreadAuthField, ThreadAuthType


class ThreadAuthService:
    @staticmethod
    def get_auth_fields(category_id: int, auth_level: str, crud: str = 'R', is_list: bool = False):
        """
        获取权限字段
        :param category_id: 类别ID
        :param auth_level 权限级别
        :param crud 增删查改
        :param is_list 是否列表
        :return: dict<allow_fields, ban_fields>, err
        """
        auth_fields = ThreadAuthField.objects.filter(category_id=category_id, auth_level__value=auth_level, crud=crud)\
            .filter(enable=True).filter(Q(is_list=is_list)|Q(is_list__isnull=not is_list))\
            .values('crud', 'allow_fields', 'ban_fields').first()
        if not auth_fields:
            return {'allow_fields': [], 'ban_fields': [], }, None

        allow_str = auth_fields['allow_fields'] if auth_fields.detail('allow_fields', '') else ''
        allow_fields = [it for it in allow_str.replace(" ", "").split(';') if it]

        ban_str = auth_fields['ban_fields'] if auth_fields.detail('ban_fields') else ''
        ban_fields = [it for it in ban_str.replace(" ", "").split(';') if it]
        ban_fields.append('is_delete')

        return {'allow_fields': allow_fields, 'ban_fields': ban_fields, }, None


    @staticmethod
    def get_all_auth_fields(auth_level: str, crud: str = 'R', is_list: bool = False):
        """
        获取所有权限字段
        :param auth_level 权限级别
        :param crud 增删查改
        :return: dict<category_id, auth_dict<allow_fields, ban_fields>>, err
        """
        auth_fields = ThreadAuthField.objects.filter(auth_level__value=auth_level, crud=crud) \
            .filter(enable=True).filter(Q(is_list=is_list) | Q(is_list__isnull=not is_list)) \
            .values('category_id', 'crud', 'allow_fields', 'ban_fields')

        categories_dict = {str(it['category_id']): it for it in auth_fields}
        for key, item in categories_dict.items():
            allow_str = item['allow_fields'] if item.get('allow_fields', '') else ''
            ban_str = item['ban_fields'] if item.get('ban_fields') else ''
            item['allow_fields'] = ([it for it in allow_str.replace(" ", "").split(';') if it])
            item['ban_fields'] = [it for it in ban_str.replace(" ", "").split(';') if it]
            item['ban_fields'].append('is_delete')

        return categories_dict, None
