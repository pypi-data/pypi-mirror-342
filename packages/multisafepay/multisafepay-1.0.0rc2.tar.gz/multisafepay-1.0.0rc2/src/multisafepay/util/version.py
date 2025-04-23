# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from pathlib import Path
from typing import Optional

from multisafepay.exception.missing_plugin_version import (
    MissingPluginVersionException,
)
from pydantic import BaseModel
from tomlkit import parse


class Version(BaseModel):
    """
    A class to represent the version information of a plugin and SDK.

    Attributes
    ----------
    plugin_version (Optional[str]): The version of the plugin, default is "unknown".
    sdk_version (Optional[str]): The version of the SDK, default is None.

    """

    plugin_version: Optional[str] = "unknown"
    sdk_version: Optional[str] = None

    @staticmethod
    def detect_sdk_version() -> str:
        """
        Detect the SDK version from the pyproject.toml file.

        Returns
        -------
        str: The detected SDK version.

        """
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        with open(pyproject_path) as file:
            content = parse(file.read())
        return content["tool"]["poetry"]["version"]

    def get_plugin_version(self) -> str:
        """
        Get the plugin version.

        Returns
        -------
        str: The plugin version.

        """
        return self.plugin_version

    def set_plugin_version(self, version: Optional[str]):
        """
        Set the plugin version.

        Parameters
        ----------
        version (Optional[str]): The version to set for the plugin.

        """
        self.plugin_version = version

    def get_sdk_version(self) -> Optional[str]:
        """
        Get the SDK version.

        Returns
        -------
        Optional[str]: The SDK version.

        """
        return self.sdk_version

    def set_sdk_version(self, version: str):
        """
        Set the SDK version.

        Parameters
        ----------
        version (str): The version to set for the SDK.

        """
        self.sdk_version = version

    def get_version(self) -> Optional[str]:
        """
        Get the combined version information of the plugin and SDK.

        Returns
        -------
        Optional[str]: The combined version information in the format "Plugin {plugin_version}; Python-Sdk {sdk_version}".

        Raises
        ------
        MissingPluginVersionException: If the plugin version is "unknown".

        """
        if self.plugin_version == "unknown":
            raise MissingPluginVersionException("Plugin version is missing")
        if self.sdk_version is None:
            self.sdk_version = Version.detect_sdk_version()

        return f"Plugin {self.plugin_version}; Python-Sdk {self.sdk_version}"
