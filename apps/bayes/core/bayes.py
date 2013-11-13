#!/usr/bin/python
#-*-coding: utf8-*-

"""
用于生成特定领域的训练集
"""

import jieba
import gevent
import os

from .stop_words import get_stop_words
from settings import CATEGORY


class Bayes(object):

    def __init__(self, train_dir, stop_words_txt):
        self.train_dir = train_dir
        self.words_category = {}
        self.docs_count = {}
        self.stop_words = get_stop_words(stop_words_txt)
        self.total_count = 0

    def calc_probability(self, category, words):
        """
        计算条件概率
        """
        docs_count = self.docs_count[category]
        pc = float(docs_count) / self.total_count
        px = 1

        for k, v in words:
            px = px * (float(v) / docs_count)
        probability = pc * pk
        return probability

    def participle(self, category, filename, pos):
        """
        分词
        """
        pos = str(pos)
        if category not in self.words_category:
            self.words_category[category] = {}
        if pos not in self.words_category[category]:
            self.words_category[category][pos] = set()
        with open(filename) as f:
            content = f.read()
            seg_iterator = jieba.cut(content, cut_all=False)
            for word in seg_iterator:
                if len(word) == 0:
                    continue
                if word in self.stop_words:
                    continue
                self.words_category[category][pos].add(word)

    def train(self):
        """
        开始训练
        """
        for dirpath, dirnames, filenames in os.walk(self.train_dir):
            if len(dirnames) == 0:
                func = lambda x: os.path.join(dirpath, x)
                process_paths = map(func, filenames)
                dirname = dirpath.split('/')[-1]
                category = CATEGORY[dirname]
                print category
                if category not in self.docs_count:
                    self.docs_count[category] = len(process_paths)
                self.total_count += len(process_paths)
                jobs = [gevent.spawn(self.participle, category, path, pos)
                                for pos, path in enumerate(process_paths)]
                gevent.joinall(jobs)

    def learn(self, words_vector):
        """
        开始学习
        """
        label = ''
        words_category_count = {}
        rst = -1 << 32
        for word in words_vector:
            for k, v in self.words_category.iteritems():
                if k not in words_category_count:
                    words_category_count[k] = {}
                if word not in words_category_count[k]:
                    words_category_count[k][word] = 0
                for i, s in v.iteritems():
                    if word in s:
                        words_category_count[k][word] += 1

        for k, v in words_category_count:
            cur_probability = self.calc_probability(k, v)

            if rst < cur_probability:
                rst = cur_probability
                label = k
        print label, rst

    def classify(self, test_file=None, test_dir=None):
        """
        文本分类
        """
        words_vector = set()
        if test_file and not test_dir:
            with open(test_file) as f:
                content = f.read()
                seg_iterator = jieba.cut(content, cut_all=False)
                for word in seg_iterator:
                    if len(word) == 0:
                        continue
                    if word in self.stop_words:
                        continue
                    words_vector.add(word)
            self.learn(words_vector)
        elif not test_file and test_dir:
            pass
        else:
            print 'no test file'
            return

