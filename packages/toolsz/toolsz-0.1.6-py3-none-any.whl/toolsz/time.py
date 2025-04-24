""" 时间小工具 """
from datetime import datetime

def get_today(type=''):
    """返回当前本地日期，格式为 'YYYY-MM-DD' 的字符串。

    Returns:
        str: 当前本地日期，格式为 'YYYY-MM-DD'
    """
    local_time = datetime.today()
    if type == 'date':
        local_time = local_time.strftime("%Y-%m-%d")
    elif type == 'time':
        local_time = local_time.strftime("%H:%M:%S")
    else:
        local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    return local_time
