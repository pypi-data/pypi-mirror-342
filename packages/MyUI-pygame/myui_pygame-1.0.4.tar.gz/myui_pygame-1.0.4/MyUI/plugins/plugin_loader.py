"""
Core loader. Load plugins and then return them to be applicated in any app.
"""
import importlib.util
import json
import os
from typing import Literal, Optional, List, Dict, Any
from .plugin_base import Plugin
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
import threading

# For clean console output from multiple threads
print_lock = threading.Lock()

class PluginWrapper:
    """A wrapper of a plugin, I wonder whats inside?"""
    def __init__(self, plugin: Plugin, config: Dict[str, Any], path: str, entry: str):
        self.plugin: Plugin = plugin  # The actual plugin object (class instance)
        self.config: Dict[str, Any] = config  # Contents of plugin.json
        self.path: str = path      # Path to plugin folder
        self.entry_name: str = entry

        self.internal_desc: str = plugin.__doc__

        self.index: int = -1 # Index can also play as a form of ID in rendering in the app. This is to easily keep track.

    @property
    def plugin_name(self) -> str:
        """The name of the plugin."""
        return self.config.get("name", "UnknownPlugin")

    @property
    def name(self) -> str:
        """The name of the plugin and the entry."""
        return f"{self.plugin_name}-{self.entry_name}"

    @property
    def version(self) -> str:
        """The version of the plugin."""
        return self.config.get("version", "0.0.0")

    @property
    def author(self) -> str:
        """The author of the plugin."""
        return self.config.get("author", "Unknown")

    @property
    def description(self) -> str:
        """The description of the plugin."""
        return self.config.get("description", "")
    
    @property
    def tags(self) -> List[str]:
        """The tags of the plugin"""
        return self.config.get("tags", [])
    
    @property
    def layer(self) -> Literal["background", "normal", "top", "none"]:
        """The layer the plugin is configured on."""
        return self.config.get("layer", "normal")

    @property
    def enabled(self) -> bool:
        """If the plugin is set as enabled in it's config."""
        return self.config.get("enabled", True)
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set and persist the enabled state in config.json."""
        self.config["enabled"] = value
        self.update_config()
    
    def update_config(self) -> None:
        config_path = os.path.join(self.path, "config.json")

        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
            print(f"[PluginWrapper] Updated '{self.name}'s configuration.")
        except Exception as e:
            print(f"[PluginWrapper] Failed to update config for '{self.name}': {e}")

    def __repr__(self):
        return f"<PluginWrapper {self.name} v{self.version} by {self.author}>"

def _load_single_plugin(plugin_path: str, plugin_dir: str) -> List[PluginWrapper]:
    wrappers = []

    config_path = os.path.join(plugin_path, "config.json")
    if not os.path.isfile(config_path):
        return wrappers

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        entry_file = config.get("main", "main.py")
        full_entry_path = os.path.join(plugin_path, entry_file)

        if not os.path.isfile(full_entry_path):
            with print_lock:
                print(f"[WARN] Entry file missing in {plugin_dir}")
            return wrappers

        spec = importlib.util.spec_from_file_location(plugin_dir, full_entry_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        entry_classes = config.get("entries")
        if not entry_classes:
            entry_classes = [config.get("entry", "Plugin")]

        for entry_class in entry_classes:
            if not hasattr(mod, entry_class):
                with print_lock:
                    print(f"[WARN] Entry class '{entry_class}' missing in {plugin_dir}")
                continue

            args: List[Any] = config.get("args", [])
            kwargs: Dict[str, Any] = config.get("kwargs", {})

            plugin_instance = getattr(mod, entry_class)(*args, **kwargs)
            wrapper = PluginWrapper(plugin_instance, config, plugin_path, entry_class)
            wrappers.append(wrapper)

    except Exception as e:
        with print_lock:
            print(f"[ERROR] Failed to load plugin from {plugin_dir}: {e}")

    return wrappers

def load_plugins_from(folder: str) -> List[PluginWrapper]:
    """
    Load all plugins from a folder in parallel.
    Each plugin error is caught individually so all others still load.
    """
    plugin_paths = [
        os.path.join(folder, name)
        for name in sorted(os.listdir(folder))
        if os.path.isdir(os.path.join(folder, name)) and not name.startswith("__")
    ]

    all_wrappers: List[PluginWrapper] = []
    plugin_names = set()

    def safe_load(path: str, name: str):
        try:
            return _load_single_plugin(path, name)
        except Exception:
            print(f"\n[!] Error loading plugin: {name}")
            traceback.print_exc()
            return []  # Return empty list so main thread can extend safely

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(safe_load, path, os.path.basename(path))
            for path in plugin_paths
        ]

        for future in as_completed(futures):
            wrappers = future.result()
            for wrapper in wrappers:
                if wrapper.name in plugin_names:
                    print(f"[!] Duplicate loaded plugin name: {wrapper.name}")
                    continue
                plugin_names.add(wrapper.name)
                all_wrappers.append(wrapper)

    return all_wrappers

def create_dict(plugins: List[PluginWrapper]) -> Dict[str, PluginWrapper]:
    """
    Converts a list of PluginWrapper instances into a dictionary for fast access by plugin name.

    This function is useful for efficiently retrieving or modifying plugins by name before 
    loading them into the application.

    Args:
        plugins (List[PluginWrapper]): A list of plugin wrapper instances.

    Returns:
        Dict[str, PluginWrapper]: A dictionary mapping plugin names to their corresponding PluginWrapper.
    """
    return {wrapper.entry_name: wrapper for wrapper in plugins}

def get_plugin_group(plugins: List[PluginWrapper], name: str) -> List[PluginWrapper]:
    """
    Get the group of wrappers (per entry) for a specified plugin name.
    """
    wrappers: List[PluginWrapper] = []
    for wrapper in plugins:
        if wrapper.plugin_name == name:
            wrappers.append(wrapper)
    return wrappers

del Plugin, Literal, Optional, List, Dict, Any