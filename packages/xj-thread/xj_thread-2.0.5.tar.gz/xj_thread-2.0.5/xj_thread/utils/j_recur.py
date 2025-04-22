# _*_coding:utf-8_*_
import re


class JRecur:

    # 该方法和create_forest功能基本一致呢，区别是一个是单树，一个是多树
    @staticmethod
    def create_tree(source_list, search_root_key, search_root_value, primary_key="id", parent_key="parent_id", children_key='children'):
        """
        生成树（一颗树）
        @param source_list 需要生成的来源数据列表
        @param search_root_key 需要从列表中搜索的树根节点键名
        @param search_root_value 需要从列表中搜索的树根植
        @param primary_key 指定主键名
        @param parent_key 指定父键名
        @param children_key 指定子键名
        """
        # print("> JRecur.create_tree:", search_root_key, search_root_value)
        # 遍历列表，把数据存放在dict里
        result_tree = {}
        source_index_dict = {}  # 父ID为键名组成的源字典，用于快速索引。里面的值均为列表
        for item in source_list:
            # 查找到树根。因为不知道哪个是被搜索项，所以在遍历时顺便找一下（只是顺便，其实也可以做两次for来解决）
            if str(item.get(search_root_key, '')) == str(search_root_value):
                result_tree = item

            # 边界检查：如果没有父类别，不需要生成索引列表字典
            if not item.get(parent_key, None):
                continue
            # 父ID的字符串
            pid = str(item[parent_key])
            # 边界检查：如果索引未创建，则初始化
            if not source_index_dict.get(pid, None):
                source_index_dict[pid] = []
            # 根据父类别ID插入列表字典
            source_index_dict[pid].append(item)
        # print("> JRecur.create_tree result_tree:", result_tree)
        # print("> JRecur.create_tree parent_node:", source_index_dict)

        # 如果不能找到树根节点，则不需要做递归了
        if not result_tree:
            return {}

        # 递归树 parent_node:树的每个父节点指针, index_dict:以每个节点的父ID作为键名的字典
        def recur_node(parent_node={}, source_dict={}, pk='id', ck='children'):
            pid_str = str(parent_node[pk])
            # 孩子列表，如果源字典中没有孩子则不需要添加孩子
            if not source_dict.get(pid_str, None):
                return parent_node
            parent_node[ck] = source_dict.get(pid_str, [])
            for child in parent_node[ck]:
                recur_node(child, source_dict)
            return parent_node

        result_tree = recur_node(parent_node=result_tree, source_dict=source_index_dict, pk=primary_key, ck=children_key)
        return result_tree

    @staticmethod
    def create_forest(source_list, primary_key="id", parent_key="parent_id", children_key='children'):
        """
        生成森林（多颗树）
        @param source_list 需要生成的来源数据列表
        @param search_root_key 需要从列表中搜索的树根节点键名
        @param search_root_value 需要从列表中搜索的树根植
        @param primary_key 指定主键名
        @param parent_key 指定父键名
        @param children_key 指定子键名
        """
        # 遍历列表，把数据存放在dict里
        result_forest = []
        source_index_dict = {}  # 父ID为键名组成的源字典，用于快速索引。里面的值均为列表
        for item in source_list:
            # 查找到树根。
            if not item.get(parent_key, None) or str(item.get(parent_key, '0')) == '0':
                result_forest.append(item)
                continue  # 边界检查：如果没有父类别，不需要生成索引列表字典

            pid = str(item[parent_key])  # 父ID的字符串

            # 边界检查：如果索引未创建，则初始化
            if not source_index_dict.get(pid, None):
                source_index_dict[pid] = []

            # 根据父类别ID插入列表字典
            source_index_dict[pid].append(item)

        # 如果不能找到树根节点，则不需要做递归了
        if not result_forest or not source_index_dict:
            return result_forest

        # 递归树 parent_node:树的每个父节点指针, index_dict:以每个节点的父ID作为键名的字典
        def recur_node(parent_node={}, source_dict={}, pk='id', ck='children'):
            pid_str = str(parent_node[pk])
            # 孩子列表，如果源字典中没有孩子则不需要添加孩子
            if not source_dict.get(pid_str, None):
                return parent_node
            parent_node[ck] = source_dict.get(pid_str, [])
            for child in parent_node[ck]:
                recur_node(child, source_dict)
            return parent_node

        for index, item in enumerate(result_forest):
            result_forest[index] = recur_node(parent_node=item, source_dict=source_index_dict, pk=primary_key, ck=children_key)

        return result_forest

    @staticmethod
    def filter_forest(source_forest=[], find_key=None, find_value=None, children_key='children', is_family_tree=False, ):
        """
        过滤森林树。支持多颗树查找，因为现实情况下被查找项可能同时属于多个家族树，所以需要用列表存放
        @param source_forest 需要过滤的森林树
        @param find_key 需要从列表中查找的树节点键名
        @param find_value 需要从列表中查找的树节点键值
        @param children_key 指定树分支键名
        @param is_family_tree 查找成功后，是否返回家族树（父亲、儿子、兄弟、祖先、后代）。True返回家族树，False返回生成子树（后代）
        """
        result_forest = []

        # 递归查找树（第一层是家族树）。判断子孙匹配则返回所在节点的生成子树
        def recur_find(node, k, v, ck):
            # 注：利用return实现匹配立即停止遍历，可巧妙减少计算遍历量 20221007 by Sieyoo
            if v and node.get(k, None) == v:
                return node
            # 如果当前节点不匹配，判断有孩子分支则继续递归，直到遍历完所有子孙节点（直至树叶）
            if node.get(ck, None):
                for it in node.get(ck):
                    cur = recur_find(it, k, v, ck)
                    if cur:
                        return cur
            # 遍历后仍不匹配，则层层回归返空值。
            return None

        # 森林是由多个家族树组成，所以最外层先做家族循环，再把匹配家族添加到结果
        for family_tree in source_forest:
            sub_tree = recur_find(family_tree, k=find_key, v=find_value, ck=children_key)
            if sub_tree:
                result_forest.append(family_tree if is_family_tree else sub_tree)

        return result_forest

    @staticmethod
    def filter_tree_values(tree_list, f_key="id", c_key="children") -> list:
        """
        遍历树中所有的节点的值
        :param tree_list: 树字典列表
        :param f_key: 检索的key
        :param c_key: 子节点的key名
        :return: list
        """
        out_list = []
        for item in tree_list:
            out_list.append(item[f_key])
            if item.get(c_key, None):
                out_list.extend(JRecur.filter_tree_values(item[c_key]))
        return out_list

    @staticmethod
    def get_filter_tree_params(params: dict = None, prefix="filter_tree_"):
        """
        解析参数中的树过滤方法
        :param params:搜索参数
        :param prefix: 参数前缀
        """
        if not isinstance(params, dict):
            return {}, None
        filter_tree_params = {}
        for k, v in params.items():
            if not re.search("^" + prefix, k):
                continue
            filter_tree_params[k.replace(prefix, "")] = v
        return filter_tree_params, None
