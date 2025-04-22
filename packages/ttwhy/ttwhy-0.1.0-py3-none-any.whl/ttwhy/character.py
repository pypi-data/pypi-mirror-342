#  character.py
#  Copyright (c) TotallyNotSeth 2025
#  All rights reserved.

# Package imports
import pygame

# Local imports
from ttwhy.color import Color, WHITE, BLACK
from ttwhy.util.helper_types import Coordinates

# Package exports
__all__ = ["Character", "BLINK"]

# Constants
BLINK = 0x1
BLINK_FRAMES = 60


class Character:
    """A class representing a terminal character with a foreground and background color."""
    def __init__(self, coords: Coordinates, char: str = " ", fg: Color = WHITE, bg: Color = BLACK,
                 font: pygame.font.Font = None) -> None:
        self.coords: Coordinates = coords
        self._char: str = char
        self.fg: Color = fg
        self.bg: Color = bg
        self.style: int = 0x0
        if not font:
            font = pygame.font.SysFont("Courier New", 32)
        self.font: pygame.font.Font = font

    @property
    def char(self) -> str:
        return self._char

    @char.setter
    def char(self, value: str = None) -> None:
        if not value or len(value) == 0:
            value = " "
        elif len(value) > 1:
            raise ValueError("`char` must be a single character")
        self._char = value

    def render(self, surface: pygame.Surface, x: int, y: int, frame_count: int = 0) -> None:
        """Render the character to a surface at a given position."""
        if frame_count < BLINK_FRAMES and BLINK & self.style:
            text = self.font.render(self.char, True, self.bg, self.bg)
        else:
            text = self.font.render(self.char, True, self.fg, self.bg)
        surface.blit(text, (x, y))

    @property
    def width(self) -> int:
        return self.font.size(" ")[0]  # Shouldn't be a problem since all characters are monospaced

    @property
    def height(self) -> int:
        return self.font.size(" ")[1]
