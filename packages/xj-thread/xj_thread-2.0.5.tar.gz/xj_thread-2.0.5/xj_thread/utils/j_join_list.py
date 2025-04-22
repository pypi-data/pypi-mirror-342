# encoding: utf-8
"""
@project: djangoModel->custom_merge
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户自定义 字典合并
@created_time: 2022/8/16 15:40
"""


class JJoinList:
    @staticmethod
    def join(l_list: list, r_list: list, l_key: str = "id", r_key: str = "id"):
        join_list = l_list.copy()
        r_map = {str(it.get(r_key)): it for it in r_list}
        for item in join_list:
            if str(item[l_key]) in r_map.keys():
                item.update(r_map[str(item[l_key])])
        return join_list
