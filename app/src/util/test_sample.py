# -*- coding: utf-8 -*-
import unittest
import sample

class TestUtil(unittest.TestCase):
    def test_print(self):
        self.assertEqual(sample.Util.print(), 'This is Util')
