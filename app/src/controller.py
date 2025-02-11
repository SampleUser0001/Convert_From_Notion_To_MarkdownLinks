# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG, NOTSET
import os

# import sys
from logutil import LogUtil
import pandas as pd

import glob

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

def apply_logger(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # メソッドかどうか確認
            logger_name = f"{__name__}.{cls.__name__}.{attr_name}"
            decorated = LogUtil.dynamic_logger(logger_name)(attr_value)
            setattr(cls, attr_name, decorated)
    return cls

@apply_logger
class MappingController():
    def __init__(self, input_dir_path) -> None:
        """ コンストラクタ
        
            Parameters
            ----------
            input_dir_path : str
                Notionからエクスポートしたディレクトリのパス
        """
        self.input_dir_path = input_dir_path
    
    def map(self):
        all_csv_path = self._get_csv_path()
        self.logger.info(f'all_csv_path : {all_csv_path}')
        
        name_set = self._csv_load(all_csv_path)
        self.logger.debug(f'name_set : {name_set}')
        
        markdown_list = self._find_markdown(self._find_directory(all_csv_path))
        
        return self._mapping(name_set, markdown_list)
    
    def _get_csv_path (self):
        """ self.input_dir_path から_all.csvファイルのパスを取得する 
        
            Returns
            -------
            str
                CSVファイルのパス
        """
        for root, dirs, files in os.walk(os.path.join(self.input_dir_path)):
            for file in files:
                if file.endswith('_all.csv'):
                    return os.path.join(root, file)
        return None

    def _csv_load(self, filepath):
        """ CSVファイルを読み込む。Nameだけ取得して、Setで返す。 """
        df = pd.read_csv(filepath, usecols=[0], header=0)
        return set(df.iloc[:, 0].tolist())

    def _find_directory(self, csv_path):
        """ CSVファイルのパスからディレクトリを取得する

            Parameters
            ----------
            csv_path : str
                CSVファイルのパス
        """
        directory = os.path.join(csv_path.replace('_all.csv', ''))
        return directory
    
    def _find_markdown(self, directory):
        """ ディレクトリからMarkdownファイルのリストを取得する 
            Parameters
            ----------
            directory : str
                Markdownファイルが格納されているディレクトリのパス
            
            Returns
            -------
            List[str]
                Markdownファイルのパスのリスト
        """
        return glob.glob(f'{directory}/**/*.md', recursive=True)
    
    def _mapping(self, name_set, file_path_list):
        """ CSVのNameとファイルパスのリストを紐付ける。
            同一Nameに対してMarkdownが複数ある可能性がある。(Notionの仕様。)
            uuidで一意になるが、Nameからは判断できないので、同じキーに複数ファイルを紐付ける。
            つまり、{str: List[str]} の辞書を返す。
            
            Parameters
            ----------
            name_set : Set[str]
                _all.csvのNameのセット
            file_path_list : List[str]
                Markdownのファイルパスのリスト
                
            Returns
            -------
            Dict[str, List[str]]
                Nameをキーにした、Markdownのファイルパスのリスト
        """

        self.logger.debug(f'name_set : {name_set}')
        self.logger.debug(f'markdown_list : {file_path_list}')

        found_all = []
        return_dict = {}
        # Nameを降順にソート。先頭が同じで、後ろが異なる場合、後ろの方が優先されるようにする。
        for name in reversed(list(name_set)):
            self.logger.debug(f'name : {name}')
            found_file_path_list = []
            for file_path in file_path_list:
                if name in file_path and file_path not in found_all:
                    found_file_path_list.append(file_path)
                    found_all.append(file_path)
            return_dict[name] = found_file_path_list
        return return_dict