#!/usr/bin/env python
# -*- coding:utf-8 -*-

#pip install Pygments
#pip insatll markdown2
from markdown2 import markdown, markdown_path


def md_to_html(md):
    """对于代码块\n\n```\n\n + codeblock + \n\n```\n\n"""
    return markdown(md, extras= ["code-friendly", 'fenced-code-blocks'])
