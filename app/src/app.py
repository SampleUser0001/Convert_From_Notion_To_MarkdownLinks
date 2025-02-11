# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG, NOTSET
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from util.sample import Util
from controller import MappingController, GenerateIndexController

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
def sample_func():
    logger.info('hoge')
    logger.debug('hoge')

if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。
    
    logger.info('Generate Notion index.md Start!!')

    name_filepath_dict = MappingController(
        os.path.join(
            PYTHON_APP_HOME, 
            *[ImportEnvKeyEnum.INPUT_DIR.value])).map()
    
    GenerateIndexController(
        export_dir=os.path.join(
            PYTHON_APP_HOME, 
            *[ImportEnvKeyEnum.INPUT_DIR.value]),
        mapping_dict=name_filepath_dict).export()

    logger.info('Generate Notion index.md  Finish!!')