# -*- coding: UTF-8 -*-
# python3

from enum import Enum

class CharSet(Enum):
    ASCII = 'ascii'
    UTF_8 = 'utf-8'
    UTF_16 = 'utf-16'

def replace_newline_with_comma(str):
    return str.replace("\n", ",")

'''
@brief 后缀匹配
'''
def ends_with(s, suffix):
    if isinstance(suffix, str):
        return s.endswith(suffix)
    elif isinstance(suffix, (tuple, list)):
        return s.endswith(tuple(suffix))
    return False

'''
@brief 前缀匹配
'''
def starts_with(s, suffix):
    if isinstance(suffix, str):
        return s.startswith(suffix)
    elif isinstance(suffix, (tuple, list)):
        return s.startswith(tuple(suffix))
    return False

'''
@brief 字符串包含
'''
def has(s, sub):
    if s is None or sub is None:
        return False

    return sub in s

'''
@brief 字符串替换(s1->s2)，支持指定替换次数
'''
def replace(s, old, new, count=None):
    """
    Replace occurrences of a substring in a string with another substring.

    :param s: The original string.
    :param old: The substring to be replaced.
    :param new: The substring to replace with.
    :param count: (Optional) Maximum number of replacements. If None, replace all occurrences.
    :return: A new string with the specified replacements.
    """
    if not isinstance(s, str):
        raise ValueError("Input s must be a string.")
    if not isinstance(old, str) or not isinstance(new, str):
        raise ValueError("Both old and new must be strings.")
    
    return s.replace(old, new, count if count is not None else -1)

'''
@brief bytearray to hex string
@example 
    byte_array = bytearray([15, 255, 160, 50])
    print(bytes_to_str_with_hex(byte_array))
    # 输出: "0fffA032"
'''
def bytes_to_str_with_hex(byte_array, separator=''):
    return separator.join(f'{byte:02x}' for byte in byte_array)


def bytes_to_str(bytes, char_set=CharSet.UTF_8):
    return bytes.decode(char_set.value)

def str_to_bytes(str, char_set=CharSet.UTF_8):
    return str.encode(char_set.value)