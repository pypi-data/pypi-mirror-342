# -*- coding: UTF-8 -*-
# python3

import schedule

class ScheCmd:
    def __init__(self):
        pass

    def regist(self, subparsers):
        parser = subparsers.add_parser('sche', help='定时任务')
        parser.add_argument('-s', '--start', type=str, default=, help='文件夹拷贝')
        parser.add_argument('-d', '--date', type=str, default='2024-01-01', help='指定日期')
        parser.add_argument('-fc', '--file_copy', type=int, default=1, help='文件拷贝')
        parser.set_defaults(handle=RemoteCmd.handle)

    @classmethod
    def handle(cls, args):
        _dir_copy(args)

