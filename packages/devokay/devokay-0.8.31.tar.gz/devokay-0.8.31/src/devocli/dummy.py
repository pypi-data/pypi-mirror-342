# -*- coding: UTF-8 -*-
# python3

import argparse

from devocli.pcsdk import regist_pcsdk
from devocli.find_big_files import FindBigFilesCmd
from devocli.omni import OmniCmd
from devocli.remote import RemoteCmd
from devocli.utf8bom import cmd_regist as utf8bom_cmd_reg
from devocli.nginx import cmd_regist as nginx_cmd_reg
from devocli.fir import cmd_regist as fir_cmd_reg
from devocli.omni_server import cmd_regist as lang_server_reg
from devocli.md5 import cmd_regist as register_md5
from devocli.omni_diff_did_csv import cmd_regist as register_omni_diff_did_csv
from devocli.cmake import cmd_regist as register_cmake_helper
from devocli.omni_postbuild import cmd_regist as register_pcs_postbuild
from devocli.default import cmd_regist as default_regist

import devolib.util_prefer

def cli():
    parser = argparse.ArgumentParser(description='CLI描述')
    subparsers = parser.add_subparsers(metavar='子命令')

    find_big_files_cmd = FindBigFilesCmd()
    find_big_files_cmd.regist(subparsers)

    regist_pcsdk(subparsers)

    omni_cmd = OmniCmd()
    omni_cmd.regist(subparsers)

    remote_cmd = RemoteCmd()
    remote_cmd.regist(subparsers)

    utf8bom_cmd_reg(subparsers)
    nginx_cmd_reg(subparsers)
    fir_cmd_reg(subparsers)
    lang_server_reg(subparsers)
    register_md5(subparsers)
    register_omni_diff_did_csv(subparsers)
    register_cmake_helper(subparsers)
    register_pcs_postbuild(subparsers)
    default_regist(subparsers)

    args = parser.parse_args()      # 解析命令
    if hasattr(args, 'handle'):     # 1.第一个命令会解析成handle，使用args.handle()就能够调用
        args.handle(args)           # 1.1.其他参数会被解析成args的属性，以命令全称为属性名
    else:                           # 2.如果没有handle属性，则表示未输入子命令
        parser.print_help()


# python cli.py one
# python cli.py two
# python cli.py two -h
# python src/devocli/dummy.py find_big_files
# python src/devocli/dummy.py find_big_files -s 10
# python src/devocli/dummy.py pcsdk upload -
        
# python src/devocli/dummy.py omni --account_unbind_all 111 --token xxxx
# python src/devocli/dummy.py omni --account_register fengzilijie@qq.com
# python src/devocli/dummy.py omni --account_delete 1059
        
# python src/devocli/dummy.py remote --dir_copy lxlogs --date 2024-04-10

# python src/devocli/dummy.py fir.upload --token ece538a6e01af06934a621c36f699536 --file /Users/fallenink/Desktop/Developer/y8-assist-android/build/outputs/apk/debug/y8-assist-android-debug.apk --name 韵动场馆 --version 3.2.14 --build 84 --app_id 653762cd23389f6010122e43
# python src/devocli/dummy.py fir.latest --token ece538a6e01af06934a621c36f699536 --app_id 653762cd23389f6010122e43

# python src/devocli/dummy.py lang.server

# python src/devocli/dummy.py md5 --path ./xxx

# python src/devocli/dummy.py omni.build --product pcsdk (包含 pcbrowser)
# python src/devocli/dummy.py omni.build --product pcdemo
# python src/devocli/dummy.py omni.build --product pclauncher
# python src/devocli/dummy.py omni.archive --product pcsdk
# python src/devocli/dummy.py omni.archive --product pcsdk

# python src/devocli/dummy.py clear.win 

# python src/devocli/dummy.py omni.diff_did_csv --path1 xxxx --path2 xxxx 

# python src/devocli/dummy.py pcs.build.store --params official-pc-10001,official-pc-12001 --target /Users/fallenink/Desktop/Developer/devokay-py/tmp --encrypt false
# python src/devocli/dummy.py pcs.build.store --params official-pc-10001 --target /Users/fallenink/Desktop/Developer/devokay-py/tmp --encrypt false
# python src/devocli/dummy.py pcs.build.store --params wegame-pc-2341234123 --target /Users/fallenink/Desktop/Developer/devokay-py/tmp --encrypt false
# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","pipe":"SteamCN","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}' --origin D:\Sevenli\pcsdk-unity-plugin/Plugins/Windows --target Build\OmniPCUnity_Data\Plugins\x86_64
# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","pipe":"TestWegameCN","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}'

# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","sdk_params":"official-android-10001","sdk_hosts": "osp-api-pre.omneegames.com", "sdk_token": "zGQhMDratFtxeMCWkpCnGJhJtUXbtrdTNMDNBksW","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}'
# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","pipe":"OmniAndroidCN","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}'

# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","pipe":"wegame_pc_212960521","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}'
# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","pipe":"vivo_android_212960521","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}'
# python src/devocli/dummy.py omni.postbuild --json '{"executeMethod":"UnitySDKPostBuildProcessor.Run","pipe":"QB_CNcbt_wegame渠道包","quit":null,"batchmode":null,"projectPath":".","buildWindows64Player":"Build\\OmniPCUnity.exe","logFile":"Build/build.log","scenes":"Assets/Scenes/Launcher.unity"}'
# python src/devocli/dummy.py omni.postbuild --json '{"pipe":"official_pc_311912533"}'
# python src/devocli/dummy.py omni.postbuild --json '{"sdk_params":"official-pc-321784311","sdk_hosts": "osp-api-pre.omneegames.com", "sdk_token": "zGQhMDratFtxeMCWkpCnGJhJtUXbtrdTNMDNBksW"}'
# python src/devocli/dummy.py omni.postbuild --json '{"sdk_params":"official-pc-321784311","sdk_hosts": "osp-api-pre.nyotagames.com", "sdk_token": "emjKMNcBMadqKbQzaMuJRDbqsehugxLccDWdjqKP"}'

# osp-api-dev.omneegames.com
# 国内: omneegames.com
# 海外：nyotagames.com
# 环境区分dev，test, pre 三个
# dev&test token=TRSbYcRYZWFWbdWHKNb6VQSuM8tJ45GkLXnkD6aM
# 国内 pre token=zGQhMDratFtxeMCWkpCnGJhJtUXbtrdTNMDNBksW
# 海外pre token=emjKMNcBMadqKbQzaMuJRDbqsehugxLccDWdjqKP

# ios - test
# python src/devocli/dummy.py omni.postbuild --json '{"sdk_params":"apple-ios-10001","sdk_hosts": "osp-api-test.omneegames.com", "sdk_token": "TRSbYcRYZWFWbdWHKNb6VQSuM8tJ45GkLXnkD6aM"}'
# python src/devocli/dummy.py omni.postbuild --json '{"sdk_params":"apple-ios-10001","sdk_hosts": "osp-api-dev.omneegames.com", "sdk_token": "TRSbYcRYZWFWbdWHKNb6VQSuM8tJ45GkLXnkD6aM"}'

# pc - test
# python src/devocli/dummy.py omni.postbuild --json '{"pipe":"SteamCNBeta"}'

# js 代码压缩+混淆
# python src/devocli/dummy.py js.minified --path /Users/fallenink/Desktop/Developer/devokay-py/tmp/cef_bridge.js

if __name__ == '__main__':
    cli()
