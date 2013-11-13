#!/usr/bin/python
#-*-coding: utf8-*-

"""
过滤停用词
"""

from settings import STOP_WORD_FILE


def get_stop_words(stop_words_txt):
    """
    获取停用词
    """
    stop_words_list = []
    func = lambda x: x.replace('\r\n', '').replace('\n', '').decode('gbk')

    if stop_words_txt:
        filename = stop_words_txt
    else:
        filename = STOP_WORD_FILE

    with open(filename) as f:
        stop_words = f.readlines()
        stop_words_list = map(func, stop_words)
    return stop_words_list
