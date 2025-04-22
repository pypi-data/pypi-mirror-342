# -*- coding: UTF-8 -*-
# python3

import os
import chardet # /opt/anaconda3/envs/py312/lib/python3.12/site-packages
import codecs

'''
utf8bom

@brief 扫描指定/当前目录，将 .h, .c, .cc, .cpp 文件转为 UFT8 with BOM
'''

def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']

            if confidence >= 0.99:
                try:
                    content = raw_data.decode(encoding)
                    with codecs.open(file_path, 'w', 'utf-8-sig') as f_out: # 文件编码转换为 UTF-8 with BOM
                        f_out.write(content)
                    print(f"=> '{file_path}': '{encoding}'({confidence}), converted")
                except Exception as e:
                    print(f"文件 '{file_path}' 转换时出现错误: {str(e)}")
            else:
                print(f"=> '{file_path}': '{encoding}'({confidence}), skipped")
    except Exception as ex:
        print(f"检测文件编码时出现异常: {str(ex)}")

def scan_files(target_dir, file_suffixes):
    file_cnt = 0
    for root, dirs, files in os.walk(target_dir): # 遍历文件夹
        for file in files:
            file_path = os.path.join(root, file) # 获取文件的完整路径
            for suffix in file_suffixes: # 检查文件后缀是否在指定的后缀数组中
                if file.endswith(suffix):
                    file_cnt += 1

                    print(f'[{file_cnt} ]path: {file_path}')

                    detect_encoding(file_path)

def cmd_handle(args):
    scan_files(args.dir, args.suffix.split(","))

def cmd_regist(subparsers):
    parser = subparsers.add_parser('utf8bom', help='文件编码转存UTF8-BOM')
    parser.add_argument('-d', '--dir', type=str, default='.', help='文件夹路径')
    parser.add_argument('-s', '--suffix', type=str, default='h,hpp,c,cc,cpp', help='文件后缀')
    parser.set_defaults(handle=cmd_handle)
    
if __name__ == '__main__':
    folder_path = '/Users/fallenink/Desktop/Developer/pc-launcher'  # 替换为实际的文件夹路径
    suffixes = ['.h', '.hpp', '.c', '.cc', '.cpp']   # 后缀数组，可以添加需要匹配的后缀

    scan_files(folder_path, suffixes)