# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/24

import os
import base64
import warnings
import marslib
import configparser

warnings.filterwarnings('ignore')


def decrypt(text):
    """
    对Base64编码的文本进行解密。

    Parameters
    ----------
    text : str
        待解密的Base64编码文本。

    Returns
    -------
    str
        解密后的文本。

    Raises
    ------
    ValueError
        如果解密过程中出现错误。

    Notes
    -----
    1. 本函数接受一个Base64编码的文本，将其解码并返回原始文本。
    2. 解码过程涉及Base64解码和UTF-8解码。

    Examples
    --------
    >>> encrypted_text = "aGVsbG8gd29ybGQ="
    >>> decrypted_text = decrypt(encrypted_text)
    >>> print(decrypted_text)
    """
    return base64.b64decode(text).decode('utf-8')


def encryption(text):
    """
    对文本进行Base64编码加密。

    Parameters
    ----------
    text : str
        待加密的文本。

    Returns
    -------
    str
        加密后的Base64编码文本。

    Notes
    -----
    1. 本函数接受一个文本，将其进行UTF-8编码后，再进行Base64编码加密。
    2. 加密后的文本是Base64编码的字符串。

    Examples
    --------
    >>> original_text = "hello world"
    >>> encrypted_text = encryption(original_text)
    >>> print(encrypted_text)
    """
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def get_config(usr='scott', encoding='utf-8'):
    """
    从配置文件中获取数据库连接配置信息。

    Parameters
    ----------
    usr : str, optional
        用户名，默认为 'scott'。

    encoding : str, optional
        配置文件的编码格式，默认为 'utf-8'。

    Returns
    -------
    tuple
        包含解密后的用户、密码、主机、端口和SID的元组。

    Raises
    ------
    ValueError
        如果在配置文件中找不到指定用户的配置。

    Exception
        如果在读取配置文件时出现错误。

    Notes
    -----
    1. 本函数从配置文件中读取用户的数据库连接配置信息，解密敏感信息，并返回一个元组。
    2. 配置文件默认命名为 'ocl.ini'，存放在与 `marslib` 模块相同的目录中。
    3. 如果配置文件不存在，将创建一个空的配置文件。

    Examples
    --------
    >>> user, password, host, port, sid = get_config(usr='my_user')
    >>> print(user, password, host, port, sid)
    """
    filename = os.path.join(os.path.dirname(dreamlake.__file__), 'ocl.ini')

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            pass

    try:
        config = configparser.ConfigParser()
        config.read(filename, encoding=encoding)
        try:
            user = decrypt(config.get(usr, 'user'))
            password = decrypt(config.get(usr, 'password'))
            host = decrypt(config.get(usr, 'host'))
            port = decrypt(config.get(usr, 'port'))
            sid = decrypt(config.get(usr, 'sid'))
        except configparser.NoSectionError:
            raise ValueError(f"User '{usr}' not found in configuration file.")
    except Exception as error:
        raise error

    return user, password, host, port, sid


def add_config(user, password, host, port, sid, encoding='utf-8'):
    """
    向配置文件中添加数据库连接配置信息。

    Parameters
    ----------
    user : str
        数据库用户名。

    password : str
        数据库密码。

    host : str
        数据库主机名。

    port : str
        数据库端口。

    sid : str
        数据库SID。

    encoding : str, optional
        配置文件的编码格式，默认为 'utf-8'。

    Raises
    ------
    FileNotFoundError
        如果配置文件不存在。

    Notes
    -----
    1. 本函数将指定的数据库连接配置信息加密后添加到配置文件中。
    2. 配置文件默认命名为 'ocl.ini'，存放在与 `marslib` 模块相同的目录中。
    3. 如果配置文件不存在，将创建一个空的配置文件。

    Examples
    --------
    >>> user = "my_user"
    >>> password = "my_password"
    >>> host = "localhost"
    >>> port = "1521"
    >>> sid = "ORCL"
    >>> add_config(user, password, host, port, sid)
    """
    filename = os.path.join(os.path.dirname(dreamlake.__file__), 'ocl.ini')

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            pass

    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename, encoding=encoding)

        config[user] = {
            'user': encryption(user),
            'password': encryption(password),
            'host': encryption(host),
            'port': encryption(port),
            'sid': encryption(sid)
        }

        with open(filename, 'w') as configfile:
            config.write(configfile)
    else:
        raise FileNotFoundError(f"Configuration file not found: {filename}")


def set_config(session, option, value, encoding='utf-8'):
    filename = os.path.join(os.path.dirname(dreamlake.__file__), 'ocl.ini')

    if not os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename, encoding=encoding)

        config.set(session, option, encryption(value))

        with open(filename, 'w') as configfile:
            config.write(configfile)
    else:
        raise FileNotFoundError(f"Configuration file not found: {filename}")
