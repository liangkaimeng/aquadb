# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/24

# print("\033[91m{}\033[0m".format("This is red text"))  # 红色
# print("\033[92m{}\033[0m".format("This is green text"))  # 绿色
# print("\033[94m{}\033[0m".format("This is blue text"))  # 蓝色

from marslib.query import fetch_all, fetch_one, read_table
from marslib.executor import to_execute, to_proceduce
from marslib.parser import textfile_search_parse, textfile_procedure_parser

user = 'scott'
# file = '456.sql'
file = '123.sql'
# file = '234.sql'

# res = fetch_all(user, file, index=-1, format_table=True)
# print(res)
print(help(fetch_all))
