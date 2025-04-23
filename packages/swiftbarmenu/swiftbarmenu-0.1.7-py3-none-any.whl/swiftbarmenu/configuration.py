from __future__ import annotations

from configparser import ConfigParser
import os
from pathlib import Path
from typing import Any


class Configuration:
    def __init__(self, auto_load: bool = True):
        """Initialize a Configuration."""

        self.file_path = Path(
            os.getenv('SWIFTBAR_PLUGIN_DATA_PATH', '.'),
            'config.ini'
        )
        self.config = ConfigParser()

        if auto_load and self.exists():
            self.load()

    def section(self, name: str) -> ConfigurationSection:
        return ConfigurationSection(self.config, name)

    def set(self, key: str, value: Any) -> Configuration:
        """
        Set a configuration value for a given key in the 'DEFAULT' section.

        Args:
            key (str): The key for the configuration value.
            value (Any): The value to set for the given key.

        Returns:
            Configuration: This instance of Configuration for method chaining.
        """

        self.section("DEFAULT").set(key, str(value))

        return self

    def get(self, key: str, default: Any = None, type: str = "str") -> Any:
        """
        Get a configuration value for a given key in the 'DEFAULT' section.

        Args:
            key (str): The key for the configuration value.
            default (any, optional): The default value to return if the key is not found. Defaults to `None`.
            type (str, optional): The type of the configuration value. Defaults to "str".

        Returns:
            Any: The configuration value for the given key, or the default value if not found.
        """

        return self.section("DEFAULT").get(key, default, type)

    def exists(self) -> bool:
        """Check if a persist Configuration file already exists."""

        return self.file_path.exists()

    def persist(self) -> Configuration:
        """Persist Configuration to a file."""

        with self.file_path.open('w') as config_file:
            self.config.write(config_file)

        return self

    def load(self) -> Configuration:
        """Load Configuration from a file."""

        if self.exists():
            self.config.read(self.file_path)

        return self

    def open_editor(self, app: str = "TextEdit") -> Configuration:
        """Open the configuration file in the specified app."""

        os.system(f"open -a '{app}' '{str(self.file_path)}'")

        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (f"Configuration(path='{self.file_path}')")


class ConfigurationSection:
    def __init__(self, config: ConfigParser, name: str):
        """Initialize a ConfigurationSection."""

        self.config = config
        self.name = name

        if not self.name == 'DEFAULT' and not self.config.has_section(name):
            self.config.add_section(name)

    def set(self, key: str, value: Any) -> ConfigurationSection:
        """
        Set a configuration  value for a given key of the section.

        Args:
            key (str): The key for the configuration value.
            value (Any): The value to set for the given key.

        Returns:
            Configuration: This instance of Configuration for method chaining.
        """

        self.config.set(self.name, key, str(value))

        return self

    def get(self, key: str, default: Any = None, type: str = "str") -> Any:
        """
        Get a configuration value for a given key of the section.

        Args:
            key (str): The key for the configuration value.
            default (any, optional): The default value to return if the key is not found. Defaults to `None`.
            type (str, optional): The type of the configuration value. Defaults to "str".

        Returns:
            Any: The configuration value for the given key, or the default value if not found.
        """

        if type == "int":
            default_v = int(default) if default is not None else None
            return self.config.getint(self.name, key, fallback=default_v)
        elif type == "float":
            default_v = float(default) if default is not None else None
            return self.config.getfloat(self.name, key, fallback=default_v)
        elif type == "bool":
            default_v = bool(default) if default is not None else None
            return self.config.getboolean(self.name, key, fallback=default_v)
        else:
            return self.config.get(self.name, key, fallback=default)
