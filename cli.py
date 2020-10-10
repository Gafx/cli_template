#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
"""
command line interface template
"""

import argparse
import logging
from commands import SUB_COMMANDS


__version__ = "0.0.1"


class TemplateCLI(object):
    
    
    def __init__(self, config=None):
        self.config = config
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-v', '--version', action="version", version=__version__,
                                  help="Print version information and quit")

        self.subparser = self._parser.add_subparsers(title="Commands",metavar="COMMAND")

        # 按照命令权重依次注册命令，权重越大 排序越靠前
        for handler_cls in sorted(SUB_COMMANDS.values(), key=lambda item: item.weight, reverse=True):
            handler = handler_cls()
            handler.register(self.subparser.add_parser(
                handler.name,
                help=handler.description,
                description=handler.description,
                formatter_class=argparse.RawTextHelpFormatter))
            

        self.args = self._parser.parse_args()

    def run(self):
        self.args.func(self.args)




if __name__ == "__main__":
    cli = TemplateCLI()
    cli.run()
