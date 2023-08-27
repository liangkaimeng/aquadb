# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25 0:46

import cx_Oracle
from aquadb import configurator


def get_connection_from_pool(usr):
    try:
        username, password, host, port, service_name = configurator.get_config(usr=usr)
        connection_str = f'{username}/{password}@{host}:{port}/{service_name}'
        connection = cx_Oracle.connect(connection_str)
        return connection
    except Exception as e:
        raise ConnectionError(f"Failed to connect to the database: {e}")
