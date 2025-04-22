# -*- coding: UTF-8 -*-
# python3

import os

from devolib.util_fs import path_join_one, path_exists

# 1. Windows - GitBash - 启动 ssh-agent
''' eval `ssh-agent -s` '''

# 1.1 然后再添加指定的私钥
''' ssh-add ~/.ssh/<> '''

'''
@cate utils
@brief 是否是有效的git目录
'''
def is_valid_git():
    dot_git_dir = path_join_one(os.getcwd(), '.git')
    return path_exists(dot_git_dir)

'''
@cate bizs
@brief 移除子模块
'''
def remove_sub(args):
    if not args.remove_sub and len(args.remove_sub) > 0:
        pass

'''
@cate bizs
@brief 清除所有改动
'''
def reset_all(args):
    if not args.reset_all:
        pass

'''
@cate cmds
@brief git帮助
'''
class GitHelperCmd:
    def __init__(self):
        pass

    def regist(self, subparsers):
        parser = subparsers.add_parser('git', help='git助手')
        parser.add_argument('-rs', '--remove_sub', type=int, default=1, help='移除子模块，传入子模块名')
        parser.add_argument('-ra', '--reset_all', type=int, default=1, help='清除所有改动')
        parser.set_defaults(handle=GitHelperCmd.handle)

    @classmethod
    def handle(cls, args):
        remove_sub(args)

    