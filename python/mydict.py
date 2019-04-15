#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
class Dict(dict):
    def __init__(self, **kw):
        super().__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("object is not Attribute %s" % key)
    def __setattr__(self, key, value):
        self[key] = value
