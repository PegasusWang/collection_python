#!/usr/bin/env python
# -*- coding: utf-8 -*-

s = """{0: {'instagram_id': '', 'image_hash': 'fcd37b937e5c95a84d96ef1dc603eea5', 'page_id': '599379080235405', 'tex
     t': {'body': '1', 'description': '1', 'title': '1'}, 'os': '', 'tracking_url': 'https://www.amazon.com'}, 1:
     {'instagram_id': '', 'image_hash': 'fcd37b937e5c95a84d96ef1dc603eea5', 'page_id': '599379080235405', 'text':
      {'body': '24', 'description': '42', 'title': '32'}, 'os': '', 'tracking_url': 'https://www.amazon.com'}, 2: {
          'instagram_id': '', 'image_hash': 'e7e9a4e087ab2f4bb7a000d27722cd95', 'page_id': '599379080235405', 'text': {
              'body': '1', 'description': '1', 'title': '1'
          }, 'os': '', 'tracking_url': 'https://www.amazon.com'
      }, 3: {'ins
             tagram_id': '', 'image_hash': 'e7e9a4e087ab2f4bb7a000d27722cd95', 'page_id': '599379080235405', 'text': {'bod
             y': '24', 'description': '42', 'title': '32'}, 'os': '', 'tracking_url': 'https://www.amazon.com'}}"""


s = s.replace('\n', '').replace(' ', '')
import ast
from pprint import pprint
d = ast.literal_eval(s)
pprint(d)
