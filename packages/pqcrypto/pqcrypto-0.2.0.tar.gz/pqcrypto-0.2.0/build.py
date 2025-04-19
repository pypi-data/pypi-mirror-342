"""
A custom build hook for Hatchling to execute compilation and modify the build tag.

Modifies the build tag to include the Python version and platform information.
This is important for pqcrypto since it contains C extensions and is separately built for specific platforms.

For clarity:
This hook results in filenames like `pqcrypto-<version>-cp313-cp313-manylinux_2_35_x86_64` instead of the generic `pqcrypto-<version>-py3-none-any`
"""

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from packaging.tags import sys_tags


class BuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        tag = next(sys_tags())
        build_data["tag"] = "-".join([tag.interpreter, tag.abi, tag.platform])
        return build_data
