# -*- coding: utf-8 -*-
"""
    Created by 亥虫 on 2019/7/6
"""
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from albumy import create_app
app = create_app('production')