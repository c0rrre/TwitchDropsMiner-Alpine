from __future__ import annotations

from typing import Any, TypedDict, TYPE_CHECKING

from yarl import URL

from utils import json_load, json_save
from constants import CONFIG_PATH, SETTINGS_PATH, DEFAULT_LANG

if TYPE_CHECKING:
    from main import ParsedArgs


class SettingsFile(TypedDict):
    proxy: URL
    language: str
    dark_theme: bool
    autostart: bool
    exclude: set[str]
    priority: list[str]
    priority_only: bool
    prioritize_by_ending_soonest: bool
    autostart_tray: bool
    connection_quality: int
    tray_notifications: bool
    window_position: str
    apprise_url: str


default_settings: SettingsFile = {
    "proxy": URL(),
    "priority": [],
    "exclude": set(),
    "dark_theme": False,
    "autostart": False,
    "priority_only": True,
    "prioritize_by_ending_soonest": False,
    "autostart_tray": False,
    "connection_quality": 1,
    "language": DEFAULT_LANG,
    "tray_notifications": True,
    "window_position": "",
	"apprise_url": "",
}


class Settings:
    # from args
    log: bool
    tray: bool
    no_run_check: bool
    # args properties
    debug_ws: int
    debug_gql: int
    logging_level: int
    # from settings file
    proxy: URL
    language: str
    dark_theme: bool
    autostart: bool
    exclude: set[str]
    priority: list[str]
    priority_only: bool
    prioritize_by_ending_soonest: bool
    autostart_tray: bool
    connection_quality: int
    tray_notifications: bool
    window_position: str
    apprise_url: str

    PASSTHROUGH = ("_settings", "_args", "_altered")

    def __init__(self, args: ParsedArgs):
        self._settings: SettingsFile = json_load(SETTINGS_PATH, default_settings)
        self._args: ParsedArgs = args
        self._altered: bool = False
        CONFIG_PATH.mkdir(parents=True, exist_ok=True)

    # default logic of reading settings is to check args first, then the settings file
    def __getattr__(self, name: str, /) -> Any:
        if name in self.PASSTHROUGH:
            # passthrough
            return getattr(super(), name)
        elif hasattr(self._args, name):
            return getattr(self._args, name)
        elif name in self._settings:
            return self._settings[name]  # type: ignore[literal-required]
        return getattr(super(), name)

    def __setattr__(self, name: str, value: Any, /) -> None:
        if name in self.PASSTHROUGH:
            # passthrough
            return super().__setattr__(name, value)
        elif name in self._settings:
            self._settings[name] = value  # type: ignore[literal-required]
            self._altered = True
            return
        raise TypeError(f"{name} is missing a custom setter")

    def __delattr__(self, name: str, /) -> None:
        raise RuntimeError("settings can't be deleted")

    def alter(self) -> None:
        self._altered = True

    def save(self, *, force: bool = False) -> None:
        if self._altered or force:
            json_save(SETTINGS_PATH, self._settings, sort=True)
