# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from enum import Enum

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class ImportEnvKeyEnum(Enum):
    """ .envファイルのキーを書く """
    SAMPLE = os.getenv("SAMPLE")
