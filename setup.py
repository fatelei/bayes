#!/usr/bin/python
#-*-coding: utf8-*-

from setuptools import find_package, setup

install_requires = ['jieba']

entry_points = """
    [console_scripts]
    bayes:bayes.app:run
"""

setup(
    author='fatelei@gmail.com',
    name='bayes',
    version='0.1',
    entry_points=entry_points,
    install_requires=install_requires,
    packages=find_package('apps'),
    package_dir={'': 'apps'}
)
