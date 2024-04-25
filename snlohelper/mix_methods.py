from typing import Any, Optional, Protocol

from .utils import Position, gui, scale
from .base_function import BaseFunction


class MixMethods(BaseFunction, Protocol):
    """Parent class for mix methods.

    Subclass it for specific methods. You should define the positions and the result interpretation.
    """

    _accept_pos: Position
    _change_inputs_pos: Position

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
