# -*- coding: UTF-8 -*-
# python3

import hashlib
import json
import os
from datetime import datetime
from omni_helper_ui import JussSportFrame

def cmd_handle_ui(args):
    app = JussSportFrame(0)
    app.MainLoop()

def cmd_regist(subparsers):
    parser = subparsers.add_parser('omni.helper.ui', help='omni helper with ui interaction.')

    # parser.add_argument('-ad', '--account_delete', type=str, default=None, help='删除账号: acc_id')
    parser.set_defaults(handle=cmd_handle_ui)

if __name__ == '__main__':
    cmd_handle_ui({})