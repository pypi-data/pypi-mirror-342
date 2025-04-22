# -*- coding: UTF-8 -*-
# python3

import os
import sys
import json
import requests

# PC SDK build tool

from devolib import DynamicObject
from devolib.util_log import LOG_D, LOG_E, LOG_W, LOG_I
from devolib.util_os import get_env_var, current_dir
from devolib.util_str import starts_with, has, replace
from devolib.util_argparse import typeparse_str2bool
from devolib.util_httpc import GET_JSON
from devolib.util_fs import path_join_one, write_bytes_to_file, path_exists, read_bytes_of_file, write_file, touch_dir, copy_files, copy_dir, remove_files, remove_file
from devolib.util_json import json_to_str, json_from_str
from devolib.consts import ENV_TEST, ENV_PROD, PLAT_ADR, PLAT_IOS, PLAT_WEB, PLAT_HAR
from devolib.tools.expo import build_android as expo_build_android, build_ios as expo_build_ios
from devolib.tools.fir import FirIM

build_args = DynamicObject(
    expo=DynamicObject(access_token=None),
    fir=DynamicObject(app_id=None, app_token=None, app_name=None))

# MARK: Utils

"""
@brief 解析当前目录的 .devo
"""
def parse_args(command_line_args):
    profile_dir = command_line_args.dir
    conf_path = os.path.join(profile_dir, ".devo")

    LOG_D(f"Configuration path: {conf_path}")

    if os.path.exists(conf_path):
        with open(conf_path, 'r') as file:
            json_obj = json.load(file)

            LOG_D(f"Configuration file: {json_obj}")

            if json_obj is not None:
                if 'expo' in json_obj:
                    expo_json = json_obj["expo"]
                    if 'access_token' in expo_json:
                        build_args.expo.access_token = expo_json['access_token']

                if 'fir' in json_obj:
                    fir_json = json_obj["fir"]
                    if 'app_token' in fir_json:
                        build_args.fir.app_token = fir_json['app_token']

                    if 'app_id' in fir_json:
                        build_args.fir.app_id = fir_json['app_id']

                    if 'app_name' in fir_json:
                        build_args.fir.app_name = fir_json['app_name']

                # others settings

    else:
        raise Exception(f"`.devo` configuration file should be provided!")

    if build_args.expo.access_token is None:
        raise Exception(f"`access_token` should be configured!")

def upload_ipa(params, context):
    conf_json = get_conf_data(params, context.host, context.token)

    LOG_W(f"[STAGE] conf json: {conf_json}")

    return conf_json

def upload_apk(params, context):
    conf_json = get_conf_data(params, context.host, context.token)

    LOG_W(f"[STAGE] conf json: {conf_json}")

    return conf_json


def build_android(command_line_args):
    """
    查找指定目录下的 StreamingAssets 子目录路径。
    如果找到，返回其路径；如果未找到，则返回 None。
    """
    parse_args(command_line_args)

    expo_build_android(command_line_args.dir, build_args.expo.access_token)

    # fir = FirIM(build_args.upload_token)
    # fir.upload_file(args.file, args.name, args.version, args.build)

    # fir.get_latest_ver(args.app_id, args.alias)


def build_ios(command_line_args):
    parse_args(command_line_args)

    expo_build_ios(command_line_args.dir, build_args.expo.access_token)

# MARK: Command Handle

def cmd_handle_expo_build(command_line_args):
    LOG_D(f'system: {command_line_args.system}')
    LOG_D(f'dir: {command_line_args.dir}')
    LOG_D(f'profile: {command_line_args.profile}')
    LOG_D(f'upload: {command_line_args.upload}')

    if command_line_args.dir == None:
        command_line_args.dir = current_dir()

    if command_line_args.system == PLAT_IOS:
        build_ios(command_line_args)
    elif command_line_args.system == PLAT_ADR:
        build_android(command_line_args)
    elif command_line_args.system == PLAT_WEB:
        pass
    elif command_line_args.system == PLAT_HAR:
        pass

# MARK: Command Regist

def cmd_regist(subparsers):
    parser = subparsers.add_parser('tools.expo_build', help='SDK Build Tool for postbuilding sdk in unity.')
    parser.add_argument('-s', '--system', type=str, default=None, help='ios, adr, har')
    parser.add_argument('-d', '--dir', type=str, default=None, help='project dir')
    parser.add_argument('-p', '--profile', type=str, default=None, help='project path')
    parser.add_argument('-f', '--upload', type=str, default="fir", help='if upload to fir')
    parser.set_defaults(handle=cmd_handle_expo_build)

# python src/devocli/tools_expo.py
if __name__ == '__main__':
    command_line_args = DynamicObject(system=PLAT_ADR, dir="/Users/fallenink/Desktop/Developer/y8-app5", profile=ENV_TEST, upload="fir")
    # cmd_handle_expo_build(command_line_args)

    command_line_args = DynamicObject(system=PLAT_IOS, dir="/Users/fallenink/Desktop/Developer/y8-app5", profile=ENV_TEST, upload="fir")
    cmd_handle_expo_build(command_line_args)