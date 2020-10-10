#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

from .base_cmd import SubCommandBase

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