from __future__ import annotations

import os
from typing import Optional

import yaml


class Config:
    ORIGN_ADDR = os.getenv("ORIGN_ADDR", "https://orign.agentlabs.xyz")
    AGENTSEA_API_KEY = os.getenv("AGENTSEA_API_KEY")
    NEBU_PROXY_URL = os.getenv("NEBU_PROXY_URL", "https://proxy.agentlabs.xyz")

    @classmethod
    def refresh(cls):
        """Refresh configuration by reloading environment variables."""
        cls.ORIGN_ADDR = os.getenv("ORIGN_ADDR", "https://orign.agentlabs.xyz")  # noqa: A001
        cls.AGENTSEA_API_KEY = os.getenv("AGENTSEA_API_KEY")
        cls.NEBU_PROXY_URL = os.getenv("NEBU_PROXY_URL", "https://proxy.agentlabs.xyz")


class GlobalConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        server: Optional[str] = None,
        debug: bool = False,
    ):
        self.api_key = api_key or Config.AGENTSEA_API_KEY
        self.server = server or Config.ORIGN_ADDR
        self.debug = debug

    def write(self) -> None:
        home = os.path.expanduser("~")
        dir = os.path.join(home, ".agentsea")
        os.makedirs(dir, exist_ok=True)
        path = os.path.join(dir, "orign.yaml")

        with open(path, "w") as yaml_file:
            yaml.dump(self.__dict__, yaml_file)
            yaml_file.flush()
            yaml_file.close()

    @classmethod
    def read(cls) -> GlobalConfig:
        home = os.path.expanduser("~")
        dir = os.path.join(home, ".agentsea")
        os.makedirs(dir, exist_ok=True)
        path = os.path.join(dir, "orign.yaml")

        if not os.path.exists(path):
            return GlobalConfig()

        with open(path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            return GlobalConfig(**config)
