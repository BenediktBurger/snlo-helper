# MIT License

# Copyright (c) 2024 Benedikt Burger

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Autoclicker setup
=================

General methods for the autoclicker
"""

import logging
from typing import Any, Optional, Union

import pyautogui as gui
from pyperclip import paste


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

Point = Union[gui.Point, tuple[float, float]]


"""

Setup of the screen and scaling
-------------------------------

All positions in code are given on a Full HD (1920 * 1080) screen and dynamically adjusted to the
screen resolution.
"""


def read_display_screenfactors(standard: Point = (1920, 1080)) -> Point:
    """Read the scaling factor from Full HD to the current display resolution."""
    width, height = gui.size()
    return standard[0] / width, standard[1] / height


def set_screenfactors(new_factors: Optional[tuple[float, float]] = None) -> tuple[float, float]:
    """Set the screenfactors to `new_factors` or detect them automatically."""
    global factors
    factors = read_display_screenfactors() if new_factors is None else new_factors
    return factors


def get_screenfactors() -> Optional[tuple[float, float]]:
    """Get the current screenfactors or None, if not yet set."""
    global factors
    try:
        return factors
    except NameError:
        return None


def scale(x: Union[float, Point], y: Optional[float] = None) -> Point:
    """Scale coordinates from the definition standard to the current screen."""
    global factors
    if isinstance(x, (list, tuple)):
        if y is None:
            x, y = x
        else:
            raise ValueError("You cannot specify x as a tuple and y.")
    elif y is None:
        raise ValueError("You have to specify two coordinatres.")
    try:
        return x / factors[0], y / factors[1]
    except NameError:
        log.warning("Factors was not set, running `set_screenfactors` to get values.")
        set_screenfactors()
        return x / factors[0], y / factors[1]


def standard_position() -> Point:
    """Get the mouse position in standard coordinates (x, y)."""
    point = gui.position()
    global factors
    return point.x * factors[0], point.y * factors[1]


"""
Helper functions
----------------

GUI functions to get/set content from/into data fields.
"""


def get_content(position: Point) -> str:
    """Get the content of the field at position via double click.

    If there is a "-" in the text, the extraction fails!
    """
    gui.doubleClick(*scale(*position))
    gui.hotkey("ctrl", "c")
    return paste()


def get_value(position: Point) -> float:
    """Move to position, retrieve value and return float."""
    return float(get_content(position))


def get_content_complete(position: Point) -> str:
    """Go to position and retrieve the content there, marking all."""
    gui.click(*scale(*position))
    gui.hotkey("ctrl", "home")
    # both shift keys are necessary if keylock is on
    gui.hotkey("ctrl", "shiftleft", "shiftright", "end")
    gui.hotkey("ctrl", "c")
    return paste()


def get_value_complete(position: Point) -> float:
    """Move to position, retrieve value via context menu (slower) and return float."""
    return float(get_content_complete(position))


def set_value(position: Point, value: Any) -> None:
    """Move to position, insert value as string."""
    gui.doubleClick(*scale(*position))
    gui.press("delete")
    gui.doubleClick()
    gui.write(str(value))


def alt_tab() -> None:
    gui.hotkey("alt", "tab")


def get_position() -> Point:
    return gui.position()
