"""配置加载模块。

提供 :class:`Config` 数据模型与全局单例，支持基于 TTL 与文件 mtime
的自动重载，避免每次访问都触发磁盘 IO。
"""

from __future__ import annotations

import threading
import time
import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

TTL: int = 30
"""配置缓存有效期（秒），到期后下次访问会触发 mtime 检查。"""

class Config(BaseModel):
    """运行时配置数据模型。"""

    allowed_referrers: list[str] = Field(default_factory=list)
    ua_blacklist: list[str] = Field(default_factory=list)
    fs_base: list[str] = Field(default_factory=list)
    sign_token: str = Field(default="")


def _ensure_config_file(path: Path) -> Path:
    """确保配置文件存在，不存在时按 :class:`Config` 默认值生成。"""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                Config().model_dump(),
                f,
                allow_unicode=True,
                sort_keys=False,
            )
    return path


def get_config_path() -> Path:
    """解析配置文件路径。

    优先使用环境变量 ``CONFIG_PATH``，否则回退到项目根目录下的
    ``config.yaml``。若目标文件不存在则自动创建并填充默认内容。
    """
    if cfg_path := os.environ.get("CONFIG_PATH"):
        return _ensure_config_file(Path(cfg_path).expanduser().resolve())
    default_path = Path(__file__).resolve().parent.parent / "config.yaml"
    return _ensure_config_file(default_path)


CONFIG_PATH: Path = get_config_path()
"""配置文件绝对路径，默认位于项目根目录下的 ``config.yaml``。"""


class _ConfigManager:
    """线程安全的配置单例管理器。

    访问策略：
    - 距上次加载不足 :data:`TTL` 秒时直接返回缓存；
    - 超过 TTL 后检查文件 mtime，仅在文件实际变更时才重新解析。
    """

    _instance: "_ConfigManager | None" = None
    _singleton_lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "_ConfigManager":
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst._init()
                    cls._instance = inst
        return cls._instance

    def _init(self) -> None:
        self._config: Config = Config()
        self._loaded_at: float = 0.0
        self._mtime: float = -1.0
        self._reload_lock: threading.Lock = threading.Lock()

    @staticmethod
    def _read_file() -> Config:
        if not CONFIG_PATH.exists():
            return Config()
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"配置文件根节点必须为映射，实际为: {type(data).__name__}")
        return Config.model_validate(data)

    @staticmethod
    def _stat_mtime() -> float:
        try:
            return CONFIG_PATH.stat().st_mtime
        except OSError:
            return 0.0

    def get(self, *, force: bool = False) -> Config:
        """获取当前配置，必要时触发自动重载。

        Args:
            force: 强制重新读取文件，忽略 TTL 与 mtime 缓存。
        """
        now = time.monotonic()
        if not force and (now - self._loaded_at) < TTL:
            return self._config

        with self._reload_lock:
            now = time.monotonic()
            if not force and (now - self._loaded_at) < TTL:
                return self._config

            mtime = self._stat_mtime()
            if force or mtime != self._mtime:
                self._config = self._read_file()
                self._mtime = mtime
            self._loaded_at = now
            return self._config

    def reload(self) -> Config:
        """立即强制重新加载配置并返回最新实例。"""
        return self.get(force=True)


def get_config() -> Config:
    """返回当前生效的 :class:`Config` 实例（带 TTL 缓存）。"""
    return _ConfigManager().get()


def reload_config() -> Config:
    """强制重新加载并返回最新的 :class:`Config` 实例。"""
    return _ConfigManager().reload()


__all__ = ["Config", "TTL", "CONFIG_PATH", "get_config", "reload_config"]
