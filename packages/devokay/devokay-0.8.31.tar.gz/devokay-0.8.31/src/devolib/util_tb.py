
# -*- coding: UTF-8 -*-
# python3

from devolib.util_log import LOG_E
from devolib.util_fs import write_file

from tabulate import tabulate

'''
@brief 打印表格
@example
    data = [
        ['Alice', 24]
    ]
    headers = [
        'Name', 'Age'
    ]
    tb_print(headers, data)
'''
def tb_print(headers, data):
    tabulate(data, headers)