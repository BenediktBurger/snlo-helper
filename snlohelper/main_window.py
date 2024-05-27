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
The SNLO main window
"""

from typing import Optional, TypeVar

from .utils import gui, scale, get_screenfactors, set_screenfactors, Point
from .functions import Functions, open_function
from .base_function import BaseFunction
from .ref_index import RefractiveIndex
from .focus import Focus
from .two_d_mix_lp import TwoDMixLP
from .two_d_mix_sp import TwoDMixSP
from .q_mix import QMix
from .pw_opo_bb import PW_OPO_BB


function_classes = {
    Functions.REF_INDEX: RefractiveIndex,
    Functions.QMIX: QMix,
    Functions.TWOD_MIX_LP: TwoDMixLP,
    Functions.TWOD_MIX_SP: TwoDMixSP,
    Functions.PW_OPO_BB: PW_OPO_BB,
    Functions.FOCUS: Focus,
}

FunctionClass = TypeVar("FunctionClass")


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

    def _open_function(self, function_class: type[FunctionClass]) -> FunctionClass:
        function = function_class()
        function.open()  # type: ignore
        return function

    def open_refractive_index(self) -> RefractiveIndex:
        return self._open_function(RefractiveIndex)
    
    def open_q_mix(self) -> QMix:
        return self._open_function(QMix)

    def open_two_d_mix_lp(self) -> TwoDMixLP:
        return self._open_function(TwoDMixLP)

    def open_two_d_mix_sp(self) -> TwoDMixSP:
        return self._open_function(TwoDMixSP)
    
    def open_pw_opo_bb(self) -> PW_OPO_BB:
        return self._open_function(PW_OPO_BB)

    def open_focus(self) -> Focus:
        return self._open_function(Focus)
