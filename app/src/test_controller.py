# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG, NOTSET
import os

# import sys
from logutil import LogUtil

from controller import MappingController
from importenv import ImportEnvKeyEnum
import unittest

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)

def apply_logger(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # メソッドかどうか確認
            logger_name = f"{__name__}.{cls.__name__}.{attr_name}"
            decorated = LogUtil.dynamic_logger(logger_name)(attr_value)
            setattr(cls, attr_name, decorated)
    return cls

@apply_logger
class TestMappingController(unittest.TestCase):
    
    def setUp(self):
        self.controller = MappingController(
            os.path.join(
                PYTHON_APP_HOME, 
                *[ImportEnvKeyEnum.INPUT_DIR.value]))

    def test_map(self):
        """mapメソッドが正常に動作するかテスト"""
        actual = self.controller.map()
        
        markdown_dir = os.path.join(PYTHON_APP_HOME, 'test_input', '8', 'Test Data 5')

        expected = {}
        expected['テスト用ノート 2'] = [os.path.join(markdown_dir, 'テスト用ノート 2 d.md')]
        expected['テスト用ノート'] = [
            os.path.join(markdown_dir, 'テスト用ノート a.md'),
            os.path.join(markdown_dir, 'テスト用ノート b.md')
        ]

        self.assertEqual(type(actual), type(expected))
        self.assertTrue('テスト用ノート 2' in actual.keys())
        self.assertEqual(actual['テスト用ノート 2'], [os.path.join(markdown_dir, 'テスト用ノート 2 d.md')])

        self.assertTrue('テスト用ノート' in actual.keys())
        self.assertEqual(actual['テスト用ノート'], [
            os.path.join(markdown_dir, 'テスト用ノート a.md'),
            os.path.join(markdown_dir, 'テスト用ノート b.md')
        ])

        self.assertEqual(actual, expected)
        
    def test_get_csv_path(self):
        """_get_csv_pathメソッドがCSVファイルのパスを返すかテスト"""
        actual = self.controller._get_csv_path()
        expected = os.path.join(
            PYTHON_APP_HOME, *[
                'test_input', 
                '8',
                'Test Data 5_all.csv'
            ])
        self.assertEqual(actual, expected)
    
    def test_csv_load(self):
        """_csv_loadメソッドがCSVファイルを読み込んでセットで返すかテスト"""
        actual = self.controller._csv_load(self.controller._get_csv_path())
        expected = {
            'テスト用ノート',
            'テスト用ノート 2'
        }
        self.assertEqual(actual, expected)

    def test_find_directory(self):
        """_find_directoryメソッドがCSVファイルのパスからディレクトリを取得するかテスト"""
        actual = self.controller._find_directory(self.controller._get_csv_path())
        expected = os.path.join(
            PYTHON_APP_HOME, *[
                'test_input', 
                '8',
                'Test Data 5'
            ])
        self.assertEqual(actual, expected)
    
    def test_find_markdown(self):
        """ Markdownファイルのみ取得できることを確認する"""
        markdown_dir = self.controller._find_directory(self.controller._get_csv_path())
        actual = self.controller._find_markdown(self.controller._find_directory(self.controller._get_csv_path()))
        expected = [
            os.path.join(markdown_dir,'テスト用ノート 2 d.md'),
            os.path.join(markdown_dir,'テスト用ノート a.md'),
            os.path.join(markdown_dir,'テスト用ノート b.md')
        ]
        self.assertEqual(sorted(actual), sorted(expected))
    
    def test_mapping(self):
        """_mappingメソッドがCSVのNameとファイルパスのリストを紐付けるかテスト"""
        
        csv_path = self.controller._get_csv_path()
        name_set = self.controller._csv_load(csv_path)
        markdown_dir = self.controller._find_directory(csv_path)
        markdown_list = self.controller._find_markdown(markdown_dir)
        
        self.logger.debug(f'markdown_list : {markdown_list}')

        actual = self.controller._mapping(name_set, markdown_list)

        expected = {}
        expected['テスト用ノート 2'] = [os.path.join(markdown_dir, 'テスト用ノート 2 d.md')]
        expected['テスト用ノート'] = [
            os.path.join(markdown_dir, 'テスト用ノート a.md'),
            os.path.join(markdown_dir, 'テスト用ノート b.md')
        ]

        self.assertEqual(type(actual), type(expected))
        self.assertTrue('テスト用ノート 2' in actual.keys())
        self.assertEqual(actual['テスト用ノート 2'], expected['テスト用ノート 2'])

        self.assertTrue('テスト用ノート' in actual.keys())
        self.assertEqual(actual['テスト用ノート'], expected['テスト用ノート'])

        self.assertEqual(actual, expected)