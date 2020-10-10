#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import os
import importlib

from .base_cmd import SUB_COMMANDS

# base_path = os.path.dirname(os.path.realpath(__file__))
# for file in os.listdir(base_path):
#     if file.endswith("_cmd.py") and file != '__init__.py':
#         importlib.import_module("." + file[:-3], package=os.path.basename(base_path))

from .other_cmd import *
from .ps_cmd import *