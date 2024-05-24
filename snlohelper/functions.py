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

from enum import StrEnum

from .utils import Point, gui, scale


# coordinates of the functions (in FHD standard)
_functions_coord: dict[str, Point] = {
    "Ref. Ind.": (66, 46),
    "Qmix": (66, 66),
    "Bmix": (66, 93),
    "QPM": (66, 120),
    "Opoangles": (66, 146),
    "Ncpm": (66, 173),
    "GVM": (66, 200),
    "PW-mix-LP": (66, 233),
    "PW-mix-SP": (66, 260),
    "PW-mix-BB": (66, 286),
    "2D-mix-LP": (66, 313),
    "2D-mix-SP": (66, 340),
    "PW-cav-LP": (66, 366),
    "PW-OPO-SP": (66, 393),
    "PW-OPO-BB": (66, 420),
    "2D-cav-LP": (66, 446),
    "Focus": (66, 473),
    "Cavity": (66, 500),
}


class Functions(StrEnum):
    """Enum for the functions."""

    REF_INDEX = "Ref. Ind."
    QMIX = "Qmix"
    BMIX = "Bmix"
    QPM = "QPM"
    OPO_ANGLES = "Opoangles"
    NCPM = "Ncpm"
    GVM = "GVM"
    PW_MIX_LP = "PW-mix-LP"
    PW_MIX_SP = "PW-mix-SP"
    PW_MIX_BB = "PW-mix-BB"
    TWOD_MIX_LP = "2D-mix-LP"
    TWOD_MIX_SP = "2D-mix-SP"
    PW_CAV_LP = "PW-cav-LP"
    PW_OPO_SP = "PW-OPO-SP"
    PW_OPO_BB = "PW-OPO-BB"
    TWOD_CAV_LP = "2D-cav-LP"
    FOCUS = "Focus"
    CAVITY = "Cavity"


def open_function(key: str | Functions) -> None:
    """opens function according to key"""
    gui.click(*scale(*_functions_coord[key]))
