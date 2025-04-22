# -*- coding: UTF-8 -*-
# python3

import subprocess
import sys
from devolib.util_log import LOG_D, LOG_E

# 检查是否安装了 Node.js
def check_node_or_quit():
    try:
        result = subprocess.run(['node', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            LOG_E("`node` not installed!")
            sys.exit(1)
        else:
            LOG_D(f"`node` version: {result.stdout.strip()}")
    
    except FileNotFoundError:
        LOG_E("`node` or `npm` not found!")
        sys.exit(1)

# 检查并安装 terser
def check_module_or_install(mod_name):
    check_node_or_quit()

    try:
        result = subprocess.run(['npm', 'install', 'terser', '--save-dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            LOG_E(f"`terser` install failed: {result.stderr}!")
            sys.exit(1)
        else:
            LOG_D("`terser` install ok.")
    
    except FileNotFoundError:
        LOG_E("`node or `npm` not found!")
        sys.exit(1)