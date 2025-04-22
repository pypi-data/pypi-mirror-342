# -*- coding: UTF-8 -*-
# python3

NAME = 'sssss'

'''
@brief env type for server
'''
ENV_DEV='dev'
ENV_TEST='test'
ENV_PRE='pre'
ENV_PROD='prod'


'''
@brief platform type
'''
PLAT_ADR='adr'      # android
PLAT_IOS='ios'
PLAT_WIN='pc'       # windows
PLAT_MAC='mac'      # macosx
PLAT_HAR='har'      # harmonyos
PLAT_WEB="web"      # web

'''
@brief log level
'''
LOG_DEBUG='debug'
LOG_INFO='info'
LOG_WARN='warn'
LOG_ERROR='error'

def log_use_debug(log_level):
    return log_level in LOG_DEBUG

def log_use_info(log_level):
    return log_level in [LOG_DEBUG, LOG_INFO]

def log_use_warn(log_level):
    return log_level in [LOG_DEBUG, LOG_INFO, LOG_WARN]

def log_use_error(log_level):
    return log_level in [LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR]


'''
@brief conf
'''
CONFIG_FILE = ".devo"