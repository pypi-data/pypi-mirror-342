"""
MyUI - The perfect tool for UI operations. Everything from text input to buttons and sliders!

Provides many utilities. Create a *App* reference to get started, and everything else should be 
straight forward!
"""

print("Booting MyUI...")

from .preseting import FontScheme, Theme
from .ui import adjust_color, Text, Button, PushButton, ToggleButton, Slider, DropdownMenu, Tooltip, Dropbox, Window, Surface, HotbarItem, Hotbar, App
from .plugins import PluginBase, PluginWrapper, load_plugins_from
from typing import Union

component = Union[ui.component, plugins.component, preseting.component]

del Union

print("Welcome to MyUI! If your interested in how we work, please check out our python package: [link]")