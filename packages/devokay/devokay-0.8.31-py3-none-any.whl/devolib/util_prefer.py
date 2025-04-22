# -*- coding: UTF-8 -*-
# python3

import os
import json

from devolib import DynamicObject

CONFIG_DIR = ".devo"
CONFIG_FILE = "conf.json"

profile_dir = os.path.expanduser("~")
conf_dir = os.path.join(profile_dir, CONFIG_DIR)
conf_file = os.path.join(conf_dir, CONFIG_FILE)

preferences = DynamicObject(log_level='debug', log_dir=None)

if os.path.exists(conf_file):
    with open(conf_file, 'r') as file:
        json_obj = json.load(file)
        if json_obj is not None:
            # logger settings
            if 'log' in json_obj:
                log = json_obj['log']
                if 'level' in log:
                    preferences.log_level = log['level']

                if 'dir' in log:
                    preferences.log_dir = log['dir']

            # others settings
