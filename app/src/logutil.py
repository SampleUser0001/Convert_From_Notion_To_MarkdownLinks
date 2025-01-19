# -*- coding: utf-8 -*-
import json
import os

class LogUtil:

    @classmethod
    def get_log_conf(cls, log_conf_path):
        """ ログ設定ファイルを読み込む
        """
        with open(log_conf_path, mode='r') as f:
            log_conf = json.loads(f.read())
            log_conf['handlers']['fileHandler']['filename'] = os.getenv('PYTHON_APP_HOME') + '/' + log_conf['handlers']['fileHandler']['filename']
            log_conf['handlers']['testFileHandler']['filename'] = os.getenv('PYTHON_APP_HOME') + '/' + log_conf['handlers']['testFileHandler']['filename']
            
            # テストファイルのログ設定を更新する。
            test_config = log_conf['loggers']['test']
            for name in cls.find_test_file():
                log_conf['loggers'][name] = test_config
        return log_conf
    
    @classmethod
    def find_test_file(cls):
        """ テスト用のファイルを探す
        """
        test_files = []
        app_dir = os.path.join(os.getenv('PYTHON_APP_HOME'), *['src'])
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(file.replace('.py', ''))
        return test_files
