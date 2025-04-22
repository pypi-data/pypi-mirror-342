# -*- coding: UTF-8 -*-
# python3

import os
import sys

from devolib import DynamicObject
from devolib.util_log import LOG_D, LOG_E
from devolib.util_str import ends_with, str_to_bytes, bytes_to_str
from devolib.util_fs import path_join_one, write_bytes_to_file, path_exists, read_of_file, write_file, touch_dir, copy_files, copy_dir, remove_files
from devolib.util_js import minified

# MARK: JS Tools

def generate_output_path(intput_path):
    output_dir = os.path.dirname(intput_path)

    # 获取输入文件的文件名（不带扩展名）
    file_name = os.path.splitext(os.path.basename(intput_path))[0]
    
    # 生成输出文件名，例如 input.js -> input.min.js
    output_path = os.path.join(output_dir, f"{file_name}.min.js")

    return output_path

def cmd_handle_js_minified(args):
    if args.path is not None:
        input_path = args.path
        output_path = generate_output_path(input_path)

        LOG_D(f"input_path: {input_path}")
        LOG_D(f"output path: {output_path}")

        if not path_exists(input_path):
            raise Exception(f"input_path not exists!")
        
        minified(input_path, output_path)
    else:
        LOG_E(f"no file is processed.")

# MARK: Command Regist

def cmd_regist(subparsers):
    parser = subparsers.add_parser('js.minified', help='js tools for minfied, .')
    parser.add_argument('-p', '--path', type=str, default=None, help='js file full path')
    parser.set_defaults(handle=cmd_handle_js_minified)

# python src/devocli/default.py
if __name__ == '__main__':
    args = DynamicObject(path="/Users/fallenink/Desktop/Developer/devokay-py/tmp/pcsdk.json")
    cmd_handle_js_minified(args)