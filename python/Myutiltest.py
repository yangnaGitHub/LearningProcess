#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import unittest

from mydict import Dict
class TestDict(unittest.TestCase):
    def test_init(self):
        d = Dict(a = 1, b = "test")
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, "test")
        self.assertTrue(isinstance(d, dict))
    def test_key(self):
        d = Dict()
        d["key"] = "value"
        self.assertEqual(d.key, "value")
    def test_attr(self):
        d = Dict()
        d.key = "value"
        self.assertTrue("key" in d)
        self.assertEqual(d["key"], "value")
    def test_keyerror(self):
        d = Dict()
