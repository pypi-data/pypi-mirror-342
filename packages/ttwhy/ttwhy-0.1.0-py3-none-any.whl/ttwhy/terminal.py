#  terminal.py
#  Copyright (c) TotallyNotSeth 2025
#  All rights reserved.

# Builtin imports
import typing

# Package imports
import pygame

# Local imports
from ttwhy.character import Character
from ttwhy.color import WHITE, BLACK
from ttwhy.util.helper_types import *

# Package exports
__all__ = ["Terminal"]


class Terminal:
    """A class representing a terminal with a grid of characters."""
    def __init__(self, surface: pygame.Surface, width: int = 80, height: int = 24, font: pygame.font.Font = None):
        self.surface: pygame.Surface = surface
        self.width: int = width
        self.height: int = height
        if not font:
            font = pygame.font.Font("vendored/MxPlus_IBM_VGA_8x16.ttf", 32)
        self.font: pygame.font.Font = font

        self.grid: list[list[Character]] = [
            [Character(Coordinates(x, y), font=self.font)
             for x in range(width)]
            for y in range(height)
        ]

        self.changed_chars: set[Character] = set()
        self.text_lines: list[str] = []

    def render(self, frame_count: int = 0) -> None:
        """Render the terminal to a surface."""
        for char in self.changed_chars:
            char.render(self.surface, *self.char_pos_to_surface_pos(char.coords), frame_count)

    def surface_pos_to_char_pos(self, surface_coords: CoordinatesType) -> Coordinates:
        """Convert a surface position to a character position."""
        if isinstance(surface_coords, tuple):
            surface_coords = Coordinates(*surface_coords)
        x_offset = self.surface.get_width() // 2 - self.width * self.grid[0][0].width // 2
        y_offset = self.surface.get_height() // 2 - self.height * self.grid[0][0].height // 2
        char_x = (surface_coords.x - x_offset) // self.grid[0][0].width
        char_y = (surface_coords.y - y_offset) // self.grid[0][0].height
        if char_x < 0:
            char_x = 0
        elif char_x >= self.width:
            char_x = self.width - 1
        if char_y < 0:
            char_y = 0
        elif char_y >= self.height:
            char_y = self.height - 1
        return Coordinates(char_x, char_y)

    def char_pos_to_surface_pos(self, char_coords: CoordinatesType) -> Coordinates:
        """Convert a character position to a surface position."""
        if isinstance(char_coords, tuple):
            char_coords = Coordinates(*char_coords)
        x_offset = self.surface.get_width() // 2 - self.width * self.grid[0][0].width // 2
        y_offset = self.surface.get_height() // 2 - self.height * self.grid[0][0].height // 2
        surface_x = char_coords.x * self.grid[0][0].width + x_offset
        surface_y = char_coords.y * self.grid[0][0].height + y_offset
        return Coordinates(surface_x, surface_y)

    def set_color_at_char(self, coords: CoordinatesType, fg: pygame.Color = WHITE, bg: pygame.Color = BLACK) -> None:
        """Set the background color of a character at a given position."""
        if isinstance(coords, tuple):
            coords = Coordinates(*coords)
        char = self.grid[coords.y][coords.x]
        char.fg = fg
        char.bg = bg
        self.changed_chars.add(char)

    def draw_char(self, char: str, coords: CoordinatesType, fg: pygame.Color = WHITE, bg: pygame.Color = BLACK) -> None:
        """Set a character at a given position."""
        if isinstance(coords, tuple):
            coords = Coordinates(*coords)
        char_obj = self.grid[coords.y][coords.x]
        char_obj.char = char
        self.set_color_at_char(coords, fg, bg)
        self.changed_chars.add(char_obj)

    def draw_str(self, text: str, coords: CoordinatesType, fg: pygame.Color = WHITE, bg: pygame.Color = BLACK) -> None:
        """Print text to the terminal at a given position with a given color."""
        if isinstance(coords, tuple):
            coords = Coordinates(*coords)
        for i, char in enumerate(text):
            self.draw_char(char, (coords.x + i, coords.y), fg, bg)

    def draw_box(self, coords: CoordinatesType, width: int, height: int,
                 fg: pygame.Color = WHITE, bg: pygame.Color = BLACK,
                 style: typing.Type[BoxDrawingCharacters] = StandardBoxDrawingCharacters) -> None:
        """Draw a box at a given position with a given color."""
        if isinstance(coords, tuple):
            coords = Coordinates(*coords)
        for i in range(width):
            self.draw_char(style.HORIZONTAL, (coords.x + i, coords.y), fg, bg)
            self.draw_char(style.HORIZONTAL, (coords.x + i, coords.y + height - 1), fg, bg)
        for i in range(height):
            self.draw_char(style.VERTICAL, (coords.x, coords.y + i), fg, bg)
            self.draw_char(style.VERTICAL, (coords.x + width - 1, coords.y + i), fg, bg)
        self.draw_char(style.TOP_LEFT, (coords.x, coords.y), fg, bg)
        self.draw_char(style.TOP_RIGHT, (coords.x + width - 1, coords.y), fg, bg)
        self.draw_char(style.BOTTOM_LEFT, (coords.x, coords.y + height - 1), fg, bg)
        self.draw_char(style.BOTTOM_RIGHT, (coords.x + width - 1, coords.y + height - 1), fg, bg)

    def clear(self) -> None:
        """Clear the terminal."""
        for char in self.changed_chars:
            char.char = " "
            char.bg = BLACK
            char.fg = WHITE
        self.changed_chars.clear()

    def print(self, text: str) -> None:
        """Print text to the terminal."""
        self.text_lines.append(text)
        if len(self.text_lines) > self.height:
            self.text_lines.pop(0)

    def draw_text_buffer(self) -> None:
        """Draw text to the terminal."""
        for i, line in enumerate(self.text_lines):
            self.draw_str(line, (0, i))

    def process_input_key(self, event: pygame.event.Event) -> None:
        """Process a key press."""
        line = self.text_lines[-1]
        if event.key == pygame.K_BACKSPACE:
            if len(line) > 3:
                self.text_lines[-1] = line[:-2] + "█"
        elif event.key == pygame.K_RETURN:
            self.text_lines[-1] = line[:-1]
            self.print("> █")
        else:
            self.text_lines[-1] = line[:-1] + event.unicode + "█"
