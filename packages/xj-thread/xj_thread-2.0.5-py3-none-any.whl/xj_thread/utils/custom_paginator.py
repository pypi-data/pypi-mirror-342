# coding: utf-8
import inspect

from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args


class CustomPaginator(Paginator):

    @cached_property
    def count(self):
        """
        重写Paginator类的count方法，并将结果数据缓存到数据库中
        """
        # print('> CustomPaginator: count!', self)
        table_name = self.object_list.model._meta.db_table
        key_name = f'table_{table_name}__count'
        # print('> CustomPaginator: key_name:', key_name)
        n = cache.get(key_name, default=None)  # 从缓存中读数据表总行数
        if n is not None:
            return n

        # 调整后的原始代码逻辑，重新计划数据表总行数
        fn = getattr(self.object_list, 'count', None)
        n = fn() if callable(fn) and not inspect.isbuiltin(fn) and method_has_no_args(fn) else len(self.object_list)
        # print('> CustomPaginator: n:', n)

        cache.set(key_name, n, timeout=86400)  # 写缓存，数据表总行数
        return n
