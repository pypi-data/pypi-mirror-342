# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
import importlib
import sys


def dynamic_load_function(import_path: str = None, function_name=None, find_services=False):
    """
    动态加载模块中的类,返回类的指针
    可从通过RPC协议从consul服务获取其他服务器的服务类。
    :param find_services: 是否使用RPC，发现服务
    :param import_path: 导入类的文件路径
    :param function_name: 导入文件中方法名称
    :return: class_instance,err_msg
    """
    try:
        function_instance = getattr(sys.modules.get(import_path), function_name, None)
        if function_instance is None:
            import_module = importlib.import_module(import_path)
            function_instance = getattr(import_module, function_name)
        return function_instance, None
    except AttributeError:
        return None, "系统中不存在该方法"
    except Exception as e:
        return None, str(e)
