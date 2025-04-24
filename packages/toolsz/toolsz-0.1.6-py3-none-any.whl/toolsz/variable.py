""" 一个方便的变量调试工具 """
import os
import dill

def pull(variable_path: str= None):
    """从临时区加载到当前全局变量"""
    variable_path = variable_path or os.getenv("VARIABLE_PATH")
    with open(variable_path, "rb") as f:
        loaded_vars = dill.load(f)
    # 将变量注入到当前命名空间
    globals().update(loaded_vars)

def push(variable_path:str = None):
    """将当前变量推送到临时区"""
    variable_path = variable_path or os.getenv("VARIABLE_PATH")
    with open(variable_path, "wb") as f:
        dill.dump({k:v for k,v in globals().items() if not k.startswith('__')}, f)
