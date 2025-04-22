# -*- coding: UTF-8 -*-
# python3

from devolib.util_fs import path_join_one, path_exists
from devolib.util_log import LOG_D, LOG_E
from devocli.mobile_ios import cmd_handle_ios_rename_project

def cmd_regist(subparsers):
    parser = subparsers.add_parser('mobile.ios.rename_project', help='For rename ios project/workspace.')
    parser.add_argument('-p', '--path', type=str, default=None, help='project path')
    parser.add_argument('-t', '--origin', type=str, default=None, help='origin project name')
    parser.add_argument('-t', '--target', type=str, default=None, help='target project name')
    parser.set_defaults(handle=cmd_handle_ios_rename_project)


if __name__ == '__main__':
    pass