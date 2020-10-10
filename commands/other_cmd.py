#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

from .base_cmd import SubCommandBase

class RunCommand(SubCommandBase):

    name = "run"  # 命令名

    weight = 0  # 子命令排序权重

    description = "Run a command in a new container"


class ExecCommand(SubCommandBase):

    name = "exec"  # 命令名

    weight = 0  # 子命令排序权重

    description = "Run a command in a running container"
