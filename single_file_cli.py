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




class TemplateCLI(object):

    def __init__(self, config=None):
        self.config = config
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-v', '--version', action="version", version=__version__,
                                  help="Print version information and quit")
        self._parser.add_argument("-a", "--all", action="store_true", help="Show all containers (default shows just running)")
        self._parser.add_argument("-f", "--filter", type=str, help="Filter output based on conditions provided (default [])")
        self._parser.add_argument("--format", help="Pretty-print containers using a Go template")
        self._parser.add_argument("-n", "--last", type=int,default=0,
                                help="Show n last created containers (includes all states) (default -1)")
        self._parser.add_argument("-l", "--latest", help="Show the latest created container (includes all states)")
        self._parser.add_argument("--no-trunc", help="Don't truncate output")
        self._parser.add_argument("-q", "--quiet", help="Only display numeric IDs")
        self._parser.add_argument("-s", "--size", help="Display total file sizes")

        self._parser.add_argument("fix_mode",
                            choices=[
                                "onstart",
                                "current_deploy_version_id_missing",
                                "update_application_service_id"],
                            help=textwrap.dedent("""
                                  onstart: 启动时修复异步任务，节点状态等
                                  update_application_service_id: 从注册中心获取service id
                                  current_deploy_version_id_missing: 修复部署id缺失"""))

        self.args = self._parser.parse_args()

    def run(self):
        log.debug("start run")
        print(self.args)

if __name__ == "__main__":
    cli = TemplateCLI()
    cli.run()
