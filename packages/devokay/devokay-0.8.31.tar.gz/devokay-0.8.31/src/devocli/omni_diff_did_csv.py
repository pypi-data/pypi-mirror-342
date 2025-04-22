# -*- coding: UTF-8 -*-
# python3

import csv

def read_csv_to_set(file_path):
    """读取CSV文件，将内容（除去表头）存入一个集合中"""
    data_set = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过表头
        for row in reader:
            data_set.add(row[0])
    return data_set

def output_difference(file1, file2):
    """计算两个CSV文件的差集，并逐行输出差集条目"""
    set1 = read_csv_to_set(file1)
    set2 = read_csv_to_set(file2)
    
    difference = set1 - set2  # 求差集

    print(f'set1 length: {len(set1)}')
    print(f'set1 length: {len(set2)}')
    print(f'diff length: {len(difference)}')
    print(f'diff length: {", ".join(difference)}')

    # # 逐行输出差集条目
    # for item in difference:
    #     print(item)

def cmd_handle(args):
    if args.path1 is not None and args.path2 is not None:
        output_difference(args.path1, args.path2)

def cmd_regist(subparsers):
    parser = subparsers.add_parser('omni.diff_did_csv', help='--')
    parser.add_argument('-p1', '--path1', type=str, default=None, help='--')
    parser.add_argument('-p2', '--path2', type=str, default=None, help='--')
    parser.set_defaults(handle=cmd_handle)