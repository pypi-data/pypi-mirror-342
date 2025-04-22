# -*- coding: UTF-8 -*-
# python3

from devolib.util_fs import md5_of_file
from devolib.util_log import LOG_CONSOLE

# Linux
# md5sum ./file_name.txt

# Macos
# md5 ./file_name.txt

# Windows
# certutil -hashfile .\file_name.txt

def cmd_handle(args):
    if args.path is not None:
        LOG_CONSOLE(md5_of_file(args.path))

def cmd_regist(subparsers):
    parser = subparsers.add_parser('md5', help='calculate md5 of file')
    parser.add_argument('-p', '--path', type=str, help='path of file')
    parser.set_defaults(handle=cmd_handle)