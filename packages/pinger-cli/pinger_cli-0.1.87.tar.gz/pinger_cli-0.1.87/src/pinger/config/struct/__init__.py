from pydantic import BaseModel, Field
import yaml
from pathlib import Path
from typing import Optional, Dict
from enum import Enum


class DeployType(str, Enum):
    ecs = "ecs"
    lambda_ = "lambda"
    infra = "infra"


class InfraConfig(BaseModel):
    docker: bool = True


class CiConfig(BaseModel):
    ecr_repo_name: str = "ecr_repo_name"
    name: str = "ci"
    profile: str = "ci"


class CdConfig(BaseModel):
    region: str = "us-west-2"
    type: DeployType = DeployType.ecs


class AppConfig(BaseModel):
    name: str = "pinger"
    envs: str = "./envs"
    packages: str = "./packages"
    configs: str = "./configs"
    ci: CiConfig = Field(default_factory=CiConfig)
    cd: CdConfig = Field(default_factory=CdConfig)


class Config:
    _config: Optional[AppConfig] = None
    _raw: Optional[Dict] = None

    @classmethod
    def config(cls) -> AppConfig:
        if cls._config is None:
            cls._raw = cls.load_config()
            cls._config = AppConfig(**cls._raw)
        return cls._config

    @classmethod
    def raw(cls) -> Dict:
        if cls._raw is None:
            cls._raw = cls.load_config()
        return cls._raw

    @staticmethod
    def load_yaml_file(path: Path) -> Dict:
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    @classmethod
    def load_config(cls) -> Dict:
        locations = [
            Path("/etc/pinger/config.yml"),
            Path.home() / ".config/pinger/config.yml",
            Path(".pinger.yml"),
        ]

        merged: Dict = {}
        for path in locations:
            data = cls.load_yaml_file(path)
            merged.update(data)

        return merged
