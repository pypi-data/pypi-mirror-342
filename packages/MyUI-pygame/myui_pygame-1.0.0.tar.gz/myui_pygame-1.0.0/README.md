# MyUI  
*A lightweight and intuitive extension for Pygame, designed to simplify UI development.*

---

## 🚀 Features  

✅ **UI Components** – Ready-to-use buttons, sliders, and more.  
✅ **Plugin System** – Easily extend functionality using modular plugins.  
✅ **Event Stack** – Simplifies repeated or custom event handling.  
✅ **Layering System** – Clean separation of background, normal, and top-level UI layers.  
✅ **Built for Games and Tools** – Seamless integration into Pygame-based projects.

---

## 📦 Installation  

Install MyUI via PyPI:

```bash
pip install MyUI_pygame
```

## ⚡ Quick Start

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
main_group = MyUI.plugins.create_dict(MyUI.plugins.get_plugin_group(plugin_wrappers, "plugin"))
entry = main_group.get("plugin-entry")
print(entry.name)

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

## ℹ️ Additional Information

- **Plugin folder**: Make sure the `plugins` directory exists and contains valid plugin files.
- **Styling**: `MyUI.FontScheme` allows you to manage multiple fonts with ease. This also applies for coloring, `MyUI.Theme`.
- **Surface layering**: Use `add_background`, `add_normal`, and `add_top` to control UI rendering layers.
- **Reloading**: The app supports hot-reloading of plugins through custom callbacks.
- **Audio**: Compatible with Pygame's sound and music systems.

--

## 📜 License

This project is licensed under the MIT License.

## ⭐ Like This Project?

If you find this project useful, consider starring it on GitHub and contributing to its development. Your support helps keep it active and growing! 🚀