# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

from logutil import LogUtil

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

class Util:
    @staticmethod
    def print():
        logger.info('Hello Util.')
        logger.debug('Hello Util.')
        return 'This is Util'