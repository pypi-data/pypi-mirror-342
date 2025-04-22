# -*- coding: UTF-8 -*-
# python3

# slimit is for : not suitable

# We are using `Terser`

import subprocess
from devolib.util_log import LOG_E, LOG_D
from devolib.util_env import check_module_or_install

# 压缩代码
def minified(input_file, output_file):
    check_module_or_install("terser")

    try:
        # 定义不需要混淆的函数/变量名
        reserved_names = ["CallCef"]

        # 构建 terser 命令，使用 --mangle-reserved 参数指定保留的名称
        result = subprocess.run(
            [
                'npx',
                'terser', 
                input_file, 
                '--mangle',
                '--mangle-reserved', *reserved_names, 
                '--compress', "drop_console=['log']", 
                '-o', output_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            LOG_D(f"minified ok")
        else:
            LOG_E(f"压缩失败: {result.stderr}")

    except Exception as e:
        LOG_E(f"Error during minification: {e}")