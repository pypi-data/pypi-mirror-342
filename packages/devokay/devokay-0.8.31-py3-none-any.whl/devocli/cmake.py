# -*- coding: UTF-8 -*-
# python3

from devolib.util_fs import path_join_one, path_exists
from devolib.util_log import LOG_D
from devolib.util_cmake import CMakeProject


def export_xc(args):
    proj = CMakeProject(source_dir=args.dir, proj_name=args.proj)
    proj.export()


def export_vs():
    pass



'''
@brief CMake 助手
'''
def cmd_regist(subparsers):
    parser = subparsers.add_parser('cmake.export', help='CMake Tools')
    parser.add_argument('-d', '--dir', type=str, help='path to CMakeList file')
    parser.add_argument('-p', '--proj', type=str, help='project name')
    parser.set_defaults(handle=export_xc)

    parser = subparsers.add_parser('cmake.build', help='CMake Tools')
    parser.add_argument('-v', '--ver', type=str, default='2022', help='2019,2022')
    parser.add_argument('-o', '--out', type=str, default='EXPORT', help='导出路径')
    parser.set_defaults(handle=export_vs)