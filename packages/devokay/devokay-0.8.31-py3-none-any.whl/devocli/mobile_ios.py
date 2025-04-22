# -*- coding: UTF-8 -*-
# python3

from devolib.util_log import LOG_D, LOG_E
from devolib.ios.rename_project import XcodeProjectRenamer

def run_rename_project():
    path = '/Users/fallenink/Desktop/test/TestAAA'
    old_name = 'TestDDD'
    new_name = 'TestEEE'

    renamer = XcodeProjectRenamer(old_name, new_name, path)
    renamer.run()

def cmd_handle_ios_rename_project(args):
    if args.path is not None:
        
        pass
    else:
        LOG_E(f"none file is processed.")


