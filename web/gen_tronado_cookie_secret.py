#!/usr/bin/env python
# -*- coding:utf-8 -*-

import uuid
import base64


print base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes)
