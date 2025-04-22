# -*- coding: UTF-8 -*-
# python3

from devolib.util_log import LOG_E

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            # 调用被装饰的函数，并返回结果
            return func(*args, **kwargs)
        except Exception as e:
            # 处理异常，这里可以根据实际需求进行处理，比如打印错误信息
            LOG_E(f"函数 {func.__name__} 发生异常: {e}")
            # 或者进行其他操作，比如记录日志、发送邮件等
            # 这里我们简单地将异常信息重新抛出
            raise
    return wrapper