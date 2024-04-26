"""
The SNLO main window
"""

from typing import Optional

from .utils import gui, scale, get_screenfactors, set_screenfactors, Point
from .functions import Functions, open_function
from .base_function import BaseFunction
from .ref_index import RefractiveIndex
from .focus import Focus
from .two_d_mix_lp import TwoDMixLP
from .two_d_mix_sp import TwoDMixSP


function_classes = {
    Functions.REF_INDEX: RefractiveIndex,
    Functions.TWOD_MIX_LP: TwoDMixLP,
    Functions.TWOD_MIX_SP: TwoDMixSP,
    Functions.FOCUS: Focus,
}


class MainWindow:
    _close_pos = (95, 14)

    def __init__(self, screenfactors: Optional[Point] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        sf = get_screenfactors()
        if sf is None or screenfactors is not None:
            set_screenfactors(new_factors=screenfactors)

    def close(self) -> None:
        gui.click(*scale(self._close_pos))

    def open_function(self, key: str | Functions) -> Optional[BaseFunction]:
        open_function(key)
        if key in function_classes:
            return function_classes[key]()
