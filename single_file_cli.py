#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
"""
command line interface template
"""

import argparse
import logging

__version__ = "0.0.1"

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


class TemplateCLI(object):

    def __init__(self, config=None):
        self.config = config
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-v', '--version', action="version", version=__version__,
                                  help="Print version information and quit")

        self.subparser = self._parser.add_subparsers(title="Commands")

        for name, handler_cls in SUB_COMMANDS.items():
            handler = handler_cls()
            handler.register(self.subparser.add_parser(
                name, help=handler.description, description=handler.description))
            self._parser.set_defaults()

        # self._parser.add_argument('command', choices=self.supprt_command.keys(), help="taishan command")
        # self._parser.add_argument('command_args', nargs="*", help="taishan command args")
        self.args = self._parser.parse_args()

    def run(self):
        self.args.func(self.args)
        # runner = self.supprt_command.get(self.args.command)
        # if runner:
        #     runner()
        # else:
        #     log.error("Not found {} runner".format(self.args.command))


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


class PsCommand(SubCommandBase):

    name = "ps"  # 命令名

    weight = 0   # 子命令排序权重

    description = "List containers"  # 子命令描述，帮助信息

    def add_arguments(self, parser):
        parser.add_argument("-a", "--all",action="store_true", help="Show all containers (default shows just running)")
        parser.add_argument("-f", "--filter", type=str, help="Filter output based on conditions provided (default [])")
        parser.add_argument("--format", help="Pretty-print containers using a Go template")
        parser.add_argument("-n", "--last", type=int,
                            help="Show n last created containers (includes all states) (default -1)")
        parser.add_argument("-l", "--latest", help="Show the latest created container (includes all states)")
        parser.add_argument("--no-trunc", help="Don't truncate output")
        parser.add_argument("-q", "--quiet", help="Only display numeric IDs")
        parser.add_argument("-s", "--size", help="Display total file sizes")



class RunCommand(SubCommandBase):

    name = "run"  # 命令名

    weight = 0  # 子命令排序权重

    description = "Run a command in a new container"


class ExecCommand(SubCommandBase):

    name = "exec"  # 命令名

    weight = 0  # 子命令排序权重

    description = "Run a command in a running container"


if __name__ == "__main__":
    cli = TemplateCLI()
    cli.run()
