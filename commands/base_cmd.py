#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

SUB_COMMANDS = {}

class CommandRegister(type):
    def __new__(meta, name, bases, class_dic):
        cls = type.__new__(meta, name, bases, class_dic)
        if cls.name is not None:
            if cls.name not in SUB_COMMANDS:
                SUB_COMMANDS[cls.name] = cls
            else:
                raise ValueError("already exist command:{}".format(cls.name))

        return cls


class SubCommandBase(object):

    name = None  # 命令名

    weight = 0  # 子命令排序权重,权重大 排序在上面

    description = None  # 子命令描述，帮助信息

    __metaclass__ = CommandRegister

    def register(self, parser):
        self.add_arguments(parser)
        parser.set_defaults(func=self.run)

    def add_arguments(self, parser):
        pass

    def run(self,args):
        print("run {} with:{}".format(self.name,args))
