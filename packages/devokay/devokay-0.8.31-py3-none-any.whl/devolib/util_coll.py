# -*- coding: UTF-8 -*-
# python3

###############################################
# 通用操作

'''
@brief 首元素
@example last('abcd') -> 'a'
@example last(['a', 'b', 'c', 'd']) -> 'a'
'''
def first(container):
    if len(container) <= 0:
        raise Exception('out of range')

    return container[0]

'''
@brief 末元素
@example last('abcd') -> 'd'
@example last(['a', 'b', 'c', 'd']) -> 'd'
'''
def last(container):
    return container[-1]

###############################################
# 字符串操作

'''
@brief 字符串分割
@required str
@optional separator
@optional howmany 指定返回的数组的最大长度
@example split('a-b-c-d', '-') -> ['a', 'b', 'c', 'd']

@todo 支持正则
'''
def split(str, separator=',', howmany=None):
    return str.split(separator)

###############################################
# 数组操作


def join():
    pass

'''
@brief 粘接？
@description 向数组添加或删除元素，返回被删除的项目
@example splice(['a', 'b', 'c', 'd'], 0, 2) ->(函数返回) ['a', 'b'] ~>(数组变化) ['c', 'd']
@example splice(['a', 'b', 'c', 'd'], 0, 2, ['e']) -> ['a', 'b'] ~> ['c', 'd', 'e']
'''
def splice(start, length, arr):
    pass

'''
@brief 切割
@example slice(['a', 'b', 'c', 'd'], 0, 2) -> ['a', 'b']
'''
def slice(start, length):
    pass

###############################################
# 字典操作