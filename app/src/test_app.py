# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG
import os

# import sys
from logutil import LogUtil

from importenv import ImportEnvKeyEnum
import unittest

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False


from importenv import ImportEnvKeyEnum
class TestUtil(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_Environment(self):
        logger.info(f'ImportEnvKeyEnum.SAMPLE.value : {ImportEnvKeyEnum.SAMPLE.value}')
        self.assertEqual(ImportEnvKeyEnum.SAMPLE.value, 'test')