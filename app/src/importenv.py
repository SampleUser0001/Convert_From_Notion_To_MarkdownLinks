# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
import json
from enum import Enum

env_path = join(dirname(__file__), 'environment.json')
json_open = open(env_path, 'r')

class ImportEnvKeyEnum(Enum):
    """ .envファイルのキーを書く """
    SAMPLE = json.load(json_open)['SAMPLE']
