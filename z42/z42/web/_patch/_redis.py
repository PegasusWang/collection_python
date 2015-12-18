#!/usr/bin/env python
# coding:utf-8
import _env
import logging
import redis.client
from redis.client import BasePipeline, NoScriptError
from hashlib import sha1





class Script(object):
    'An executable LUA script object returned by ``register_script``'

    def __init__(self, registered_client, script):
        self.registered_client = registered_client
        self.script = script
        self.sha = str(sha1(script).hexdigest())

    def __call__(self, keys=[], args=[], client=None):
        'Execute the script, passing any required ``args``'
        if client is None:
            client = self.registered_client


        args = tuple(keys) + tuple(args)
        # make sure the Redis server knows about the script
        if isinstance(client, BasePipeline):
            # make sure this script is good to go on pipeline
            client.script_load_for_pipeline(self)
        try:
            return client.evalsha(self.sha, len(keys), *args)
        except NoScriptError:
            # Maybe the client is pointed to a differnet server than the client
            # that created this instance?
            self.sha = client.script_load(self.script)
            return client.evalsha(self.sha, len(keys), *args)



redis.client.Script = Script

