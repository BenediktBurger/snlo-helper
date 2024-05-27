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

import time
from typing import Any, Optional, Protocol

from .utils import Point, gui, scale, get_content_complete, set_value
from .functions import Functions, open_function


class BaseFunction(Protocol):
    """Base class for a function window."""

    _function: Functions
    # Positions
    _run_pos: Point  # of the run field
    _result_pos: Point  # of the results field
    _close_pos: Point
    _configuration_pos: dict[str, list[Point]]  # of the configuration fields

    def open(self) -> None:
        """Open the function."""
        open_function(self._function)

    def run(self) -> None:
        """Click 'Run'."""
        gui.click(*scale(*self._run_pos))

    def close(self) -> None:
        """Click 'x'."""
        self.open()
        gui.click(*scale(*self._close_pos))

    def configure(
        self, data: Optional[dict[str, Any | list[Any] | tuple[Any, ...]]] = None
    ) -> None:
        """Configure the values and leave the config window open.

        If any value is "None", that field will not be changed. This is useful, if you want to
        change a single value in a row.
        For example `data={'Wavelengths (nm)': [1064.5, None, None]}` will set the first wavelength
        to 1064.5 nm while leaving the other wavelengths untouched.
        """
        self.open()
        if data is None:
            return
        for key, value in data.items():
            positions = self._configuration_pos[key]
            if isinstance(value, (list, tuple)):
                for i, val in enumerate(value):
                    if val is not None:
                        set_value(positions[i], val)
            else:
                if value is not None:
                    set_value(positions[0], value)

    def get_configuration(self) -> dict[str, list[float | str]]:
        """Read the current configuration."""
        self.open()
        data = {}
        for key, positions in self._configuration_pos.items():
            d = []
            for pos in positions:
                val = get_content_complete(pos)
                try:
                    d.append(float(val))
                except ValueError:
                    d.append(val)
            data[key] = d
        return data

    def read_results(self) -> list[str]:
        return get_content_complete(self._result_pos).split("\r\n")

    def interpret_results(self, rows: list[str]) -> dict[str, Any]:
        """Interpret the results and return them as a dictionary."""
        data = {}
        for row in rows:
            # skip empty lines
            if not row:
                continue
            if row == 'ERROR: No phase match found.':
                raise Exception('No phase match found')
            
            text, values = row.split("=")
            content = []
            for element in values.split():
                try:
                    val = float(element)
                except ValueError:
                    val = element
                content.append(val)
            data[text.strip()] = content
        return data

    def run_and_read(
        self,
        waiting_time: float = 1,
        max_tries: int = 10,
        interval: float = 0.5,
        waiting_line_count: int = 3,
    ) -> dict[str, Any]:
        """Run an analysis and return the result."""
        self.run()
        time.sleep(waiting_time)
        for _ in range(max_tries):
            rows = self.read_results()
            if len(rows) > waiting_line_count:
                break
            time.sleep(interval)

        # interpret results and save as dictionary:
        return self.interpret_results(rows)

    def configure_run_read(
        self, data: Optional[dict[str, Any]] = None, **kwargs
    ) -> dict[str, Any]:
        """Configure and run an analysis and return the result."""
        self.configure(data)
        return self.run_and_read(**kwargs)


def generate_position_dict(
    first_position: Point,
    configuration_names: list[str],
    columns: int = 3,
    column_distance: int = 60,
) -> dict[str, list[Point]]:
    """Generate a position dictionary for functions.

    This utility makes it easier to generate a position matrix with three fields per entry.
    Adjust it afterwards according to the number of entries.

    :param first_position: Position (tuple) of the top left configuration field.
    :param configuration_names: List of all the names (in order) of the configuration.
    """
    # Notes regarding positions for mix: horizontal distance is 60 px, vertical distance 16 pixels
    positions = {}
    i = 0
    for name in configuration_names:
        positions[name] = [
            (first_position[0] + j * column_distance, first_position[1] + 16 * i)
            for j in range(columns)
        ]
        i += 1
    return positions
