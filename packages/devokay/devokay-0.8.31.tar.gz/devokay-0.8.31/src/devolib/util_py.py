# -*- coding: UTF-8 -*-
# python3

from devolib.pyminifier import pyminify
from devolib.util_log import LOG_E
from devolib import DynamicObject

# 压缩代码
def minified(code):
    try:
        # TODO: 未完成
        # return minification.js_minify(code)
        return None
    except Exception as e:
        LOG_E(f"Error during minification: {e}")
        return None

# 压缩文件 
def minified(files):
    try:
        # TODO: 未完成
        args = DynamicObject(path="/Users/fallenink/Desktop/Developer/devokay-py/tmp/pcsdk.json")
        return pyminify(args, files)
    except Exception as e:
        LOG_E(f"Error during minification: {e}")
        return None

if __name__ == '__main__':
    # 需要压缩的 JavaScript 代码
    js_code = """
    function greet() {
        console.log("Hello, World!"); // Print greeting
    }
    greet();
    """
    
    minified_js = minified(js_code)

    # 输出结果
    print("Minified JavaScript:")
    print(minified_js)