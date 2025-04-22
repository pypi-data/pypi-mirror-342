# -*- coding: UTF-8 -*-
# python3

import os

'''
@brief 递归查找大于threshhold_size的文件
'''
def get_large_files(folder_path, threshhold_size):
    large_files = []
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path) # 单位:字节
            if file_size > 1024 * 1024 * (threshhold_size):
                large_files.append((file_path, file_size))
    return large_files

'''
@brief 查找大文件命令
'''
class FindBigFilesCmd:
    def __init__(self):
        pass

    def regist(self, subparsers):
        parser = subparsers.add_parser('find_big_files', help='寻找当前文件夹下的大文件')
        # 参数(简写，全称，类型，是否必填，帮助说明)
        parser.add_argument('-s', '--size', type=int, default=1, help='文件大小阈值(默认1M)')
        parser.set_defaults(handle=FindBigFilesCmd.handle)

    @classmethod
    def handle(cls, args):
        current_path = os.getcwd()

        print(f'current_path: {current_path}')
        print(f'size: {args.size}')

        big_files = get_large_files(current_path, args.size)

        # 输出文件列表
        if len(big_files) > 0:
            for file_path, file_size in big_files:
                print(f"File: {file_path}, Size: {file_size} bytes")
        else:
            print(f"No big deal")

    