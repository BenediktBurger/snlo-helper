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

from typing import Any, Optional, Protocol

from .utils import Point, gui, scale
from .base_function import BaseFunction


class MixMethods(BaseFunction, Protocol):
    """Parent class for mix methods.

    Subclass it for specific methods. You should define the positions and the result interpretation.
    """

    _accept_pos: Point
    _change_inputs_pos: Point

    def accept(self) -> None:
        """Click 'Accept'."""
        gui.click(*scale(*self._accept_pos))

    def change_inputs(self) -> None:
        """Click 'Change Inputs'."""
        gui.click(*scale(*self._change_inputs_pos))

    def configure_run_read(
        self, data: Optional[dict[str, Any]] = None, **kwargs
    ) -> dict[str, float | list[float]]:
        """Configure and run an analysis and return the result."""
        self.configure(data)
        self.accept()
        return self.run_and_read(**kwargs)
