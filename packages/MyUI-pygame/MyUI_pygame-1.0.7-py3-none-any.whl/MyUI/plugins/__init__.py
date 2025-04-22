"""
Use plugins to optimize adding utilities to a app in MyUI.
"""

from .plugin_base import Plugin as PluginBase
from .plugin_loader import PluginWrapper, load_plugins_from, create_dict, get_plugin_group
from typing import Union

component = Union[PluginBase, PluginWrapper]

del Union

print("- MyUI plugin loader")