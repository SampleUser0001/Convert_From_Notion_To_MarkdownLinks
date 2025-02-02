# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG, NOTSET
import os

# import sys
from logutil import LogUtil

from importenv import ImportEnvKeyEnum
import unittest

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)

from importenv import ImportEnvKeyEnum

def apply_logger(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # メソッドかどうか確認
            logger_name = f"{__name__}.{cls.__name__}.{attr_name}"
            decorated = LogUtil.dynamic_logger(logger_name)(attr_value)
            setattr(cls, attr_name, decorated)
    return cls

@apply_logger
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
        self.logger.info(f'ImportEnvKeyEnum.SAMPLE.value : {ImportEnvKeyEnum.SAMPLE.value}')
        self.assertEqual(ImportEnvKeyEnum.SAMPLE.value, 'test')