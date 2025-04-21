"""
For reaccuring values, you may predefine them before 
setting up your app and its correlating components.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Union
import pygame

InputColor = Union[Tuple[int, int, int], pygame.Color]

@dataclass
class FontScheme:
    title: Optional[pygame.font.Font] = None
    large: Optional[pygame.font.Font] = None
    medium1: Optional[pygame.font.Font] = None
    medium2: Optional[pygame.font.Font] = None
    small1: Optional[pygame.font.Font] = None
    small2: Optional[pygame.font.Font] = None

@dataclass
class Theme:
    text_color: Optional[InputColor] = None
    background: Optional[InputColor] = None
    border_color: Optional[InputColor] = None

component = Union[FontScheme, Theme]

del InputColor, Tuple, Union, Optional, dataclass

print("- MyUI preseting")