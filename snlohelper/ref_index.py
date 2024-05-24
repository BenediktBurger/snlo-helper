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

from typing import Any

from .base_function import BaseFunction, Functions


class RefractiveIndex(BaseFunction):
    _function = Functions.REF_INDEX
    _run_pos = (295, 187)
    _result_pos = (160, 260)
    _close_pos = (365, 41)
    _configuration_pos = {
        "Crystal": [(170, 90)],
        "Temperature": [(290, 90)],
        "theta": [(170, 146)],
        "phi": [(300, 146)],
        "Wavelength": [(170, 190)],
    }

    def run_and_read(
        self,
        waiting_time: float = 0.1,
        max_tries: int = 10,
        interval: float = 0.1,
        waiting_line_count: int = 3,
    ) -> dict[str, Any]:
        return super().run_and_read(waiting_time, max_tries, interval, waiting_line_count)

    def refractive_indices(
        self, Crystal=None, Temperature=None, theta=None, phi=None, Wavelength=None
    ) -> list[float]:
        """Get the refractive indices (o, e).

        For the crystal, you have to use letters to press, for example "BB" to select the second
        crystal starting with a "B". In order to ensure, that it starts correctly, use any other
        letter first, e.g. "ABB".
        """
        kwargs = {
            "Crystal": Crystal,
            "Temperature": Temperature,
            "theta": theta,
            "phi": phi,
            "Wavelength": Wavelength,
        }
        results = self.configure_run_read(kwargs)
        return results["Refractive index (o,e)"]
