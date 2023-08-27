# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25 1:01

import time
import warnings
import cx_Oracle
from aquadb import connection
from aquadb import parser

warnings.filterwarnings('ignore')


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print("\033[92m程序运行结束，运行时间{:.0f}小时{:.0f}分{:.2f}秒.\033[0m".format(hours, minutes, seconds))


def to_execute(usr, file=None, query=None, index=None, commit=False, series=False, tolerant=False):
    """
    执行数据库查询或语句，即只执行增、删、改。

    Parameters
    ----------
    usr : str
        数据库用户名。

    file : str, optional
        存放SQL查询语句的文件路径，默认为 None。

    query : str or list of str, optional
        要执行的SQL查询语句，可以是字符串或字符串列表，默认为 None。

    index : int, optional
        当 query 是字符串列表时，指定要执行的语句索引，默认为 None。

    commit : bool, optional
        是否执行提交操作，即提交事务，默认为 False。

    series : bool, optional
        是否逐条执行多个语句，默认为 False。

    tolerant : bool, optional
        是否容忍异常，即遇到异常是否继续执行，默认为 False。

    Raises
    ------
    cx_Oracle.Error
        如果在连接数据库时出现错误。

    Exception
        如果在执行数据库查询或语句时出现错误。

    Notes
    -----
    1. 本函数执行数据库查询或语句，并提供了一些选项来控制执行行为。
    2. 可以选择执行单个语句或多个语句，以及是否提交事务。

    Examples
    --------
    >>> query = "SELECT * FROM employees"
    >>> to_execute('my_user', query=query, commit=True)
    """
    start_time = time.time()

    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if query is None:
            if not file is None:
                query = parser.textfile_search_parse(file, index)
            else:
                raise ValueError('数据类型错误。')
        else:
            query = parser.search_statement_parse(query, index)

        try:
            if series:  # 跑多个语句
                if not isinstance(query, list):
                    query = [query]

                error_count = 0
                for item in query:
                    try:
                        cursor.execute(item)
                    except Exception as error:
                        error_count += 1
                        if not tolerant:
                            raise error
                        else:
                            print("\033[94m异常代码：\n{}\033[0m".format(item))
                            print("\033[91m\U0001F622 {}\033[0m".format(error))

                if commit:
                    if error_count == 0:
                        connect.commit()
                    else:
                        connect.rollback()
            else:  # 跑单个语句
                try:
                    cursor.execute(query)
                    if commit:
                        connect.commit()
                except Exception as error:
                    print("\033[94m异常代码：\n{}\033[0m".format(query))
                    raise error

        except Exception as error:
            raise error

        finally:
            cursor.close()
            connect.close()

    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()
        seconds = end_time - start_time
        seconds_to_hms(seconds)


def to_proceduce(usr, file=None, query=None, index=None, series=False, tolerant=False):
    """
    执行存储过程或 SQL 匿名块。

    Parameters
    ----------
    usr : str
        数据库用户名。

    file : str, optional
        存放存储过程或 SQL 匿名块语句的文件路径，默认为 None。

    query : str or list of str, optional
        要执行的存储过程或 SQL 匿名块语句，可以是字符串或字符串列表，默认为 None。

    index : int, optional
        当 query 是字符串列表时，指定要执行的语句索引，默认为 None。

    series : bool, optional
        是否逐条执行多个语句，默认为 False。

    tolerant : bool, optional
        是否容忍异常，即遇到异常是否继续执行，默认为 False。

    Raises
    ------
    cx_Oracle.Error
        如果在连接数据库时出现错误。

    Exception
        如果在执行存储过程或 SQL 匿名块时出现错误。

    Notes
    -----
    1. 本函数执行存储过程或 SQL 匿名块，并提供了一些选项来控制执行行为。
    2. 可以选择执行单个语句或多个语句。

    Examples
    --------
    >>> procedure = "BEGIN my_procedure; END;"
    >>> to_procedure('my_user', query=procedure)
    """
    start_time = time.time()

    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if query is None:
            if not file is None:
                query = parser.textfile_procedure_parser(file, index)
            else:
                raise ValueError('数据类型错误。')

        try:
            if series:  # 跑多个语句
                if not isinstance(query, list):
                    query = [query]

                error_count = 0
                for item in query:
                    try:
                        cursor.execute(item)
                    except Exception as error:
                        error_count += 1
                        if not tolerant:
                            raise error
                        else:
                            print("\033[94m异常代码：\n{}\033[0m".format(item))
                            print("\033[91m\U0001F622 {}\033[0m".format(error))

            else:  # 跑单个语句
                try:
                    cursor.execute(query)
                except Exception as error:
                    print("\033[94m异常代码：\n{}\033[0m".format(query))
                    raise error
        except Exception as error:
            raise error
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()
        seconds = end_time - start_time
        seconds_to_hms(seconds)
