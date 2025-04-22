# -*- coding: UTF-8 -*-
# python3

import argparse
import ast

'''
    parser = argparse.ArgumentParser(description="接收字符串列表输入")
    parser.add_argument(
        "--items",
        type=parse_list,
        help="输入一个列表格式的字符串，例如 ['apple', 'banana', 'cherry']"
    )

    args = parser.parse_args()
    print("接收到的字符串数组:", args.items)
'''
def typeparse_list(value):
    try:
        # 将字符串解析为 Python 对象，例如 ['apple', 'banana', 'cherry']
        parsed_value = ast.literal_eval(value)
        if isinstance(parsed_value, list):
            return parsed_value
        else:
            raise argparse.ArgumentTypeError("Format error: should be ['apple', 'banana', 'cherry']")
    except (ValueError, SyntaxError):
        raise argparse.ArgumentTypeError("Format error: should be ['apple', 'banana', 'cherry']")

'''
@brief 将str转bool
'''
def typeparse_str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')