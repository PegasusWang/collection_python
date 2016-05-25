#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from io import open
import sys
from pprint import pprint


def dict_string_to_dict(dict_string):
    dict_string = dict_string.replace('\n', '').replace(' ', '')
    d = ast.literal_eval(dict_string)
    return d


def pprint_dict(d):
    pprint(d)



if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
    except IndexError:
        exit()
    with open(filepath, 'r' , encoding='utf-8') as f:
        pprint_dict(dict_string_to_dict(f.read()))

#     dict_string = """{0: {'instagram_id': '', 'image_hash': 'fcd37b937e5c95a84d96ef1dc603eea5', 'page_id': '599379080235405', 'tex
#         t': {'body': '1', 'description': '1', 'title': '1'}, 'os': '', 'tracking_url': 'https://www.amazon.com'}, 1:
#         {'instagram_id': '', 'image_hash': 'fcd37b937e5c95a84d96ef1dc603eea5', 'page_id': '599379080235405', 'text':
#         {'body': '24', 'description': '42', 'title': '32'}, 'os': '', 'tracking_url': 'https://www.amazon.com'}, 2: {
#             'instagram_id': '', 'image_hash': 'e7e9a4e087ab2f4bb7a000d27722cd95', 'page_id': '599379080235405', 'text': {
#                 'body': '1', 'description': '1', 'title': '1'
#             }, 'os': '', 'tracking_url': 'https://www.amazon.com'
#         }, 3: {'ins
#                 tagram_id': '', 'image_hash': 'e7e9a4e087ab2f4bb7a000d27722cd95', 'page_id': '599379080235405', 'text': {'bod
#                 y': '24', 'description': '42', 'title': '32'}, 'os': '', 'tracking_url': 'https://www.amazon.com'}}"""
#     pprint_dict(dict_string_to_dict(dict_string))
