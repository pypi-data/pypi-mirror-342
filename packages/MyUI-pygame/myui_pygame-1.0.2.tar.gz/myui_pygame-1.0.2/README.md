# MyUI  
*A lightweight and intuitive UI extension for Pygame that simplifies interface development.*

---

### 🚀 Features  

✅ **UI Components** – Ready-to-use buttons, sliders, surfaces, and more    
✅ **Plugin System** – Easily extend and modularize your app's functionality    
✅ **Event Stack** – Simplified handling of custom and repeated events  
✅ **Layering System** – Clean separation of background, normal, and top-level layers   
✅ **Game & Tool Ready** – Built with flexibility for both games and utility applications   

---

## 📦 Installation  

Install via [PyPI](https://pypi.org/project/MyUI-pygame/):

```bash
pip install MyUI-pygame
```

## ⚡ Quick Start

### 1️⃣ Application Example

```Python
import MyUI
import pygame

# Load music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

# Initialize app
WIDTH, HEIGHT = 800, 600
app = MyUI.App((WIDTH, HEIGHT))
pygame.display.set_caption("Simple MyUI Demo")

# Load plugins from folder
plugin_wrappers = MyUI.load_plugins_from("plugins")

# Handle plugins before loading
plugin_group = MyUI.plugins.create_dict(MyUI.plugins.get_plugin_group(plugin_wrappers, "plugin"))
entry = plugin_group.get("entry")
print(entry.plugin_name) # Plugin name
print(entry.entry_name) # Entry name
print(entry.name) # Name is "plugin-entry", each plugin has seperate entries, each has seperate functions and different wrappers.

# Create a reload method
def reload_plugins():
    global plugin_wrappers
    plugin_wrappers = MyUI.load_plugins_from("plugins")
    app.reload(plugin_wrappers)

# Load fonts
fonts = MyUI.FontScheme(
    small1=pygame.font.SysFont("consolas", 15)
)

# Create a button
button = MyUI.PushButton(
    text="Reload!",
    font=fonts.small1,
    pos=(50, 50),
    size=(100, 30),
    color=(50, 50, 150),
    hover_color=(70, 70, 170),
    callback=reload_plugins
)

# Create a surface
surf = MyUI.Surface(
    pos=(100, 50),
    size=(200, 200),
    background_color=(200, 200, 250),
    border_color=(225, 225, 255),
    border_width=2,
    border_radius=5
)

# Add UI elements to the top layer
surf.add_handler(button.render, button.handle_event)
app.add_top(surf.render, surf.handle_event)

# Attach plugins
app.load_plugins(plugin_wrappers)

# Run the app
app.run()
```

### 2️⃣ Plugin System

Create modular plugin components using a simple configuration + Python file.

#### 📄 Plugin `config.json`
```JSON
{
    "name": "builtin",
    "version": "1.0.0",
    "author": "Neo",
    "description": "Builtin methods to simplify (e.g) statistics and feedback.",
    "tags": [
        "ui",
        "debugging",
        "statistics"
    ],
    "main": "main.py",
    "entries": [
        "Text"  // Class to locate as a entry*
    ],
    "layer": "top", // May be "top", "normal", "background", or "none"
    "enabled": true,

    // All below are optional
    "args": [ // The same as kwargs, but by order before the kwargs
        "value"
    ],

    "kwargs": {
        "argument name": "value"  // Tuples can be written as a list; define arguments when creating the plugin in the plugin loader.
    }
}
```

#### 🧠 Plugin `main.py`
```Python
# A basic example
import pygame
import math
from datetime import datetime
from MyUI import App

class Text:
    """Text renderer plugin.""" # Will be parsed as "internal_description" in the wrapper. Optional!

    def __init__(self):
        self.font: pygame.font.Font = pygame.font.SysFont("consolas", 15)
        self.offset: pygame.math.Vector2 = pygame.math.Vector2(-5, -5)
        self.color: pygame.Color = pygame.Color(50, 50, 50)

        self.app: App = None # App reference
        self.debug: bool = True

        self.updates: int = 0

    def update_time(self) -> None:
        now = datetime.now()
        self.date_time_str = now.strftime("%H:%M")

    def on_load(self, app) -> None:
        self.app = app
    
    def on_unload(self) -> None:
        pass
    
    def on_update(self) -> None:
        if self.updates % 100 == 0: self.update_time()
        self.updates += 1

    def on_render(self, surface: pygame.Surface):
        if self.app:
            text = f"{int(self.app.fps)} fps, {self.date_time_str}{f", {len(self.app.plugins)} plugins, {pygame.mouse.get_pos()}" if self.debug else ""}"
            text_surface = self.font.render(text, True, self.color)
            text_rect = text_surface.get_rect(bottomright=self.app.size + self.offset)

            # Optional drop shadow
            shadow = self.font.render(text, True, (0, 0, 0))
            surface.blit(shadow, text_rect.move(1, 1))

            surface.blit(text_surface, text_rect)

    def on_event(self, event: pygame.event.Event, offset: pygame.math.Vector2):
        pass
```

> 📁 Place plugin folders inside a top-level plugins/ directory. Each plugin should have its own subfolder containing the config.json and main script alongside any other related resource, like folders or related files.

## ℹ️ Tips & Additional Info

- **Plugin folder**: Ensure the `plugins` directory exists and contains properly structured plugin folders.
- **Font Management**: `MyUI.FontScheme` simplifies managing multiple font styles.
- **Themes**: Use `MyUI.Theme` to centralize and style your app’s color palette.
- **UI Layers**: Add renderables to `add_background()`, `add_normal()`, or `add_top()` for layer control.
- **Hot Reloading**: Reload plugins live with custom callbacks—great for debugging and rapid iteration.
- **Audio**: Fully compatible with Pygame’s `mixer` system for sound/music.

## 📜 License

This project is licensed under the MIT License.

## ⭐ Support the Project

If you find MyUI helpful, consider giving it a ⭐ on GitHub and contributing! Every bit of feedback or code helps keep development active. 🚀

---

## 🛠 Changelog

> A list of changes and fixes made across versions.

### v1.0.2

- 📦 Icons: PyPI seems to be unable to send png-images, thus, removed

- 🛠 Plugins: Small fix on `MyUI.plugins.create_dict()` where it now returns *entry name*

- 🚀 Fixed link in message on launch

### v1.0.1

- 🛠 Doc-strings + readme: Fixed invalid text and made readme more intuative

### v1.0.0

- 🚀 Initial stable release

- 📦 Base components: App, Surface, basic UI rendering loop

- 🛠 Event handling and layered rendering support