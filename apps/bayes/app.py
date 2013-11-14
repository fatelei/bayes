#!/usr/bin/python
#-*-coding: utf8-*-

import os
import argparse

from bayes.core.bayes import Bayes
from settings import SUPPORT_CATEGORY


def run():
    parser = argparse.ArgumentParser(description='bayes')
    parser.add_argument('--train_dir', metavar='train_dir',
                        dest='train_dir', type=str, required=True, help='train dir')
    parser.add_argument('--test_dir', metavar='test_dir',
                        dest='test_dir', type=str, help='test file')
    parser.add_argument('--test', metavar='test_file',
                        dest='test_file', type=str, help='test files')
    parser.add_argument('--stop_words', metavar='stop words',
                        dest='stop_words', help='stop words')
    parser.add_argument('--predict_label', metavar='predict_label',
                        dest='predict_label', type=str, required=True,
                        help='predict label: sport|it|car|tour|education|military|finance|recruitment|health|cultural')
    args = parser.parse_args()

    if not args.test_dir and not args.test_file:
        parser.print_help()
    else:
        if args.predict_label not in SUPPORT_CATEGORY:
            parser.print_help()
        else:
            bayes = Bayes(args.train_dir, stop_words_txt=args.stop_words)
            bayes.train()
            if args.test_file:
                bayes.classify(test_file=args.test_file, predict_label=args.predict_label)
            if args.test_dir:
                bayes.classify(test_dir=args.test_dir, predict_label=args.predict_label)
