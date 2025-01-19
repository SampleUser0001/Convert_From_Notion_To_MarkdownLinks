# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from util.sample import Util
from controller import SampleController

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

def sample_func():
    logger.info('hoge')
    logger.debug('hoge')

if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。
    
    logger.info('This is logger message!!')
    logger.debug('This is logger message!!')

    # .envの取得
    logger.info(f'ImportEnvKeyEnum.SAMPLE.value : {ImportEnvKeyEnum.SAMPLE.value}')

    sample_func()

    Util.print()
    
    SampleController().print_log()