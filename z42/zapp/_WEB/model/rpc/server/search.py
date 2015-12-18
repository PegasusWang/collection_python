#!/usr/bin/env python
#coding:utf-8
# -*- coding: utf-8 -*-
import _env
import hyperestraier
from _gearman import gearman
from z42.config import HYPERESTRAIER


@gearman.async
def index(db, id, txt, score=1):
    node = hyperestraier.Node()
    node.set_url(HYPERESTRAIER.URL+db)
    node.set_auth(HYPERESTRAIER.USER, HYPERESTRAIER.PASSWORD)

    uri = str(id)
    try:
        node.out_doc_by_uri(uri)
    except:
        import traceback
        traceback.print_exc()


    doc = hyperestraier.Document()
    doc.add_attr('@uri', uri)
    doc.add_text(txt.lower())
    doc.set_score(score)
    node.put_doc(doc)

