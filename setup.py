#!/usr/bin/python
#-*-coding: utf8-*-

from setuptools import find_packages, setup

install_requires = ['jieba==0.31',
                    'gevent']

entry_points = """
    [console_scripts]
    bayes=bayes.app:run
"""

setup(
    author='fatelei@gmail.com',
    name='bayes',
    version='0.1',
    entry_points=entry_points,
    install_requires=install_requires,
    packages=find_packages('apps'),
    package_dir={'': 'apps'}
)
