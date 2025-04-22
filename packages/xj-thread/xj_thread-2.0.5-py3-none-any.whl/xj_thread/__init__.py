import os, sys
from pathlib import Path

# 引入内置库到环境变量
__module_dir = Path(__file__).resolve().parent
sys.path.append(os.path.join(__module_dir, 'libs'))

# 当前模块所需安装应用。应用会搜索内置库，并通过setting.py注册到项目中
INSTALLED_APPS = ["DjangoUeditor"]

