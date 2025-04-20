""" 一些常用的正则工具"""
import re

def extract_python_code(text: str)->str:
    """从文本中提取python代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的python文本
    """
    pattern = r'```python([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches

def extract_json_code(text:str)->str:
    """从文本中提取json代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的json文本
    """
    pattern = r'```json([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches
