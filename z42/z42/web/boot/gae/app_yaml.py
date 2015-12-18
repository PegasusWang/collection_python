#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _env import PREFIX
from z42.config import GAE_APP_ID
import re
from mako.template import Template
from os import mkdir
from os.path import join, dirname, exists, isdir
from datetime import datetime


with open(join(PREFIX, 'app.template.yaml')) as conf:
    tmpl = conf.read()
T = Template(tmpl)


with open(join(PREFIX, 'app.yaml'), 'w') as conf:
    conf.write(
        T.render(
            GAE_APP_ID=GAE_APP_ID,
            version=str(datetime.today())[:10]
        )
    )

