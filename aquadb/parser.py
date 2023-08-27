# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25 23:26

import os
import re


def search_statement_parse(query, index=-1):
    """
    从给定的文本中提取 SQL 语句并返回。

    Parameters:
        query (str): 包含 SQL 语句的字符串。
        index (int, optional): 要获取的 SQL 语句在列表中的索引。支持负数索引。默认为 -1。

    Returns:
        str or list: 如果提供了 index，则返回索引处的 SQL 语句；否则，返回包含所有提取的 SQL 语句的列表。

    Raises:
        ValueError: 如果没有识别到相关的 SQL 语句。
        IndexError: 如果指定的索引超出范围。

    Examples:
        >>> query_text = "SELECT * FROM users; -- Get user data\nINSERT INTO logs VALUES ('login'); /* Log activity */"
        >>> search_statement_parse(query_text)
        ['SELECT * FROM users', "INSERT INTO logs VALUES ('login')"]

        >>> query_text = "SELECT * FROM orders; INSERT INTO logs VALUES ('order placed');"
        >>> search_statement_parse(query_text, index=0)
        'SELECT * FROM orders'
    """
    # 移除 /* */注释内容
    text_without_comments = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
    # 去除每行开头的 -- 注释
    text_lines = text_without_comments.split('\n')
    text_without_comments = '\n'.join(line for line in text_lines if not line.strip().startswith('--'))

    # 使用正则表达式匹配 SQL 语句
    sql_statements = re.split(r';\s*(?!--)', text_without_comments)
    # 去掉分号和空元素
    sql_statements = [sql.replace(";", "").strip() for sql in sql_statements if sql.strip()]

    if not sql_statements:
        raise ValueError("没有识别到相关的SQL语句，请检查输入是否有误")

    if index is not None:
        if index < 0:
            index += len(sql_statements)  # 支持负数索引，从后往前计数
        if 0 <= index < len(sql_statements):
            return sql_statements[index]
        else:
            raise IndexError("索引超出范围")
    else:
        return sql_statements


def textfile_search_parse(file_path, index=-1):
    """
    解析文本文件中的SQL语句。

    Parameters
    ----------
    file_path : str
        存放SQL的文件路径及文件名。

    index : int or None, optional
        SQL语句的位置索引。默认为-1，即返回文件中最后一个语句。
        如果为None，将返回所有的语句列表。

    Returns
    -------
    str or list of str
        解析出的SQL语句。如果index不为None，则返回字符串。
        如果index为None，则返回语句列表。

    Raises
    ------
    FileNotFoundError
        如果文件不存在。

    ValueError
        如果未能识别到SQL语句。

    Notes
    -----
    1. 本函数将读取指定文件，解析出文件中的SQL语句，并返回。
    2. 注释内容会被移除，包括 /* */ 和 -- 形式的注释。
    3. SQL语句以分号分隔，可以通过指定索引来获取特定的语句。

    Examples
    --------
    >>> file_path = "path/to/your/sql_file.sql"
    >>> result = textfile_search_parse(file_path)
    >>> print(result)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("没有找到相关的文件")

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 移除 /* */注释内容
    text_without_comments = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # 去除每行开头的 -- 注释
    text_lines = text_without_comments.split('\n')
    text_without_comments = '\n'.join(line for line in text_lines if not line.strip().startswith('--'))

    # 使用正则表达式匹配 SQL 语句
    sql_statements = re.split(r';\s*(?!--)', text_without_comments)
    # 去掉分号和空元素
    sql_statements = [sql.replace(";", "").strip() for sql in sql_statements if sql.strip()]

    if not sql_statements:
        raise ValueError("没有识别到相关的SQL语句，请检查输入是否有误")

    if index is not None:
        if index < 0:
            index += len(sql_statements)  # 支持负数索引，从后往前计数
        if 0 <= index < len(sql_statements):
            return sql_statements[index]
        else:
            raise IndexError("索引超出范围")
    else:
        return sql_statements


def textfile_procedure_parser(file_path, index=-1):
    """
    从指定文件中解析出SQL语句块。

    Parameters
    ----------
    file_path : str
        存放SQL的文件路径及文件名。

    index : int or None, optional
        SQL语句块的位置索引。默认为-1，即返回文件中最后一个语句块。
        如果为None，将返回所有的语句块列表。

    Returns
    -------
    str or list of str
        解析出的SQL语句块。如果index不为None，则返回字符串。
        如果index为None，则返回语句块列表。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("没有找到相关的文件")

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 使用非贪婪模式匹配declare和end;之间的内容
    sql_blocks = re.findall(r"(declare.*?end;)", text, re.DOTALL)

    if index is not None:
        if index < 0:
            index += len(sql_blocks)  # 支持负数索引，从后往前计数
        if 0 <= index < len(sql_blocks):
            return sql_blocks[index]
        else:
            raise IndexError("索引超出范围")
    else:
        return sql_blocks
