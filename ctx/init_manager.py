#!/usr/bin/with-contenv python3
# -*- coding: utf-8 -*-
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.configure import Configure as CFG
from config.configure_setter import ConfigureSetter as CS


class InitManager:
    def __init__(self, ):
        self.cfg = CFG() # Configure
        self.cs = CS() # ConfigureSetter

    def run(self, ):
        self.print_banner()
        self.cfg.logger.info(f"[INIT_CONFIG] Initializing Configuration")
        for key, value in self.cfg.compose_env.items():
            self.cfg.logger.info(f"[INIT_CONFIG] {key} = {value} ({type(value).__name__})")

        if self.cfg.compose_env.get('LOCAL_TEST') is True:
            ip_type = "LOCAL_TEST"
        else:
            ip_type = "PUBLIC"
        self.cfg.logger.info(f"[INIT_CONFIG] GOLOOP_P2P = \"{self.cfg.config['settings']['icon2']['GOLOOP_P2P']}\" ({ip_type})")

        settings = self.cfg.config['settings']['env']
        if settings:
            for key, value in settings.items():
                if key != "COMPOSE_ENV":
                    if key == 'KEY_PASSWORD' and len(value):
                        value = '*' * len(str(value))
                    self.cfg.logger.info(f"[DOCKER_ENV] {key} = {value} ({type(value).__name__})")

        settings = self.cfg.config['settings']['icon2']
        if settings:
            for key, value in settings.items():
                if value is not None:
                    self.cfg.logger.info(f"[ICON2] {key} = {value} ({type(value).__name__})")

        self.cs.create_yaml_file()
        self.cs.create_env_file()
        self.cs.make_base_dir()
        # if self.cfg.config['settings']['env'].get('IS_AUTOGEN_CERT') is True:
        self.cs.create_key()
        self.cs.create_genesis_json()
        self.cs.create_gs_zip()
        self.cs.create_icon_config()
        self.cs.create_db()
        self.cfg.logger.info("--- Finish initializing ---")

    def print_banner(self):
        v_info = self.cfg.get_version()
        self.cfg.logger.info(f" ██████╗████████╗██╗  ██╗")
        self.cfg.logger.info(f"██╔════╝╚══██╔══╝╚██╗██╔╝")
        self.cfg.logger.info(f"██║        ██║    ╚███╔╝  Goloop Version: {v_info.get('VERSION')}")
        self.cfg.logger.info(f"██║        ██║    ██╔██╗  CTX Version:    {v_info.get('VCS_REF')}")
        self.cfg.logger.info(f"╚██████╗   ██║   ██╔╝ ██╗ Build Date:     {v_info.get('BUILD_DATE')}")
        self.cfg.logger.info(f" ╚═════╝   ╚═╝   ╚═╝  ╚═╝")


if __name__ == '__main__':
    IM = InitManager()
    IM.run()
