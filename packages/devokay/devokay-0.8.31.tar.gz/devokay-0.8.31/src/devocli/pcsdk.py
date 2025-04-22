# -*- coding: UTF-8 -*-
# python3

import os
import subprocess

from devolib.util_oss import Oss
from devolib.util_fs import target_path_of_dirname, path_join_many, has_dir, touch_dir, remove_dir, has_file, list_files, filename_of_path
from devolib.util_log import LOG_D, LOG_E
from devolib.util_coll import last, split

VERSION_TYPE_SNAPSHOT = 'snapshot'
VERSION_TYPE_RELEASE = 'release'

########################################
# utils

def is_valid_plat(plat):
    return plat in ['win', 'mac', 'ios', 'android', 'switch', 'linux', 'harmony']

def is_valid_ver(ver):
    segments = split(ver, '.')
    if len(segments) != 4:
        return False

    for segment in segments:
        if not segment.isdigit() or int(segment) < 0:
            return False
    return True

def compare_vers(version1, version2):
    v1_segments = list(map(int, version1.split('.')))
    v2_segments = list(map(int, version2.split('.')))

    # 逐段比较版本号
    for v1, v2 in zip(v1_segments, v2_segments):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1

    # 如果所有段都相等，则比较版本号长度
    if len(v1_segments) < len(v2_segments):
        return -1
    elif len(v1_segments) > len(v2_segments):
        return 1
    else:
        return 0

def is_ver_greater(version1, version2):
    return compare_vers(version1, version2) > 0

def is_ver_less(version1, version2):
    return compare_vers(version1, version2) < 0

def is_ver_equal(version1, version2):
    return compare_vers(version1, version2) == 0

def start_or_restart_exe(exe_path):
    # 尝试启动 exe
    try:
        subprocess.Popen([exe_path])
        print(f"启动 {exe_path}")
    except Exception as e:
        print(f"启动 {exe_path} 失败：{e}")
        # 尝试关闭已经打开的同名程序
        try:
            subprocess.run(["taskkill", "/F", "/IM", exe_path])
            print(f"关闭 {exe_path}")
            # 再次尝试启动 exe
            subprocess.Popen([exe_path])
            print(f"再次启动 {exe_path}")
        except Exception as e:
            print(f"关闭 {exe_path} 失败：{e}")

########################################
# 沙盒

class SandBox:
    _deploy_folder_name = '.deploy'
    _deploy_dir = path_join_many(os.getcwd(), [_deploy_folder_name])

    def __init__(self):
        # LOG_D(f'deploy_dir: {self._deploy_dir}')

        # 如果没有文件夹，则创建
        touch_dir(self._deploy_dir)

    # 清理沙盒
    def clr(self):
        remove_dir(self._deploy_dir)

########################################
# 版本相关

# 四段式版本(major.minor.patch.build)
# Major（主要版本号）：表示主要的版本更新，通常意味着引入了向后不兼容的改变或重大功能更新。当发生重大变化时，需要提升主要版本号。
# Minor（次要版本号）：表示次要的版本更新，通常意味着引入了新功能，但是这些新功能与之前版本兼容。当引入了新功能时，需要提升次要版本号。
# Patch（补丁版本号）：表示补丁或修复更新，通常意味着修复了之前版本中的 bug 或者安全漏洞。当进行 bug 修复时，需要提升补丁版本号。
# Build（构建版本号）：表示构建或者编译的版本号，通常用于标识不同的构建或者编译。在每次构建或者编译时，可以递增构建版本号。

class VerMgr:
    _type = None
    _oss = None
    _sand_box = None

    def __init__(self, oss, sand_box):
        self._oss = oss
        self._sand_box = sand_box

    def _ver_obj_name(self):
        return f'vers.{self._type}.json'

    def set_type(self, type):
        self._type = type

    # 获取需要清理的版本列表
    def clr():
        pass

    # 获取版本
    def get():
        # 下载文件

        # 提取最新版本，

        # 如果没有就生成初始文件

        return {
            'id': 1, 
            'build': 1, 
            'object': 'pcsdk-0.1.1.1-windows.zip', 
            'md5': '83838838', 
            'type': VERSION_TYPE_SNAPSHOT
        }

    # 提交版本
    def put(version_obj):
        pass

class PCSdk:
    _oss = Oss(end_point=os.getenv('OSS_END_POINT'), bucket_name=os.getenv('OSS_BUCKET_NAME'), path_prefix='pcsdk')
    _sand_box = SandBox()
    _ver_mgr = VerMgr(oss=_oss, sand_box=_sand_box)

    def __init__(self):

        # res_path = target_path_of_dirname('res')
        # file_path = f'{res_path}/oss_test.jpeg'
        # self._oss.put(file_path=file_path)

        # tmp_path = target_path_of_dirname('tmp')
        # file_path = f'{tmp_path}/oss_test.jpeg'
        # self._oss.get(file_path=file_path)
        pass


    '''
    @brief 编译项目
    '''
    def build(self, ver, type):
        pass

    '''
    @brief 上传oss
    '''
    def upload(self, args):
        upload = args.upload

        if upload == '.': # current dir
            upload_dir = os.getcwd()
            LOG_D(f'upload_dir: {upload_dir}')

            likely_files = list_files(in_folder=upload_dir, by_extension='.zip')

            LOG_D(f'likely_files: {likely_files}')

            upload_path = last(likely_files)# join_dirs(upload_dir, likely_files)
        else:
            upload_path = upload

        LOG_D(f'upload_path: {upload_path}')

        # check if upload is valid file path
        if not has_file(upload_path):
            LOG_E(f'`--upload/-u` not valid')

            return
        
        # extract file info
        filename = filename_of_path(upload_path)

        # parse `sdk_name` `sdk_ver` `sdk_plat`
        sdk_name, sdk_ver, sdk_plat, *rest = split(filename, '-')
        if not is_valid_ver(sdk_ver) or not is_valid_plat(sdk_plat):
            LOG_E(f'product name invalid: sdk_ver({sdk_ver}), sdk_plat({sdk_plat})')

            return
        
        # upload upload_path
        self._oss.put(file_path=upload_path)

    '''
    @brief 升级
    '''
    def upgrade(self):
        pass

    '''
    @brief 升级demo下的pcsdk，并启动demo，如果demo进程已经打开，则强制关闭它
    '''
    def demo(self, ver=None):
        demo_dir = 'D:/Sevenli/pcsdk-demo-old'
        sdk_dir = 'D:/Sevenli/pcsdk-old'

        demo_exe_path = path_join_many(demo_dir, ['ParkSDKDemo.exe'])
        sdk_main_product_dir = path_join_many(sdk_dir, ['build', 'sdk', 'main', 'Debug'])
        sdk_browser_product_dir = path_join_many(sdk_dir, ['src', 'pcbrowser', 'win', 'install', 'browser', 'redistributable_bin', 'Win64', 'bin', 'Plugins'])

        sdk_main_products = ['limpc.dll', 'limpc.lib', 'limpc.pdb']
        sdk_browser_products = ['', '', '', 'limpcbrowser.exe']


        # 拷贝 sdk main products
        sdk_main_product_pathes = sdk_main_products

        # 拷贝 sdk browser products
        sdk_browser_product_pathes = sdk_browser_products


    '''
    @brief 收集本机pcsdk的日志和cache等
    '''
    def log_collect(self):
        pass

    '''
    @brief 打印版本列表
    '''
    def vers():
        pass

'''
@brief 
'''

########################################
# ？？相关

########################################
# 命令注册

def regist_pcsdk(subparsers):
    parser = subparsers.add_parser('pcsdk', help='pcsdk相关')
    parser.add_argument('-b', '--build', type=str, help='编译(项目根目录执行)')
    parser.add_argument('-u', '--upload', type=str, help='上传(项目根目录执行)')
    parser.add_argument('-d', '--demo', type=str, help='demo更新pcsdk(demo根目录执行)')
    parser.add_argument('-lc', '--log_collect', type=str, help='日志收集(任意目录执行)(将输出的标识给到开发)')
    parser.set_defaults(handle=handle_pcsdk)

def handle_pcsdk(args):
    pcsdk = PCSdk()

    if args.upload is not None:
        pcsdk.upload(args)