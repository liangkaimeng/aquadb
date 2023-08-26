# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/24

from setuptools import setup, find_packages


setup(
    name='marslib',
    version='1.1.1',
    author='梁开孟',
    author_email='519281809@qq.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'cx_Oracle>=8.3.0',
        'pandas>=1.5.3',
        'prettytable>=3.5.0'
    ],
)
