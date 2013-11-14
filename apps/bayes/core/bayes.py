#!/usr/bin/python
#-*-coding: utf8-*-

"""
用于生成特定领域的训练集
"""

import jieba
import gevent
import os
import math

from .stop_words import get_stop_words
from settings import SUPPORT_CATEGORY


class Bayes(object):

    def __init__(self, train_dir, stop_words_txt=None):
        self.train_dir = train_dir
        self.stop_words = get_stop_words(stop_words_txt)
        self.cate_words_pro = {}
        self.cate_words_num = {}
        self.total_words_count = 0.0
        self.cate_doc_prefix = {}

    def participle(self, category, filename, pos):
        """
        分词
        """
        pos = str(pos)

        if category not in self.cate_words_num:
            self.cate_words_num[category] = 0.0

        with open(filename) as f:
            content = f.read()
            content = "".join(content.split())
            seg_iterator = jieba.cut(content, cut_all=False)
            for word in seg_iterator:
                if word.encode('utf8') in self.stop_words:
                    continue
                else:
                    key = '%s_%s' % (category, word)
                    if key not in self.cate_words_pro:
                        self.cate_words_pro[key] = 0.0
                    self.cate_words_pro[key] += 1.0
                    self.cate_words_num[category] += 1.0

    def train(self):
        """
        开始训练
        """
        func = lambda x: os.path.join(dirpath, x)
        for dirpath, dirnames, filenames in os.walk(self.train_dir):
            if len(dirnames) == 0:
                process_paths = map(func, filenames)
                category = dirpath.split('/')[-1]
                jobs = [gevent.spawn(self.participle, category, path, pos)
                        for pos, path in enumerate(process_paths)]
                gevent.joinall(jobs)

        for k, v in self.cate_words_num.iteritems():
            self.total_words_count += v

    def learn(self, words_vector):
        """
        开始学习
        """
        max_pro = -1 << 32
        category = None

        for cate in SUPPORT_CATEGORY:
            words_in_cate_num = self.cate_words_num[cate]
            pro = self.calc_probability(words_vector, cate, words_in_cate_num)
            if max_pro < pro:
                max_pro = pro
                category = cate
        return category, max_pro

    def calc_probability(self, words_vector, cate, words_in_cate_num):
        """
        计算概率
        """
        probability = 0.0
        for word in words_vector:
            key = '%s_%s' % (cate, word)
            if key in self.cate_words_pro:
                test_word_in_cate_num = self.cate_words_pro[key]
            else:
                test_word_in_cate_num = 0.0
            pc = (test_word_in_cate_num + 0.0001) / \
                (words_in_cate_num + self.total_words_count)
            probability = probability + math.log(pc)

        res = probability + math.log(words_in_cate_num) - math.log(self.total_words_count)
        return res

    def classify(self, test_file=None, test_dir=None, predict_label=None):
        """
        文本分类
        """
        words_vector = set()
        if test_file and not test_dir:
            with open(test_file) as f:
                content = f.read()
                seg_iterator = jieba.cut(content, cut_all=False)
                for word in seg_iterator:
                    if word.encode('utf8') in self.stop_words:
                        continue
                    else:
                        words_vector.add(word)
            label, _ = self.learn(words_vector)
            print label
        elif not test_file and test_dir:
            process_paths = []
            func = lambda x: os.path.join(dirpath, x)
            for dirpath, dirnames, filenames in os.walk(test_dir):
                if len(dirnames) == 0:
                    process_paths = map(func, filenames)

            good = 0
            bad = 0
            for path in process_paths:
                words_vector = set()
                with open(path) as f:
                    content = f.read()
                    seg_iterator = jieba.cut(content, cut_all=False)
                    for word in seg_iterator:
                        if word.encode('utf8') in self.stop_words:
                            continue
                        else:
                            words_vector.add(word)
                label, _ = self.learn(words_vector)

                if label == predict_label:
                    good += 1
                else:
                    bad += 1
            print 'right: %s' % (float(good) / len(process_paths))
            print 'bad: %s' % (float(bad) / len(process_paths))
        else:
            print 'no test file'
            return
