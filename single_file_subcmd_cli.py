#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
"""
command line interface template
"""
import textwrap
import argparse
import logging

__version__ = "0.0.1"

# ============ configs ===========
oss_endpoint = 'http://10.111.11.148:18091'
oss_bucket = 'bw-package'
oss_dir = "packages"
repo_root = "/data/registry-nginx0001/registry/package"

cdn_prefix = "https://package.baiwang.com"
expire_time = 50 * 365 * 24 * 3600

log_config = {"log_level": "DEBUG"}

# ======== endof configs =========

# ============ logger configs ===========
log = logging.getLogger(__name__)

def set_logger(config):
    _log_level = config.get("log_level") if config.get("log_level") else "INFO"
    log_level = getattr(logging, _log_level)
    log.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

set_logger(log_config)
# ============ endof logger configs ===========


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

    def run(self, args):
        print("run {} with:{}".format(self.name, args))


class TemplateCLI(object):

    def __init__(self, config=None):
        self.config = config
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-v', '--version', action="version", version=__version__,
                                  help="Print version information and quit")

        self.subparser = self._parser.add_subparsers(title="Commands", metavar="COMMAND")

        for name, handler_cls in SUB_COMMANDS.items():
            handler = handler_cls()
            handler.register(self.subparser.add_parser(
                name, help=handler.description, description=handler.description))
            self._parser.set_defaults()

        self.args = self._parser.parse_args()

    def run(self):
        self.args.func(self.args)


class PsCommand(SubCommandBase):

    name = "ps"  # 命令名

    weight = 0   # 子命令排序权重

    description = "List containers"  # 子命令描述，帮助信息

    def add_arguments(self, parser):
        parser.add_argument("-a", "--all", action="store_true", help="Show all containers (default shows just running)")
        parser.add_argument("-f", "--filter", type=str, help="Filter output based on conditions provided (default [])")
        parser.add_argument("--format", help="Pretty-print containers using a Go template")
        parser.add_argument("-n", "--last", type=int,
                            help="Show n last created containers (includes all states) (default -1)")
        parser.add_argument("-l", "--latest", help="Show the latest created container (includes all states)")
        parser.add_argument("--no-trunc", help="Don't truncate output")
        parser.add_argument("-q", "--quiet", help="Only display numeric IDs")
        parser.add_argument("-s", "--size", help="Display total file sizes")

    def run(self, args):
        print ("{}".format(args.all))
        print("run {} with:{}".format("ps", args))


class RunCommand(SubCommandBase):

    name = "run"  # 命令名

    weight = 0  # 子命令排序权重

    description = "Run a command in a new container"

    def add_arguments(self, parser):
        parser.add_argument("fix_mode",
                            choices=[
                                "onstart",
                                "current_deploy_version_id_missing",
                                "update_application_service_id"],
                            help=textwrap.dedent("""
                                  onstart: 启动时修复异步任务，节点状态等
                                  update_application_service_id: 从注册中心获取service id
                                  current_deploy_version_id_missing: 修复部署id缺失"""))


class ExecCommand(SubCommandBase):

    name = "exec"  # 命令名

    weight = 0  # 子命令排序权重

    description = "Run a command in a running container"


if __name__ == "__main__":
    cli = TemplateCLI()
    cli.run()
