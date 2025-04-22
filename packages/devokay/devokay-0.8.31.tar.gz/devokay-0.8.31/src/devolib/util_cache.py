# -*- coding: UTF-8 -*-
# python3

import os
from diskcache import Cache as DiskCache


# 获取用户主目录
user_home = os.path.expanduser('~')

# 拼接 .devo/cache 目录
cache_dir = os.path.join(user_home, '.devo', 'cache')

cache = DiskCache(cache_dir)


def cache_set(key, value):
    cache.set(key, value)

def cache_get(key, default_val=None):
    if default_val is None:
        return cache.get(key)
    else:
        return cache.get(key, default=default_val)
    
def cache_has(key):
    return key in cache

def cache_rem(key):
    if cache_has(key):
        # 删除缓存中的某个键值对
        del cache[key]

def cache_cls():
    # 清空缓存
    cache.clear()

def cache_shut():
    # 关闭缓存
    cache.close()