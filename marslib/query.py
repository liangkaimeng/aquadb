# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25

import time
import warnings
import cx_Oracle
import pandas as pd
from marslib import connection
from marslib import parser
from prettytable import PrettyTable

warnings.filterwarnings("ignore")


def create_pretty_table(data_list, headers):
    """
    创建一个格式化的PrettyTable对象来显示数据。

    Parameters
    ----------
    data_list : list of lists
        包含数据行的二维列表。

    headers : list of str
        列名列表。

    Returns
    -------
    PrettyTable
        格式化后的PrettyTable对象。

    Notes
    -----
    1. 本函数接受一个二维数据列表和列名列表，返回一个用于显示数据的格式化PrettyTable对象。
    2. `data_list` 包含了数据行，每个数据行是一个列表。
    3. `headers` 是列名列表，用于设置表格的列名。

    Examples
    --------
    >>> data_list = [
    ...     ["Alice", 25, "Engineer"],
    ...     ["Bob", 30, "Designer"],
    ...     ["Charlie", 28, "Manager"]
    ... ]
    >>> headers = ["Name", "Age", "Occupation"]
    >>> table = create_pretty_table(data_list, headers)
    >>> print(table)
    """
    table = PrettyTable()
    table.field_names = headers

    for row in data_list:
        table.add_row(row)

    return table


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print("\033[92m程序运行结束，运行时间{:.0f}小时{:.0f}分{:.2f}秒.\033[0m".format(hours, minutes, seconds))


def read_table(usr, file=None, query=None, index=-1, **kwargs):
    """
    从数据库中查询结果并返回DataFrame。

    Parameters
    ----------
    usr : str
        数据库用户名。

    file : str, optional
        存放SQL查询语句的文件路径。可以一个文件存放多个语句。

    query : str, optional
        SQL查询语句。

    index : int, optional
        位置索引，用于在SQL文件中获取查询语句。默认为-1，表示取最后一个语句。

    kwargs : dict
        与 pandas 模块相关的其他参数。

    Returns
    -------
    pandas.DataFrame
        查询结果的数据表。

    Raises
    ------
    cx_Oracle.Error
        如果在数据库连接或查询过程中出现错误。

    ValueError
        如果未指定查询语句或无法从文件中获取查询语句。

    Notes
    -----
    1. 本函数从数据库中查询数据，并将结果返回为 DataFrame。
    2. 如果未提供查询语句 `query`，将尝试从文件 `file` 中获取语句。
    3. `index` 参数指定在文件中选择哪个语句，默认为 -1，表示选择最后一个语句。

    Examples
    --------
    >>> usr = "your_db_username"
    >>> query = "SELECT * FROM your_table"
    >>> result = read_table(usr, query=query)
    >>> print(result)
    """
    start_time = time.time()  # 记录开始时间
    try:
        connect = connection.get_connection_from_pool(usr)

        if not query:
            query = parser.textfile_search_parse(file, index)

        try:
            table = pd.read_sql(query, con=connect, **kwargs)
            return table
        except Exception as error:
            raise error
        finally:
            connect.close()
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()  # 记录结束时间
        seconds = end_time - start_time  # 计算运行时间
        seconds_to_hms(seconds)


def fetch_all(usr, file=None, query=None, index=-1, format_table=True, head=5):
    """
    使用cx_Oracle游标的方式查询数据并进行格式化输出。

    Parameters
    ----------
    usr : str
        数据库用户名。

    file : str, optional
        存放SQL查询语句的文件路径，可以一个文件存放多个语句。

    query : str, optional
        数据库查询语句。

    index : int, optional
        索引位置，用于在SQL文件中获取查询语句。默认为 -1，表示取最后一个。

    format_table : bool, optional
        是否格式化输出表格。默认为 True，即默认格式化。

    head : int or None, optional
        输出前N条数据，默认值为 5，即默认输出前五条数据。如果 head 为 None 或 0，则输出全部。

    Returns
    -------
    PrettyTable or list of tuples
        格式化后的输出表格（使用 PrettyTable 格式化）或元组列表（如果不格式化）。

    Raises
    ------
    cx_Oracle.Error
        如果在数据库连接或查询过程中出现错误。

    Notes
    -----
    1. 本函数使用 cx_Oracle 游标方式查询数据，并提供了格式化输出的选项。
    2. 如果未提供查询语句 `query`，将尝试从文件 `file` 中获取语句。
    3. 可以通过设置 `format_table` 为 False，输出原始的元组列表。
    4. 可以通过设置 `head` 为 None 或 0，输出所有数据。

    Examples
    --------
    >>> usr = "your_db_username"
    >>> query = "SELECT * FROM your_table"
    >>> result = fetch_all(usr, query=query)
    >>> print(result)
    """
    start_time = time.time()  # 记录开始时间
    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if not query:
            query = parser.textfile_search_parse(file, index)

        cursor.execute(query)
        field_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

        if format_table:
            table = PrettyTable()
            table.field_names = field_names
            if head:
                for row in result[:head]:
                    table.add_row(row)
            else:
                for row in result:
                    table.add_row(row)
        else:
            table = result

        cursor.close()
        connect.close()

        return table
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()  # 记录结束时间
        seconds = end_time - start_time  # 计算运行时间
        seconds_to_hms(seconds)


def fetch_one(usr, file=None, query=None, index=-1, format_table=True):
    """
    使用cx_Oracle游标的方式查询单条数据并进行格式化输出。

    Parameters
    ----------
    usr : str
        数据库用户名。

    file : str, optional
        存放SQL查询语句的文件路径，可以一个文件存放多个语句。

    query : str, optional
        数据库查询语句。

    index : int, optional
        索引位置，用于在SQL文件中获取查询语句。默认为 -1，表示取最后一个。

    format_table : bool, optional
        是否格式化输出表格。默认为 True，即默认格式化。

    Returns
    -------
    PrettyTable or tuple
        格式化后的输出表格（使用 PrettyTable 格式化）或单条记录的元组。

    Raises
    ------
    cx_Oracle.Error
        如果在数据库连接或查询过程中出现错误。

    Notes
    -----
    1. 本函数使用 cx_Oracle 游标方式查询单条数据，并提供了格式化输出的选项。
    2. 如果未提供查询语句 `query`，将尝试从文件 `file` 中获取语句。

    Examples
    --------
    >>> usr = "your_db_username"
    >>> query = "SELECT * FROM your_table WHERE id = 1"
    >>> result = fetch_one(usr, query=query)
    >>> print(result)
    """
    start_time = time.time()  # 记录开始时间
    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if not query:
            query = parser.textfile_search_parse(file, index)

        cursor.execute(query)
        field_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()

        if format_table:
            table = PrettyTable()
            table.field_names = field_names
            table.add_row(result)
        else:
            table = result

        cursor.close()
        connect.close()
        return table
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()  # 记录结束时间
        seconds = end_time - start_time  # 计算运行时间
        seconds_to_hms(seconds)
