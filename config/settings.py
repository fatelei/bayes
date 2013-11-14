#!/usr/bin/python
#-*-coding: utf8-*-

import os

ROOT_DIR = '/'.join(os.path.dirname(__file__).split('/')[:-1])

# 停用词文件
STOP_WORD_FILE = os.path.join(ROOT_DIR, 'data/stop_words.txt')

# 训练集分类
CATEGORY = {
    'C000007': u'汽车',
    'C000008': u'财经',
    'C000010': u'IT',
    'C000013': u'健康',
    'C000016': u'旅游',
    'C000014': u'体育',
    'C000020': u'教育',
    'C000022': u'招聘',
    'C000023': u'文化',
    'C000024': u'军事'
    } 

SUPPORT_CATEGORY = [
    'it',
    'cultural',
    'recruitment',
    'education',
    'car',
    'tour',
    'military',
    'sport',
    'finance',
    'health'
    ]