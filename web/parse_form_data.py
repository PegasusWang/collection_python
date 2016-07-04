#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import re
import requests
try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3

def form_data_to_dict(s):
    arg_list = [line.strip() for line in s.split('\n')]
    d = {}
    for i in arg_list:
        if i:
            k = i.split(':')[0].strip()
            v = ''.join(i.split(':')[1:]).strip()
            d[k] = v
    return d


FORMS_DATA = """
__business_id:712764242174174
_reqName:path:/act_858751837556226/customaudiences
_reqSrc:adsDaoGraphDataMutator
accountId:858751837556226
creation_params:{"combination_type":"website","traffic_type":4}
description:
endpoint:/act_858751837556226/customaudiences
exclusions:[{"type":"website","retention_days":30,"rule":"{\"and\":[{\"or\":[{\"url\":{\"i_contains\":\"\"}}]}]}","rule_aggregation":null}]
inclusions:[{"type":"website","retention_days":180,"rule":"{\"and\":[{\"or\":[{\"url\":{\"i_contains\":\"\"}}]}]}","rule_aggregation":null}]
locale:zh_CN
method:post
name:tt
pixel_id:1792170334346121
prefill:true
pretty:0
subtype:combination
suppress_http_code:1
"""


if __name__ == '__main__':
    import pprint
    pprint.pprint(forms_data_to_dict(FORMS_DATA))
