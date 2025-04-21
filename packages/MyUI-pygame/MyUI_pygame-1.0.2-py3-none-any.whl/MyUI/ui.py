"""
MyUI - The perfect tool for UI operations. Everything from text input to buttons and sliders!

Provides many utilities. Create a *App* reference to get started, and everything else should be 
straight forward!
"""

from typing import Literal, List, Tuple, Dict, Any, Union, Optional, Callable
from dataclasses import dataclass
from .plugins import PluginWrapper
import traceback
import pyperclip
import pygame
import re

# Input type hints
InputVector = Union[Tuple[int, int], pygame.math.Vector2]
InputColor = Union[Tuple[int, int, int], pygame.Color]

# Callback type hints
RenderCallback = Callable[[pygame.Surface], Any]
EventCallback = Callable[[pygame.event.Event, pygame.math.Vector2], Optional[bool]]

def adjust_color(color: pygame.Color, offset: int) -> pygame.Color:
    """Adjust a color's brightness while clamping values."""
    if hasattr(color, "a"):
        alpha = color.a
    else: alpha = 255
    return pygame.Color(*(min(255, max(0, c + offset)) for c in color[:3]), alpha)

pygame.init()
pygame.event.set_allowed([pygame.DROPFILE, pygame.DROPTEXT])

class Cursor:
    prev_key: Any = None
    prev_cursor: int = None

    @classmethod
    def set_cursor(cls, key: Any, cursor: int) -> None:
        if cls.prev_key == key and cls.prev_cursor == cursor:
            return
        pygame.mouse.set_cursor(cursor)
        cls.prev_key = key
        cls.prev_cursor = cursor

@dataclass
class CursorPos:
    """
    The cursors position.
    """

    row: int = 0
    col: int = 0

    @staticmethod
    def new(origin: Optional['CursorPos'] = None) -> 'CursorPos':
        """New cursor position. May have a origin."""
        return CursorPos(origin.row, origin.col) if origin else CursorPos(0, 0)

    def copy(self) -> 'CursorPos':
        """Copy the cursor position into a new."""
        return CursorPos.new(self)

    def __lt__(self, other: 'CursorPos') -> bool:
        return (self.row, self.col) < (other.row, other.col)

    def __gt__(self, other: 'CursorPos') -> bool:
        return (self.row, self.col) > (other.row, other.col)

    def __eq__(self, other: 'CursorPos') -> bool:
        return (self.row, self.col) == (other.row, other.col)

class Text:
    """
    The best tool available for any kind of text editing. May even be applicable upon un-editable text, 
    but be sure to review your most optimal option for a good user experience!
    """
    def __init__(self, font: pygame.font.Font, pos: InputVector, size: InputVector, text_color: InputColor, border_color: InputColor, flags: int = 0):
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA | flags)
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.size: pygame.math.Vector2 = pygame.math.Vector2(size)
        self.font: pygame.font.Font = font

        self.text: List[str] = [""]
        self.text_color: pygame.Color = pygame.Color(text_color)  # White color
        self.highlight_color: pygame.Color = pygame.Color(
            min(self.text_color.r + 50, 255),  # Ensure value doesn't exceed 255
            min(self.text_color.g + 50, 255),
            min(self.text_color.b + 50, 255),
            self.text_color.a  # Preserve the alpha channel
        )
        self.border_color: pygame.Color = pygame.Color(border_color)
        self.unactive_color: pygame.Color = pygame.Color(
            min(self.border_color.r - 50, 255),  # Ensure value doesn't exceed 255
            min(self.border_color.g - 50, 255),
            min(self.border_color.b - 50, 255),
            self.border_color.a  # Preserve the alpha channel
        )
        self.cursor_pos: Dict[str, CursorPos] = {k: CursorPos() for k in ["start", "end"]}
        self.scroll_active: bool = False
        self.editable: bool = True
        self.active: bool = False
        self.mouse_move: bool = False

        self.scroll: float = 0
        self.scroll_speed: int = 5

        self.text_offset: pygame.math.Vector2 = pygame.math.Vector2(5, 5)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, *size)
        pygame.key.set_text_input_rect(self.rect)
        
        self.cursor_visible: bool = True
        self.cursor_timer: float = 0
        self.cursor_timer_threshold: float = 500
        self.last_click_time: float = 0
        self.click_count: int = 0

        self.undo_stack: List[List[str]] = []  # History of text states
        self.redo_stack: List[List[str]] = []  # Redoable actions
    
    def toggle_scroll(self, enabled: bool = None) -> None:
        """Toggle scroll. Use `enabled` to set the new value, if left as *None*, it will be the reversed value of the current."""
        if enabled is None: enabled = not self.scroll_active
        self.scroll_active = enabled
        if not enabled:
            self.scroll = 0  # Reset scroll offset
    
    def toggle_editable(self, enabled: bool = None) -> None:
        """Toggle editablity. Use `enabled` to set the new value, if left as *None*, it will be the reversed value of the current."""
        if enabled is None: enabled = not self.editable
        self.editable = enabled
        if not enabled: 
            self.active = False
            self.scroll = 0
    
    def update_rect(self) -> None:
        """Update the rect upon a change in any metrical values."""
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        pygame.key.set_text_input_rect(self.rect)
    
    def save_state(self) -> None:
        """Save state to undo stacks before handling a operation that may differ the text."""
        # Save the current state to the undo stack
        self.undo_stack.append(self.text[:])  # Make a copy of the current text
        # Clear redo stack when a new action is performed
        self.redo_stack.clear()

    def undo(self) -> None:
        """Undo the last change."""
        if self.undo_stack:
            # Save the current state for redo
            self.redo_stack.append(self.text[:])
            # Revert to the previous state
            self.text = self.undo_stack.pop()
            # Adjust cursor position
            self.set_cursor(CursorPos(len(self.text) - 1, len(self.text[-1])))

    def redo(self) -> None:
        """Redo what has last been undun."""
        if self.redo_stack:
            # Save the current state for undo
            self.undo_stack.append(self.text[:])
            # Restore the most recent redo state
            self.text = self.redo_stack.pop()
            # Adjust cursor position
            self.set_cursor(CursorPos(len(self.text) - 1, len(self.text[-1])))

    def _calculate_char_size(self, text: str) -> List[int]:
        return [self.font.size(c)[0] for c in text]

    def _clamp_cursor(self, cursor: CursorPos) -> CursorPos:
        row = max(0, min(cursor.row, len(self.text) - 1))
        col = max(0, min(cursor.col, len(self.text[row])))
        return CursorPos(row, col)

    def set_cursor(self, pos: CursorPos) -> None:
        """Set both cursor positions to a specified."""
        clamped = self._clamp_cursor(pos)
        self.cursor_pos["start"] = clamped
        self.cursor_pos["end"] = clamped.copy()

    def get_cursor_pos(self, screen_pos: InputVector) -> CursorPos:
        """Get cursor position form screen position."""
        text_pos = pygame.math.Vector2(screen_pos) - self.pos
        y_offset = self.text_offset.y - self.scroll if self.scroll_active else self.text_offset.y
        line_size = self.font.get_linesize()

        for row, line in enumerate(self.text):
            if text_pos.y < y_offset + (row + 1) * line_size:
                widths = self._calculate_char_size(line)
                x_acc = 0
                for i, w in enumerate(widths):
                    if x_acc + w / 2 >= text_pos.x:
                        return CursorPos(row, i)
                    x_acc += w
                return CursorPos(row, len(line))

        return CursorPos(len(self.text) - 1, len(self.text[-1]))
    
    def fix_cursor(self) -> None:
        """Fix the cursor position in case of it being out of bounds."""
        # Ensure the cursor positions are within valid bounds
        start, end = sorted([self.cursor_pos["start"], self.cursor_pos["end"]])

        # Clamp rows to valid range
        start.row = max(0, min(start.row, len(self.text) - 1))
        end.row = max(0, min(end.row, len(self.text) - 1))

        # Clamp columns to valid range for each row
        start.col = max(0, min(start.col, len(self.text[start.row])))
        end.col = max(0, min(end.col, len(self.text[end.row])))

        # Update the cursor positions
        self.cursor_pos["start"] = start
        self.cursor_pos["end"] = end

    def remove_selection(self) -> CursorPos:
        """Remove the text between the two current cursor positions (thus, selection)."""
        start, end = sorted([self.cursor_pos["start"], self.cursor_pos["end"]])
        if start != end:
            if start.row == end.row:
                line = self.text[start.row]
                self.text[start.row] = line[:start.col] + line[end.col:]
            else:
                self.text[start.row] = self.text[start.row][:start.col] + self.text[end.row][end.col:]
                del self.text[start.row + 1:end.row + 1]
        self.fix_cursor()
        return start
    
    def _max_lines(self) -> int:
        line_size = self.font.get_linesize()
        return (self.surface.get_height() - 10) // line_size  # 5px padding on each side

    def append_text(self, text: str) -> None:
        """Append text to where the cursor is located."""
        self.save_state()
        start = self.remove_selection()
        row, col = start.row, start.col
        current_line = self.text[row]
        new_line = current_line[:col] + text + current_line[col:]

        # Wrap and handle line overflow
        wrapped_line, overflow = self.wrap_line(new_line)
        self.text[row] = wrapped_line

        # Prevent adding more lines beyond the height limit, but only if scrolling is inactive
        if overflow and (not self.scroll_active and len(self.text) >= self._max_lines()):
            self.set_cursor(CursorPos(row, len(self.text[row])))
            return  # Prevent exceeding the line limit
        elif overflow:
            self.text.insert(row + 1, overflow)
            self.set_cursor(CursorPos(row + 1, len(overflow)))
        else:
            self.set_cursor(CursorPos(row, len(self.text[row])))

    def wrap_line(self, line: str) -> Tuple[str, str]:
        """Wrap line so that it fits."""
        max_width = self.surface.get_width() - 10  # 5px padding on each side
        words = re.findall(r'\S+|\s+', line)
        wrapped_line = ''
        for word in words:
            test_line = wrapped_line + word
            if sum(self._calculate_char_size(test_line)) > max_width:
                return wrapped_line, line[len(wrapped_line):]
            wrapped_line = test_line
        self.fix_cursor()
        return wrapped_line, ''

    def remove_text(self, ctrl: bool = False) -> None:
        """Remove text from where the cursor is positioned. In case `ctrl` is *True*, remove whole words."""
        self.save_state()
        start = self.remove_selection()
        row, col = start.row, start.col

        if ctrl and col > 0:
            line = self.text[row][:col]
            matches = list(re.finditer(r"\w+|\W", line))
            if matches:
                last = matches[-1]
                for m in reversed(matches):
                    if m.end() == col:
                        last = m
                        break
                self.text[row] = line[:last.start()] + self.text[row][col:]
                self.set_cursor(CursorPos(row, last.start()))
                self.fix_cursor()
                return

        if col > 0:
            self.text[row] = self.text[row][:col-1] + self.text[row][col:]
            self.set_cursor(CursorPos(row, col-1))
        elif row > 0:
            prev_line = self.text[row - 1]
            self.set_cursor(CursorPos(row - 1, len(prev_line)))
            self.text[row - 1] += self.text[row]
            del self.text[row]
        self.fix_cursor()

    def cursor_left(self) -> None:
        """Move the cursor left."""
        row, col = self.cursor_pos["start"].row, self.cursor_pos["start"].col
        if col > 0:
            self.set_cursor(CursorPos(row, col - 1))
        elif row > 0:
            self.set_cursor(CursorPos(row - 1, len(self.text[row - 1])))

    def cursor_right(self) -> None:
        """Move the cursor right."""
        row, col = self.cursor_pos["start"].row, self.cursor_pos["start"].col
        if col < len(self.text[row]):
            self.set_cursor(CursorPos(row, col + 1))
        elif row + 1 < len(self.text):
            self.set_cursor(CursorPos(row + 1, 0))

    def cursor_up(self) -> None:
        """Move the cursor up."""
        row, col = self.cursor_pos["start"].row, self.cursor_pos["start"].col
        if row > 0:
            self.set_cursor(CursorPos(row - 1, min(col, len(self.text[row - 1]))))

    def cursor_down(self) -> None:
        """Move the cursor down."""
        row, col = self.cursor_pos["start"].row, self.cursor_pos["start"].col
        if row + 1 < len(self.text):
            self.set_cursor(CursorPos(row + 1, min(col, len(self.text[row + 1]))))

    def insert_newline(self) -> None:
        """Insert a new line."""
        self.save_state()
        start = self.remove_selection()
        row, col = start.row, start.col
        line = self.text[row]

        # Check if scrolling is disabled and enforce the maximum line limit
        if not self.scroll_active and len(self.text) >= self._max_lines():
            return  # Prevent adding a new line if it exceeds the height limit

        # Split the current line and insert a new one
        self.text[row] = line[:col]
        self.text.insert(row + 1, line[col:])
        self.set_cursor(CursorPos(row + 1, 0))
    
    def copy_text(self) -> str:
        """Copy the text between the two current cursor positions (thus, selection)."""
        start, end = sorted([self.cursor_pos["start"], self.cursor_pos["end"]])
        if start != end:  # Ensure there's a selection
            if start.row == end.row:
                return self.text[start.row][start.col:end.col]
            else:
                copied_text = self.text[start.row][start.col:] + "\n"
                for row in range(start.row + 1, end.row):
                    copied_text += self.text[row] + "\n"
                copied_text += self.text[end.row][:end.col]
                return copied_text
        return ""
    
    def fix_scroll(self) -> None:
        max_scroll = max(0, self.text_offset.y + len(self.text) * self.font.get_linesize() - self.surface.get_height())
        self.scroll = min(self.scroll, max_scroll)
    
    def scroll_down(self) -> None:
        self.scroll = max(0, self.text_offset.y + len(self.text) * self.font.get_linesize() - self.surface.get_height())
    
    def insert_text(self, text: str) -> None:
        """Insert text at where the cursor is positioned."""
        self.save_state()
        # Remove selection if there's any
        start = self.remove_selection()
        row, col = start.row, start.col

        # Split clipboard text into lines
        lines = text.splitlines()
        current_line = self.text[row]

        # Combine the first line with the current line
        self.text[row] = current_line[:col] + lines[0] + current_line[col:]
        
        # Handle any additional lines from the clipboard
        for i, line in enumerate(lines[1:], start=1):
            self.text.insert(row + i, line)

        # Set the cursor to the end of the pasted text
        self.set_cursor(CursorPos(row + len(lines) - 1, len(lines[-1])))
        self.fix_cursor()

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle a event. If a position is applicable, it will be offseted by the specified vector."""

        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))

        # Events always applicable
        if event.type == pygame.MOUSEBUTTONDOWN:
            now = pygame.time.get_ticks()
            if now - self.last_click_time < 400:
                self.click_count += 1
            else:
                self.click_count = 1
            self.last_click_time = now

            if self.rect.collidepoint(pos):
                self.active = True
                pygame.key.start_text_input()
                pos = self.get_cursor_pos(pos)
                self.set_cursor(pos)
                if self.click_count == 2:
                    line = self.text[pos.row]
                    for m in re.finditer(r"\w+|\W", line):
                        if m.start() <= pos.col < m.end():
                            self.cursor_pos["start"] = CursorPos(pos.row, m.start())
                            self.cursor_pos["end"] = CursorPos(pos.row, m.end())
                            break
                else:
                    self.mouse_move = True
                return True
            else:
                self.active = False
                pygame.key.stop_text_input()
        
        elif event.type == pygame.MOUSEWHEEL and self.active and self.scroll_active:
            # Update scroll position based on the wheel movement
            self.scroll = max(0, self.scroll + event.y * -self.scroll_speed)
            # Optional: Clamp the scroll value to prevent scrolling beyond content height
            self.fix_scroll()
            return True

        elif event.type == pygame.MOUSEMOTION and self.active and self.mouse_move:
            self.cursor_pos["end"] = self.get_cursor_pos(pos)
            return True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_move = False
        
        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL:
                if event.key == pygame.K_c:
                    pyperclip.copy(self.copy_text())
                    return True
                elif event.key == pygame.K_a:
                    self.cursor_pos["start"] = CursorPos(0, 0)
                    self.cursor_pos["end"] = CursorPos(len(self.text) - 1, len(self.text[-1]))
                    return True
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    prev_pos = self.cursor_pos["end"].copy()
                    if event.key == pygame.K_LEFT:
                        self.cursor_left()
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_right()
                    elif event.key == pygame.K_UP:
                        self.cursor_up()
                    elif event.key == pygame.K_DOWN:
                        self.cursor_down()
                    self.cursor_pos["end"] = prev_pos
                    return True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(pos):
                Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_IBEAM)
                return True

        if not self.editable:
            return False
        
        # Events only applicable on edit
        if event.type == pygame.DROPFILE:
            file_path = event.file  # This is a string
            # Optionally read the file contents and insert it
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
                # Insert file_content into your text editor's buffer
                self.insert_text(file_content)
            return True

        elif event.type == pygame.DROPTEXT:
            dropped_text = event.text
            # Insert dropped_text into your text editor's buffer
            self.insert_text(dropped_text)
            return True

        elif event.type == pygame.TEXTINPUT and self.active:
            self.append_text(event.text)
            return True

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.remove_text(ctrl=mods & pygame.KMOD_CTRL)
                return True
            elif mods & pygame.KMOD_CTRL:
                if mods & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_s:
                        self.toggle_scroll(not self.scroll_active)
                        return True
                    elif event.key == pygame.K_z:
                        self.redo()
                        return True
                else:
                    if event.key == pygame.K_v:
                        clipboard_text = pyperclip.paste()
                        if not clipboard_text:
                            return True  # Skip if clipboard is empty
                        self.insert_text(clipboard_text)
                        return True
                    elif event.key == pygame.K_x:
                        pyperclip.copy(self.copy_text())
                        self.remove_selection()
                        return True
                    elif event.key == pygame.K_z:
                        self.undo()
                        return True
            elif event.key == pygame.K_LEFT:
                self.cursor_left()
                return True
            elif event.key == pygame.K_RIGHT:
                self.cursor_right()
                return True
            elif event.key == pygame.K_UP:
                self.cursor_up()
                return True
            elif event.key == pygame.K_DOWN:
                self.cursor_down()
                return True
            elif event.key == pygame.K_RETURN:
                self.insert_newline()
                return True
            elif event.key == pygame.K_TAB:
                self.append_text("    ")
                return True
    
    def draw_cursor(self) -> None:
        """Draws selection highlights and blinking cursor with transparency."""
        line_size = self.font.get_linesize()
        cursor_color = (150, 150, 150, 200)
        selection_color = (50, 100, 255, 100) if self.active else (100, 50, 122, 75)
        y_offset = self.text_offset.y - self.scroll if self.scroll_active else self.text_offset.y

        # Create a surface with alpha support for selection highlights
        highlight_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)

        start, end = self.cursor_pos["start"], self.cursor_pos["end"]
        if (start.row, start.col) > (end.row, end.col):
            start, end = end, start

        for row in range(start.row, end.row + 1):
            if row >= len(self.text): continue
            row_text = self.text[row]
            char_widths = self._calculate_char_size(row_text)

            row_start_col = start.col if row == start.row else 0
            row_end_col = end.col if row == end.row else len(row_text)

            start_x = self.text_offset.x + sum(char_widths[:row_start_col])
            end_x = self.text_offset.x + sum(char_widths[:row_end_col])

            y = y_offset + row * line_size
            width = max(2, end_x - start_x)

            pygame.draw.rect(
                highlight_surface, selection_color,
                (start_x, y, width, line_size), border_radius=3
            )

        if start == end:
            if self.cursor_visible and self.active:
                # Blinking cursor (only when no selection)
                char_widths = self._calculate_char_size(self.text[start.row]) if start.row < len(self.text) else []
                x = self.text_offset.x + sum(char_widths[:start.col]) if start.col <= len(char_widths) else 5
                y = y_offset + start.row * line_size
                pygame.draw.rect(self.surface, cursor_color, (x, y, 2, line_size), border_radius=2)
        else: 
            # Blit the highlight before drawing the text
            self.surface.blit(highlight_surface, (0, 0))
    
    def render_text_lines(self) -> None:
        """Render the text."""
        # Calculate the text offset and line height
        line_height = self.font.get_linesize()
        y_offset = self.text_offset.y - self.scroll if self.scroll_active else self.text_offset.y

        # Pre-calculate selection bounds
        start, end = sorted([self.cursor_pos["start"], self.cursor_pos["end"]])

        for index, line in enumerate(self.text):
            # Skip lines that are outside the visible area when scrolling is active
            if self.scroll_active and (y_offset + line_height < 0 or y_offset > self.surface.get_height()):
                y_offset += line_height
                continue

            # Determine the appropriate color based on selection
            color = self.highlight_color if start.row <= index <= end.row or not self.editable else self.text_color

            # Render the text line
            text_surface = self.font.render(line, True, color)
            self.surface.blit(text_surface, (self.text_offset.x, y_offset))
            y_offset += line_height

    def render(self, surface: pygame.Surface, dt: float) -> None:
        """Render text, cursor, highlighting, and the border upon a specified surface."""
        self.surface.fill((0, 0, 0, 0))  # Clear surface

        self.render_text_lines()

        # Cursor blinking logic
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_timer_threshold:  # Toggle cursor every 500ms
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

        self.draw_cursor()  # Draw cursor and selection only if active
        surface.blit(self.surface, self.pos)
        border_color = self.border_color if self.active else self.unactive_color
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=6)

class Button: 
    """A pressable button"""
    pass

class PushButton(Button):
    """Push the button to call it."""
    def __init__(self, text: str, font: pygame.font.Font, pos: InputVector, size: InputVector, color: InputColor, hover_color: InputColor, callback: Callable[[], Any]):
        self.text: str = text
        self.font: pygame.font.Font = font
        self.original_pos: pygame.math.Vector2 = pygame.math.Vector2(pos)  # Store original position
        self.original_size: pygame.math.Vector2 = pygame.math.Vector2(size)  # Store original size
        self.color: pygame.Color = pygame.Color(color)
        self.hover_color: pygame.Color = pygame.Color(hover_color)
        self.callback: Callable[[], Any] = callback

        # Current size and position start at original values
        self.size: pygame.math.Vector2 = self.original_size.copy()
        self.pos: pygame.math.Vector2 = self.original_pos.copy()

        # Initialize rect in the constructor
        self.rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        
        self.tooltip: Optional[Tooltip] = None

        # State tracking
        self.is_hovered: bool = False
        self.is_clicked: bool = False
    
    def __call__(self) -> None:
        self.callback()

    def render(self, surface: pygame.Surface) -> None:
        """Render the button onto the surface specified."""
        # Adjust size based on hover and click state
        if self.is_clicked:
            self.size = self.original_size * 0.9  # Shrink further on click
        elif self.is_hovered:
            self.size = self.original_size * 0.95  # Shrink on hover
        else:
            self.size = self.original_size.copy()  # Reset to original size

        # Recalculate position to keep the button centered
        self.pos.x = self.original_pos.x + (self.original_size.x - self.size.x) / 2
        self.pos.y = self.original_pos.y + (self.original_size.y - self.size.y) / 2

        # Update the rect's size and position
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        # Draw the button
        button_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, button_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, adjust_color(button_color, 20), self.rect, 2, 8)

        # Render button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        if self.tooltip: self.tooltip.render(surface)

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle a event. If a position is applicable, it will be offseted by the specified vector."""
        # Check for mouse interaction
        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))

        if self.tooltip:
            if self.is_hovered:
                self.tooltip.visible = True
                self.tooltip.update_position((self.rect.x + self.rect.width + 10, self.rect.y))
            else:
                self.tooltip.visible = False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(pos)
            if self.is_hovered: 
                Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_HAND)
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.is_clicked = True
            return True
        elif event.type == pygame.MOUSEBUTTONUP and self.is_clicked:
            self.is_clicked = False
            self.callback()
            return True

class ToggleButton(Button):
    """
    Instead of a push-button, a toggle-button might be it!
    """
    def __init__(self, text: str, font: pygame.font.Font, pos: InputVector, size: InputVector, color: InputColor, hover_color: InputColor, active_color: InputColor, callback: Callable[[], Any] = None):
        self.text: str = text
        self.font: pygame.font.Font = font
        self.original_pos: pygame.math.Vector2 = pygame.math.Vector2(pos)  # Store original position
        self.original_size: pygame.math.Vector2 = pygame.math.Vector2(size)  # Store original size
        self.color: pygame.Color = pygame.Color(color)
        self.hover_color: pygame.Color = pygame.Color(hover_color)
        self.active_color: pygame.Color = pygame.Color(active_color)  # Color when toggled "on"
        self.callback: Callable[[], Any] = callback

        # Current size and position start at original values
        self.size: pygame.math.Vector2 = self.original_size.copy()
        self.pos: pygame.math.Vector2 = self.original_pos.copy()

        # Create the button rectangle
        self.rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        self.tooltip: Optional[Tooltip] = None

        # State tracking
        self.is_hovered: bool = False
        self.is_clicked: bool = False
        self.is_toggled: bool = False  # Tracks whether the button is toggled
    
    def __call__(self) -> None:
        self.is_toggled = not self.is_toggled
        self.callback()

    def render(self, surface: pygame.Surface) -> None:
        """Render the button onto the surface specified."""
        # Adjust size based on hover and click state
        if self.is_clicked:
            self.size = self.original_size * 0.9  # Shrink further on click
        elif self.is_hovered:
            self.size = self.original_size * 0.95  # Shrink on hover
        else:
            self.size = self.original_size.copy()  # Reset to original size

        # Recalculate position to keep the button centered
        self.pos.x = self.original_pos.x + (self.original_size.x - self.size.x) / 2
        self.pos.y = self.original_pos.y + (self.original_size.y - self.size.y) / 2

        # Create the button rectangle with updated size and position
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        # Determine button color based on toggle state
        button_color = self.active_color if self.is_toggled else (self.hover_color if self.is_hovered else self.color)
        pygame.draw.rect(surface, button_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, adjust_color(button_color, 20), self.rect, 2, 8)

        # Render button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        if self.tooltip: self.tooltip.render(surface)

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle a event. If a position is applicable, it will be offseted by the specified vector."""
        # Check for mouse interaction
        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))

        if self.tooltip:
            if self.is_hovered:
                self.tooltip.visible = True
                self.tooltip.update_position((self.rect.x + self.rect.width + 10, self.rect.y))
            else:
                self.tooltip.visible = False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(pos)
            if self.is_hovered: 
                Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_HAND)
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.is_clicked = True
            return True
        elif event.type == pygame.MOUSEBUTTONUP and self.is_clicked:
            self.is_clicked = False
            self.is_toggled = not self.is_toggled  # Toggle state on release
            if self.callback:
                self.callback()
            return True

class Slider:
    """
    A normal slider. Don't forget to update it's value onto screen somewhere!
    """
    def __init__(self, pos: InputVector, size: InputVector, min_val: int, max_val: int, start_val: int, color: InputColor, knob_color: InputColor, callback: Callable[[int], Any] = None):
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.size: pygame.math.Vector2 = pygame.math.Vector2(size)
        self.min_val: int = min_val
        self.max_val: int = max_val
        self.value: int = start_val
        self.color: pygame.Color = pygame.Color(color)
        self.knob_color: pygame.Color = pygame.Color(knob_color)
        self.callback: Callable[[str], Any] = callback  # Function to execute when the value changes

        # Create the track and knob rectangles
        self.track_rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y + self.size.y // 2 - 5, self.size.x, 10)
        self.knob_rect: pygame.Rect = pygame.Rect(0, 0, self.size.y, self.size.y)
        self.update_knob_position()

        # State tracking
        self.dragging: bool = False

    def update_knob_position(self) -> None:
        """Update the position of the knob based on internal factors."""
        # Update the knob position based on the current value
        normalized_val = (self.value - self.min_val) / (self.max_val - self.min_val)  # Normalize value between 0 and 1
        knob_x = self.track_rect.x + normalized_val * self.track_rect.width - self.knob_rect.width // 2
        self.knob_rect.x = int(knob_x)
        self.knob_rect.y = self.track_rect.y - self.knob_rect.height // 2 + self.track_rect.height // 2

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle a event. If a position is applicable, it will be offseted by the specified vector."""
        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(pos):
                Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_HAND)
                self.dragging = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Move the knob with the mouse and update the value
            mouse_x = max(self.track_rect.left, min(pos[0], self.track_rect.right))
            normalized_val = (mouse_x - self.track_rect.left) / self.track_rect.width
            self.value = int(self.min_val + normalized_val * (self.max_val - self.min_val))
            self.update_knob_position()
            if self.callback:
                self.callback(self.value)
            return True

    def render(self, surface: pygame.Surface) -> None:
        """Render the slider onto the surface specified."""
        # Draw the slider track
        pygame.draw.rect(surface, self.color, self.track_rect, border_radius=5)
        pygame.draw.rect(surface, adjust_color(self.color, 20), self.track_rect, 2, 5)

        # Draw the knob
        pygame.draw.ellipse(surface, self.knob_color, self.knob_rect)
        pygame.draw.ellipse(surface, adjust_color(self.knob_color, 20), self.knob_rect, 2)

class DropdownMenu:
    """
    Let's you simply chose one of the applicable options. Who doesn't want that?
    """
    def __init__(self, options: List[str], font: pygame.font.Font, pos: InputVector, size: InputVector, color: InputColor, hover_color: InputColor, active_color: InputColor, callback: Callable[[str], Any] = None):
        self.options: List[str] = options  # List of options for the dropdown
        self.font: pygame.font.Font = font
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.size: pygame.math.Vector2 = pygame.math.Vector2(size)
        self.color: pygame.Color = pygame.Color(color)
        self.hover_color: pygame.Color = pygame.Color(hover_color)
        self.active_color: pygame.Color = pygame.Color(active_color)
        self.callback: Callable[[str], Any] = callback  # Function called when an option is selected

        # Track which option is currently selected and whether the menu is expanded
        self.selected_option: Optional[str] = options[0] if options else None
        self.expanded: bool = False

        # Rectangles for rendering
        self.base_rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.option_rects: List[pygame.Rect] = []

        for i, _ in enumerate(self.options):
            y_offset = self.pos.y + self.size.y * (i + 1)
            self.option_rects.append(pygame.Rect(self.pos.x, y_offset, self.size.x, self.size.y))

        # State tracking
        self.hover_index: int = -1

    def render(self, surface: pygame.Surface) -> None:
        """Render the dropdownmenu onto the surface specified."""
        # Render the base dropdown button
        button_color = self.active_color if self.expanded else self.color
        pygame.draw.rect(surface, button_color, self.base_rect, border_radius=5)
        pygame.draw.rect(surface, adjust_color(button_color, 20), self.base_rect, 2, 5)

        # Render selected text
        if self.selected_option:
            text_surface = self.font.render(self.selected_option, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.base_rect.center)
            surface.blit(text_surface, text_rect)

        # Render the dropdown options if expanded
        if self.expanded:
            for i, option in enumerate(self.options):
                rect = self.option_rects[i]
                bg_color = self.hover_color if i == self.hover_index else self.color
                pygame.draw.rect(surface, bg_color, rect, border_radius=5)
                pygame.draw.rect(surface, adjust_color(bg_color, -20), rect, 2, 5)

                # Render option text
                text_surface = self.font.render(option, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle a event. If a position is applicable, it will be offseted by the specified vector."""
        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.base_rect.collidepoint(pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        self.selected_option = self.options[i]
                        self.expanded = False
                        if self.callback:
                            self.callback(self.selected_option)
                        return True
                else:
                    self.expanded = False

        elif event.type == pygame.MOUSEMOTION:
            if self.expanded:
                self.hover_index = -1
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        self.hover_index = i
                        break
                return True

class Tooltip:
    """
    Must be rendered. A must-have for simple UI elements with additional side notes.
    """
    def __init__(self, text: str, font: pygame.font.Font, color: InputColor, bg_color: InputColor, padding: int = 5):
        self.text: str = text
        self.font: pygame.font.Font = font
        self.color: pygame.Color = pygame.Color(color)
        self.bg_color: pygame.Color = pygame.Color(bg_color)
        self.padding: int = padding
        self.visible: bool = False
        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    def update_position(self, pos: InputVector) -> None:
        """Update the position of the tooltip so that it is acuratly placed upon display."""
        # Update tooltip position near the mouse or element
        text_surface = self.font.render(self.text, True, self.color)
        self.rect = pygame.Rect(pos[0], pos[1], text_surface.get_width() + self.padding * 2, text_surface.get_height() + self.padding * 2)

    def render(self, surface: pygame.Surface) -> None:
        """Render the tooltip onto the surface specified"""
        if self.visible:
            # Draw the tooltip background
            pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=5)
            pygame.draw.rect(surface, adjust_color(self.bg_color, 20), self.rect, 2, 5)
            # Draw the tooltip text
            text_surface = self.font.render(self.text, True, self.color)
            surface.blit(text_surface, (self.rect.x + self.padding, self.rect.y + self.padding))

class Dropbox:
    """
    Simply drag and drop a file into its field and the callback will be rung upon the event.
    """
    def __init__(self, label: str, pos: InputVector, size: InputVector, font: pygame.font.Font, color: InputColor, hover_color: InputColor, callback: Callable[[str], Any]):
        self.rect: pygame.Rect = pygame.Rect(*pos, *size)
        self.font: pygame.font.Font = font
        self.label: pygame.Surface = font.render(label, True, (50, 50, 50))
        self.color: pygame.Color = pygame.Color(color)
        self.hover_color: pygame.Color = pygame.Color(hover_color)

        self.border_width: int = 1
        self.border_radius: int = 7

        self.hover: bool = False

        self.callback: Callable[[str], Any] = callback
    
    def set_label(self, text: str, color: InputColor = (50, 50, 50)) -> None:
        self.label = self.font.render(text, True, color)
    
    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(pos)
            if self.hover: 
                Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_HAND)
                return True
        elif event.type == pygame.DROPFILE and self.hover:
            self.callback(event.file)
            return True
    
    def render(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, self.border_width, self.border_radius)
        surface.blit(self.label, self.label.get_rect(center = self.rect.center))

class Window:
    """
    A basic window to keep things separated. Useful for multiple smaller systems in one MyUI application.
    """
    def __init__(
        self,
        size: InputVector,
        font: pygame.font.Font,
        top_color: InputColor = (150, 175, 200),
        background_color: InputColor = (230, 230, 230),
        border_color: InputColor = (130, 130, 130),
        border_radius: int = 4,
        border_width: int = 1,
        surface_offset: InputVector = (0, 25),
        app: Optional['App'] = None,
        pos: InputVector = (0, 0),
        ):
        # Initialize Position and Size
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.size: pygame.math.Vector2 = pygame.math.Vector2(size)

        # Initialize Surface
        self.surface_offset: pygame.math.Vector2 = pygame.math.Vector2(surface_offset)
        self.surface: pygame.Surface = pygame.Surface(self.size - self.surface_offset, pygame.SRCALPHA)

        # Colors and Styles
        self.top_color: pygame.Color = pygame.Color(top_color)
        self.background_color: pygame.Color = pygame.Color(background_color)
        self.border_color: pygame.Color = pygame.Color(border_color)
        self.border_radius: int = border_radius
        self.border_width: int = border_width

        # Font and Title
        self.font: pygame.font.Font = font
        self.title: pygame.Surface = font.render("MyUI Window", True, (255, 255, 255))

        # State Variables
        self.active: bool = False
        self.dragging: bool = False
        self.shown: bool = True

        self.app: App = None
        self.index: int = -1
        if app:
            self.app = app
            self.index = app.add_handler(self.render, self.handle_event)

        # Event Handlers and Renderers
        self.event_handlers: List[EventCallback] = []
        self.on_render: List[RenderCallback] = []

        self.resize()
    
    def toggle_shown(self, enabled: bool = None) -> None:
        """
        Toggle if the window should be drawn or not. 
        If not `enabled` is provided, it defaults to the opposite of the current value.
        """
        if enabled is None: enabled = not self.shown
        self.shown = enabled
    
    def set_title(self, title: str, color: InputColor = (255, 255, 255)) -> None:
        """Set the current title and the color it will be displayed in."""
        self.title = self.font.render(title, True, color)

    def resize(self, size_change: InputVector = (0, 0)) -> None:
        """Resize the window."""
        self.size += pygame.math.Vector2(size_change)
        self.surface = pygame.Surface(self.size - self.surface_offset, pygame.SRCALPHA)
        self.top_size = pygame.math.Vector2(self.size.x - 1, 25)

    def move(self, pos_change: InputVector = (0, 0)) -> None:
        """Move the window."""
        self.pos += pygame.math.Vector2(pos_change)

    def get_rect(self) -> pygame.Rect:
        """Get the window's main rectangle."""
        return pygame.Rect(*self.pos, *self.size)

    def get_top_rect(self) -> pygame.Rect:
        """Get the rectangle for the top bar."""
        return pygame.Rect(*self.pos, *self.top_size)
    
    def add_handler(self, on_render: RenderCallback = None, on_event: EventCallback = None) -> None:
        """Add an object with event and render handlers."""
        if on_render: self.on_render.append(on_render)
        if on_event: self.event_handlers.append(on_event)

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle events for the window."""
        if not self.shown: return

        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))

        top_rect = self.get_top_rect()
        return_value = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.get_rect().collidepoint(pos)
            if self.active:
                if self.app:
                    self.app.bring_to_front(self.index)
                if top_rect.collidepoint(pos):
                    self.dragging = True
                return_value = True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.move(event.rel)
            if self.get_rect().collidepoint(pos):
                Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_ARROW)
                return_value = True
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            return_value = True

        if self.active or event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            for handle in self.event_handlers:
                if handle(event, -(self.pos + self.surface_offset + pygame.math.Vector2(offset))):
                    return True
        return return_value

    def render(self, surface: pygame.Surface) -> None:
        """Render the window and its contents."""

        if not self.shown: return

        # Main Window Rectangle
        window_rect = self.get_rect()
        top_rect = self.get_top_rect()
        border_radius = self.border_radius - 1 if self.dragging else self.border_radius

        # Adjust Top Color Based on Activity
        top_color = adjust_color(self.top_color, -10 if self.dragging else -20 if not self.active else 0)
        border_color = adjust_color(self.border_color, -10 if self.dragging else -20 if not self.active else 0)

        # Draw Window Background
        pygame.draw.rect(surface, self.background_color, window_rect, 0, border_radius)

        # Render Child Objects
        for render in self.on_render:
            render(self.surface)
        surface.blit(self.surface, self.pos + self.surface_offset)
        self.surface.fill((0, 0, 0, 0))  # Clear surface after rendering

        # Draw Top Bar
        pygame.draw.rect(surface, top_color, top_rect, 0, border_radius)
        pygame.draw.rect(surface, border_color, top_rect, 1, border_radius)
        surface.blit(self.title, self.pos + (5, 5))

        # Draw Window Border
        pygame.draw.rect(surface, border_color, window_rect, self.border_width, border_radius)

class Surface:
    """Easily seperate components by different surfaces and menues. Who doesn't want that?"""
    def __init__(self, pos: InputVector, size: InputVector, background_color: InputColor, border_color: InputColor, border_width: int, border_radius: int):
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.size: pygame.math.Vector2 = pygame.math.Vector2(size)

        self.rect: pygame.Rect = pygame.Rect(0, 0, *size)
        self.bakground_color: pygame.Color = pygame.Color(background_color)
        self.border_color: pygame.Color = pygame.Color(border_color)
        self.border_width: int = border_width
        self.border_radius: int = border_radius

        self.event_handlers: List[EventCallback] = []
        self.on_render: List[RenderCallback] = []
    
    def add_handler(self, on_render: RenderCallback = None, on_event: EventCallback = None) -> None:
        """Add an object with event and render handlers."""
        if on_render: self.on_render.append(on_render)
        if on_event: self.event_handlers.append(on_event)
    
    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle events for the surface."""
        for handle in self.event_handlers:
            if handle(event, -(self.pos + pygame.Vector2(offset))):
                return True
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the surface and its contents."""
        self.surface.fill((255, 255, 255, 0))
        pygame.draw.rect(self.surface, self.bakground_color, self.rect, border_radius = self.border_radius)
        if self.border_width >= 1: 
            pygame.draw.rect(self.surface, self.border_color, self.rect, self.border_width, self.border_radius)
        for render in self.on_render: render(self.surface)
        surface.blit(self.surface, self.surface.get_rect(topleft=self.pos))

class HotbarItem:
    """
    A hotbar item. It can be pressed and the corresponding callback will be rung.
    The hotbar item will be given as a argument in case of attribute changes, e.g the *selected* attribute.
    """
    def __init__(self, label: str, font: pygame.font.Font, callback: Callable[['HotbarItem'], Any]):
        self.label: str = label
        self.callback: Callable[[HotbarItem], Any] = callback
        self.font: pygame.font.Font = font
        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.hovered: bool = False
        self.selected: bool = False

        self.tooltip: Optional[Tooltip] = None

    def render(self, surface: pygame.Surface, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        """Render the hotbar item as to how/where specified."""
        self.rect = pygame.Rect(*pos, *size)
        color = (100, 100, 150) if self.selected else (80, 80, 100)
        hover_color = (120, 120, 180)

        bg_color = hover_color if self.hovered else color
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=7)
        pygame.draw.rect(surface, adjust_color(bg_color, 20), self.rect, 2, 7)

        text_surface = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        if self.tooltip: self.tooltip.render(surface)

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """Handle a event with a given offset to position if applicable."""
        if hasattr(event, "pos"):
            pos = tuple(event.pos[i] + offset[i] for i in range(2))
            self.hovered = self.rect.collidepoint(pos)

        if self.tooltip:
            if self.hovered:
                self.tooltip.visible = True
                self.tooltip.update_position((self.rect.x + self.rect.width + 10, self.rect.y))
            else:
                self.tooltip.visible = False

        if event.type == pygame.MOUSEBUTTONUP and self.hovered:
            self.callback(self)
            return True
        
        if self.hovered:
            Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_HAND)
            return True

class Hotbar:
    """
    The hotbar enables the developer to easily create button menues with their own 
    specific functionalities, e.g to open or close a *Window*.
    """
    def __init__(self, font: pygame.font.Font, pos: InputVector = (0, 0), item_size: InputVector = (100, 30), spacing: int = 5):
        self.font: pygame.font.Font = font
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.item_size: InputVector = item_size
        self.spacing: int = spacing
        self.items: List[HotbarItem] = []

    def add_item(self, label: str, callback: Callable[[HotbarItem], None]) -> HotbarItem:
        """
        Add a item with specific functionality. Give it a label.
        """
        item = HotbarItem(label, self.font, callback)
        self.items.append(item)
        return item
    
    def add_window(self, label: str, window: Window) -> HotbarItem:
        """
        Add a item to represent opening and closing a window. Give it a label.
        """
        def toggle(item: HotbarItem) -> None:
            window.toggle_shown()
            item.selected = window.shown
        return self.add_item(label, toggle)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render all labels as positioned
        """
        x, y = self.pos
        for item in self.items:
            item.render(surface, (x, y), self.item_size)
            x += self.item_size[0] + self.spacing

    def handle_event(self, event: pygame.event.Event, offset: InputVector = (0, 0)) -> Optional[bool]:
        """
        Handle a event with a given offset to the events position if applicable.
        """
        for item in self.items:
            if item.handle_event(event, offset):
                return True

class App:
    """
    The central application interface for managing UI components.

    Supports registering background, normal, and top-level components with 
    custom rendering and event handling. Components can be added manually or 
    through plugins. Top-level components render above all others and are 
    ideal for overlays such as FPS displays. Return *True* if any plugins 
    event handler should stop event propagation.

    Usage: 
    - Background components render first.
    - Normal components render in order.
    - Top-level components render last.
    """
    def __init__(self, size: InputVector, fps_target: float = 60, background_color: InputColor = (255, 255, 255), flags: int = 0):
        self.screen: pygame.Surface = pygame.display.set_mode(size, flags)
        pygame.display.set_caption("MyUI Window (Pygame)")
        self.size: pygame.math.Vector2 = pygame.math.Vector2(size)
        self.flags: int = flags
        
        self.fps: float = 0
        self.dt: float = 0
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps_target: float = fps_target

        self.active: bool = False
        self.paused: bool = False
        self.render_on_pause: bool = True

        self.background_color: InputColor = background_color

        self.background_render: List[RenderCallback] = []

        self.event_handlers: List[EventCallback] = []
        self.on_render: List[RenderCallback] = []
        self.sorted: List[int] = []

        self.top_handler: List[EventCallback] = []
        self.top_render: List[RenderCallback] = []

        self.plugins: List[PluginWrapper] = []
    
    @property
    def stats(self) -> dict[str, Any]:
        return {"fps": self.fps, "dt": self.dt}
    
    def pause(self): self.paused = True

    def resume(self): self.paused = False
    
    def render(self) -> None:
        """
        Render all components.
        """
        for render in self.background_render:
            self.safe_call(render, self.screen)
        for index in self.sorted:
            self.safe_call(self.on_render[index], self.screen)
        for render in self.top_render:
            self.safe_call(render, self.screen)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[bool]:
        """Parse the event to all components."""
        cursor_handled = False
        for handle in reversed(self.top_handler): 
            if self.safe_call(handle, event, (0, 0)):  # No effect on cursor
                cursor_handled = True
                break
        
        if not cursor_handled:
            for index in reversed(self.sorted):
                if self.safe_call(self.event_handlers[index], event, (0, 0)):
                    cursor_handled = True
                    break

        if not cursor_handled:
            Cursor.set_cursor(self, pygame.SYSTEM_CURSOR_ARROW)
    
    def bring_to_front(self, index: int) -> None:
        """Bring a component to the front."""
        if index in self.sorted:
            self.sorted.remove(index)
            self.sorted.append(index)

    def move_to_index(self, index: int, position: int) -> None:
        """Move a component to a specific rendering position."""
        if index in self.sorted:
            self.sorted.remove(index)
            self.sorted.insert(position, index)
    
    def remove(self, index: int) -> None:
        """Remove a component."""
        for wrapper in self.plugins[::]:
            if wrapper.index == index:
                self.plugins.remove(wrapper)
                break
        if index in self.sorted:
            self.sorted.remove(index)
    
    def remove_other(self, layer: Literal["top", "background"] = "top", render: RenderCallback = None, on_event: EventCallback = None):
        if layer == "top":
            if render and render in self.top_render: 
                self.top_render.remove(render)
            if on_event and on_event in self.top_handler: 
                self.top_handler.remove(on_event)
        elif layer == "background" and render and render in self.background_render:
            self.background_render.remove(render)
    
    def add_handler(self, on_render: RenderCallback = None, on_event: EventCallback = None) -> int:
        """
        Adds a new component with both render and event handler callbacks.

        Args:
            on_render (Callable[[pygame.Surface], Any]): Render function.
            on_event (Callable[[pygame.event.Event, Vector2], Optional[bool]]): Event handler that returns True if event is handled.

        Returns:
            int: Index used for ordering and removal. (Identifier)
        """
        index = len(self.on_render)
        if on_render: self.on_render.append(on_render)
        if on_event: self.event_handlers.append(on_event)
        self.sorted.append(index)
        return index
    
    def add_background(self, on_render: Callable[[pygame.Surface], Any]) -> None:
        """Adds a background component. No events will be parsed, but the components will get rendered first."""
        self.background_render.append(on_render)
    
    def add_top(self, on_render: Callable[[pygame.Surface], Any] = None, on_event: Callable[[pygame.event.Event, pygame.math.Vector2], Any] = None):
        """Adds a top-level component that renders above all standard components, unaffected by normal sorting. """
        if on_render: self.top_render.append(on_render)
        if on_event: self.top_handler.append(on_event)
    
    def run(self) -> None:
        """Run the app when configured."""
        self.active = True
        while self.active:
            if not self.active:
                break
            self.tick()
    
    def tick(self) -> None:
        """Simulate a tick for the app."""
        self.dt = self.clock.tick(self.fps_target)
        self.fps = self.clock.get_fps()
        for wrapper in self.plugins:
            wrapper.plugin.on_update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
                return
            if not self.paused: 
                self.handle_event(event)
        self.screen.fill(self.background_color)
        if not (self.render_on_pause and self.paused):
            self.render()
        pygame.display.update()
    
    @staticmethod
    def safe_call(func: Callable, *args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[Error] {func.__name__}: {e}")
            traceback.print_exc()
    
    def load_plugins(self, plugins: List[PluginWrapper]) -> None:
        """Load plugins from a list of plugin wrappers."""
        for wrapper in plugins:
            if wrapper.enabled:
                self.safe_call(wrapper.plugin.on_load, self)
                if wrapper.layer == "top":
                    self.add_top(wrapper.plugin.on_render, wrapper.plugin.on_event)
                elif wrapper.layer == "normal":
                    wrapper.index = self.add_handler(wrapper.plugin.on_render, wrapper.plugin.on_event)
                elif wrapper.layer == "background":
                    self.add_background(wrapper.plugin.on_render)
                self.plugins.append(wrapper)
    
    def unload_plugins(self) -> None:
        for wrapper in self.plugins[::]:
            if hasattr(wrapper.plugin, "on_unload"):
                wrapper.plugin.on_unload()
            if wrapper.layer == "top":
                self.remove_other("top", wrapper.plugin.on_render, wrapper.plugin.on_event)
            elif wrapper.layer == "normal":
                self.remove(wrapper.index)
            elif wrapper.layer == "background":
                self.remove_other("background", wrapper.plugin.on_render)
            self.plugins.remove(wrapper)
    
    def ready(self) -> None:
        """Recreate and recycle the app."""
        self.screen = pygame.display.set_mode(self.size, self.flags)
    
    def cleanup(self) -> None:
        """Cleans up all components and resets the app."""
        self.background_render.clear()
        self.event_handlers.clear()
        self.on_render.clear()
        self.sorted.clear()
        self.top_handler.clear()
        self.top_render.clear()
        self.unload_plugins()
    
    def _backup_ui(self) -> Tuple[List[int], List[RenderCallback], List[EventCallback], List[RenderCallback], List[EventCallback], List[RenderCallback]]:
        return (
            self.sorted[:], self.on_render[:], self.event_handlers[:],
            self.top_render[:], self.top_handler[:], self.background_render[:]
        )
    
    def _restore_ui(self, backup: Tuple[List[int], List[RenderCallback], List[EventCallback], List[RenderCallback], List[EventCallback], List[RenderCallback]]) -> None:
        self.sorted, self.on_render, self.event_handlers, \
        self.top_render, self.top_handler, self.background_render = backup
    
    def reload(self, plugins: Optional[List[PluginWrapper]] = None, preserve_ui: bool = True, reset_plugins: bool = True) -> None:
        """Reload the application with optional plugin list and optional UI preservation."""
        
        if reset_plugins or not preserve_ui:
            self.unload_plugins()

        ui_backup = self._backup_ui() if preserve_ui else None

        self.quit()       # Cleans everything
        self.ready()      # Reinitialize screen
        
        if preserve_ui: self._restore_ui(ui_backup)
        
        if plugins:
            self.load_plugins(plugins)

        self.run()
    
    def quit(self) -> None:
        """Quit the app when running."""
        self.active = False
        self.cleanup()

component = Union[Text, Button, Slider, DropdownMenu, Tooltip, Dropbox, Window, Surface, HotbarItem, Hotbar, App]

del InputVector, InputColor, RenderCallback, EventCallback, Literal, List, Tuple, Dict, Any, Union, Optional, Callable, dataclass

print("- MyUI ui")