#  helper_types.py
#  Copyright (c) TotallyNotSeth 2025
#  All rights reserved.

from collections import namedtuple

# Coordinates
Coordinates = namedtuple("Coordinates", "x y")
CoordinatesType = Coordinates | tuple[int, int]


# Box drawing characters
class BoxDrawingCharacters:
    HORIZONTAL = "─"
    VERTICAL = "│"
    TOP_LEFT = "┌"
    TOP_RIGHT = "┐"
    BOTTOM_LEFT = "└"
    BOTTOM_RIGHT = "┘"
    HORIZONTAL_T = "┬"
    HORIZONTAL_B = "┴"
    VERTICAL_L = "├"
    VERTICAL_R = "┤"
    CROSS = "┼"


class StandardBoxDrawingCharacters(BoxDrawingCharacters):
    pass


class DoubleBoxDrawingCharacters(BoxDrawingCharacters):
    HORIZONTAL = "═"
    VERTICAL = "║"
    TOP_LEFT = "╔"
    TOP_RIGHT = "╗"
    BOTTOM_LEFT = "╚"
    BOTTOM_RIGHT = "╝"
    HORIZONTAL_T = "╦"
    HORIZONTAL_B = "╩"
    VERTICAL_L = "╠"
    VERTICAL_R = "╣"
    CROSS = "╬"
