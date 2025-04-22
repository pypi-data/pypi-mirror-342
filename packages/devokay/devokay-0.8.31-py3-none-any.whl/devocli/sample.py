# -*- coding: UTF-8 -*-
# python3

import os

def reg_one(subparsers):
    # 添加子命令，演示没有参数
    one_parser = subparsers.add_parser('one', help='第一个命令')
    one_parser.set_defaults(handle=handle_one)

def handle_one(args):
    print('handle_one')

def reg_two(subparsers):
    # 添加子命令，演示有参数
    two_parser = subparsers.add_parser('two', help='第二个命令')
    # 参数(简写，全称，类型，是否必填，帮助说明)
    two_parser.add_argument('-s', '--str', type=str, required=True,
                            help='一个字符串类型参数')
    # 参数(简写，全称，类型，默认值，帮助说明)
    two_parser.add_argument('-d', '--default', type=str, default='默认值',
                            help='这个命令有默认值')
    # 参数(简写，全称，类型，帮助说明)
    two_parser.add_argument('-ts', '--the-str', type=str,
                            help='当全称有横线时，属性名转换为下划线，即 the_str')
    two_parser.set_defaults(handle=handle_two)

def handle_two(args):
    print('handle_two')
    print(f'str:{args.str}')
    print(f'default:{args.default}')
    print(f'the-str:{args.the_str}')