# -*- coding: UTF-8 -*-
# python3

import os
import platform
from enum import Enum

class OSEnum(Enum):
    WIN = "Windows"
    MAC = "macOS"
    UBU = "Ubuntu"
    CEN = "CentOS"
    LIN = "Linux"

def operating_system():
    system = platform.system()
    if system == "Windows":
        return OSEnum.WIN
    elif system == "Darwin":
        return OSEnum.MAC
    elif system == "Linux":
        distribution = platform.linux_distribution()
        if distribution[0] == "Ubuntu":
            return OSEnum.UBU
        elif distribution[0] == "CentOS Linux":
            return OSEnum.CEN
        else:
            return OSEnum.LIN
    else:
        return system  # 其他操作系统名称

def is_ubuntu():
    return operating_system() == OSEnum.UBU

"""自定义异常类，表示环境变量未找到"""
class EnvVarNotFoundError(Exception):
    pass

"""获取环境变量，如果不存在则返回默认值或抛出异常"""
def get_env_var(var_name, default=None):
    value = os.getenv(var_name)
    if value is None:
        if default is not None:
            return default
        raise EnvVarNotFoundError(f"env var '{var_name}' missing")
    return value

def current_dir():
    return os.getcwd()