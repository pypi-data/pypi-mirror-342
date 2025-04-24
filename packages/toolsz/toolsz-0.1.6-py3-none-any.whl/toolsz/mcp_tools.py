""" 函数工具 """
from llama_index.core.tools.types import ToolOutput
from llama_index.core.tools import FunctionTool

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def xshell(shell:str) -> str:
    "This is an interactive shell tool,It remembers your actions and allows you to take them step by step."
    print(shell,'shell')
    result = input('输入shell:')
    tool_output = ToolOutput(
        content=result,
        tool_name="interaction_xshell",
        raw_input={"args": {"shell":shell}},
        raw_output={"结果": "成功"}
    )
    return tool_output


def package(fn,name:str = None,description:str = None):
    """将一般的函数打包成工具

    Args:
        fn (function): 编写的函数
        name (str, optional): 函数名.
        description (str, optional): 函数描述. Defaults to None.

    Returns:
        FunctionTool: functioncall
    """

    if name is not None or description is not None:
        return FunctionTool.from_defaults(fn=fn,
                                      name = name,
                                      description = description)
    else:
        return FunctionTool.from_defaults(fn=fn)

# TODO 增加一些MCP能力
