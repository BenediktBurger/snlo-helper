import time
from typing import Any, Optional

from .utils import Position, gui, scale, set_value, get_content_complete
from .main_window import Functions, open_function


class MixMethods:
    """Parent class for mix methods.

    Subclass it for specific methods. You should define the positions and the result interpretation.
    """

    _function: Functions
    # Positions
    _accept_pos: Position
    _run_pos: Position
    _change_inputs_pos: Position
    _result_pos: Position  # of the results field
    _configuration_pos: dict[str, list[Position]]  # of the configuration fields

    def open(self) -> None:
        """Open the function."""
        open_function(self._function)

    def accept(self) -> None:
        """Click 'Accept'."""
        gui.click(*scale(*self._accept_pos))

    def run(self) -> None:
        """Click 'Run'."""
        gui.click(*scale(*self._run_pos))

    def change_inputs(self) -> None:
        """Click 'Change Inputs'."""
        gui.click(*scale(*self._change_inputs_pos))

    def configure(self, data: Optional[dict[str, Any]] = None) -> None:
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
            for i, val in enumerate(value):
                if val is not None:
                    set_value(positions[i], val)

    def get_configuration(self) -> dict[str, Any]:
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

    def interpret_results(self, rows: list[str]) -> dict[str, Any]:
        """Interpret the results and return them as a dictionary."""
        data = {}
        for row in rows:
            text, values = row.split("=")
            data[text.strip()] = [float(i) for i in values.split()]
        return data

    def read_results(self) -> list[str]:
        return get_content_complete(self._result_pos).split("\r\n")

    def run_and_read(
        self,
        waiting_time: float = 1,
        max_tries: int = 10,
        interval: float = 0.5,
        successful_line_count: int = 3,
    ) -> dict[str, Any]:
        """Run an analysis and return the result."""
        self.run()
        time.sleep(waiting_time)
        for _ in range(max_tries):
            rows = self.read_results()
            if len(rows) > successful_line_count:
                break
            time.sleep(interval)

        # interpret results and save as dictionary:
        return self.interpret_results(rows)

    def configure_run_read(
        self, data: Optional[dict[str, Any]] = None, **kwargs
    ) -> dict[str, float | list[float]]:
        """Configure and run an analysis and return the result."""
        self.configure(data)
        self.accept()
        return self.run_and_read(**kwargs)


def generate_position_dict(
    first_configuration_field: Position, configuration_names: list[str]
) -> dict[str, list[Position]]:
    """Generate a position dictionary for mix methods.

    This utility makes it easier to generate a position matrix with three fields per entry.
    Adjust it afterwards according to the number of entries.

    :param first_configuration_field: Position (tuple) of the top left configuration field.
    :param configuration_names: List of all the names (in order) of the configuration.
    """
    # Notes regarding positions: horizontal distance is 60 px, vertical distance 16 pixels
    positions = {}
    i = 0
    for name in configuration_names:
        positions[name] = [
            (first_configuration_field[0], first_configuration_field[1] + 16 * i),
            (first_configuration_field[0] + 60, first_configuration_field[1] + 16 * i),
            (first_configuration_field[0] + 120, first_configuration_field[1] + 16 * i),
        ]
    return positions
