# -*- coding: UTF-8 -*-
# python3

import inspect
import logging
import os
import sys
from devolib.util_prefer import preferences
from devolib.consts import log_use_debug, log_use_info, log_use_warn, log_use_error

#################################################################
## 常规日志对象
# 获取 debug logger
# logger = logging.getLogger("debug_logger")
# logger.setLevel(logging.DEBUG)

# # 创建流式句柄
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# # 创建格式化器
# formatter = logging.Formatter(
#     '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# )

# # 配置 logger
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

#########################################################################
## 动态日志对象
# 创建动态 logger 适配器，解决 logger 封装带来的文件信息缺失问题
class DynamicLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        stack = inspect.stack()
        try:
            outer_frames = inspect.getouterframes(stack[0].frame)
            caller_frame_ = outer_frames[4]
            filename = caller_frame_.filename
            lineno = caller_frame_.lineno

            filename = os.path.basename(filename)

            kwargs['extra'] = {'custom_lineno': lineno, 'custom_pathname': filename}
        finally:
            del outer_frames
            del stack
        return msg, kwargs

# 创建 Logger
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG) # output logs whose level greater than DEBUG

# dyn_console_handler = logging.StreamHandler()
# dyn_console_handler.setLevel(logging.DEBUG) # output logs whose level greater than DEBUG

# 创建 stdout Handler，用于输出 INFO 和 WARNING 级别的日志
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)  # 最低日志级别
stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

# 创建 stderr Handler，用于输出 ERROR 和 CRITICAL 级别的日志
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)  # 最低日志级别

# 设置通用日志格式
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(custom_pathname)s:%(custom_lineno)d] %(message)s'
)
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

# dyn_console_handler.setFormatter(formatter)

# 将两个 Handler 添加到 Logger
default_logger.addHandler(stdout_handler)
default_logger.addHandler(stderr_handler)

# 日志输出预期
# logger.debug("This is a DEBUG message.")     # 输出到 sys.stdout
# logger.info("This is an INFO message.")      # 输出到 sys.stdout
# logger.warning("This is a WARNING message.") # 输出到 sys.stdout
# logger.error("This is an ERROR message.")    # 输出到 sys.stderr
# logger.critical("This is a CRITICAL message.") # 输出到 sys.stderr

dyn_logger = DynamicLoggerAdapter(default_logger, {})

'''
@brief 级别封装
'''

def LOG_D(str):
    if log_use_debug(preferences.log_level):
        dyn_logger.debug(str)

def LOG_I(str):
    if log_use_info(preferences.log_level):
        dyn_logger.info(str)

def LOG_W(str):
    if log_use_warn(preferences.log_level):
        dyn_logger.warning(str)

def LOG_E(str):
    if log_use_error(preferences.log_level):
        dyn_logger.error(str)

def LOG_F(str):
    dyn_logger.error(str)
    raise Exception(str)

'''
@brief 打印主流程
'''
def LOG_MAIN(str):
    dyn_logger.warning(f'====> {str}')


'''
@brief 打印子流程
'''
def LOG_SUB(str):
    dyn_logger.info(f'----> {str}')

def LOG_CONSOLE(str):
    print(f'>> {str}')

# 测试例程

if __name__ == '__main__':
    LOG_D('debug log')
    LOG_MAIN('main log')