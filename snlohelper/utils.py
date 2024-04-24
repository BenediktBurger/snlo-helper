"""
Autoclicker setup
=================

General methods for the autoclicker
"""

import logging
from typing import Any, Optional

import pyautogui as gui
from pyperclip import paste


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

Position = tuple[float, float]


"""

Setup of the screen and scaling
-------------------------------

All positions in code are given on a Full HD (1920 * 1080) screen and dynamically adjusted to the
screen resolution.
"""


def get_screenfactors(standard: Position = (1920, 1080)) -> Position:
    """Get the scaling factor from Full HD to the current display resolution."""
    width, height = gui.size()
    return standard[0] / width, standard[1] / height


def set_screenfactors(new_factors: Optional[tuple[float, float]] = None) -> tuple[float, float]:
    """Set the screenfactors to `new_factors` or detect them automatically."""
    global factors
    factors = get_screenfactors() if new_factors is None else new_factors
    return factors


def scale(x: float | Position, y: float | None = None) -> Position:
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


def standard_position() -> Position:
    """Get the mouse position in standard coordinates (x, y)."""
    point = gui.position()
    global factors
    return point.x * factors[0], point.y * factors[1]


"""
Helper functions
----------------

GUI functions to get/set content from/into data fields.
"""


def get_content(position: Position) -> str:
    """Get the content of the field at position via double click.

    If there is a "-" in the text, the extraction fails!
    """
    gui.doubleClick(*scale(*position))
    gui.hotkey("ctrl", "c")
    return paste()


def get_value(position: Position) -> float:
    """Move to position, retrieve value and return float."""
    return float(get_content(position))


def get_content_complete(position: Position) -> str:
    """Go to position and retrieve the content there, marking all."""
    gui.click(*scale(*position))
    gui.hotkey("ctrl", "home")
    # both shift keys are necessary if keylock is on
    gui.hotkey("ctrl", "shiftleft", "shiftright", "end")
    gui.hotkey("ctrl", "c")
    return paste()


def get_value_complete(position: Position) -> float:
    """Move to position, retrieve value via context menu (slower) and return float."""
    return float(get_content_complete(position))


def set_value(position: Position, value: Any) -> None:
    """Move to position, insert value as string."""
    gui.doubleClick(*scale(*position))
    gui.press("delete")
    gui.doubleClick()
    gui.write(str(value))
