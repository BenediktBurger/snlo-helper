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
from collections import defaultdict

from .base_function import BaseFunction, Functions


class PW_OPO_BB(BaseFunction):
    _function = Functions.PW_OPO_BB
    _run_pos = (433, 475)
    _result_pos = (182, 618)
    _close_pos = (515, 174)
    _configuration_pos = {
        "Wavelengths (nm)": [(351, 219), (423, 219), (489, 219)],
        "Index of refraction": [(351, 235), (423, 235), (489, 235)],
        "Group velocity index": [(351, 251), (423, 251), (489, 251)],
        "Crystal left reflectivity": [(351, 267), (423, 267), (489, 267)],
        "Crystal right reflectivity": [(351, 283), (423, 283), (489, 283)],
        "Crystal loss (per mm)": [(351, 299), (423, 299), (489, 299)],
        "Enrgy/Pwr left (J/W)": [(351, 315), (423, 315), (489, 315)],
        "Enrgy/Pwr right (J/W)": [(351, 331), (423, 331)],
        "Pulse duration (FWHM ns)": [(351, 347), (423, 347), (489, 347)],
        "Beam diam. (FWHM mm)": [(351, 363), (423, 363), (489, 363)],
        "Left mirror reflectivity": [(351, 379), (423, 379), (489, 379)],
        "Right mirror reflectivity": [(351, 395), (423, 395), (489, 395)],
        "L mir. to Xtal phase (rad)": [(351, 411), (423, 411), (489, 411)],
        "R mir. to Xtal phase (rad)": [(351, 427), (423, 427), (489, 427)],
        "Cavity/Xtal length (mm)": [(351, 443), (423, 443)],
        "Pump bandwidth (MHz)": [(351, 459)],
        "Pump mode spacing (MHz)": [(351, 475)],
        "Pump FM (1/0)": [(351, 491)],
        "Deff (pm/V)": [(351, 507)],
        "Cav. type (1=lin. 0=ring)": [(351, 523)],
        "Delta k(1/mm)": [(351, 539)],
        "# of z integration steps": [(351, 555)],
        "New noise (1/0)": [(351, 571)]
    }

    def interpret_results(self, rows: list[str]) -> dict[str, Any]:
        """Interpret the results and return them as a dictionary."""
        data = defaultdict(list) # to support duplicate rows e.g., in qmix for different phase-matching conditions
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
            data[text.strip()].append(content)
        return data

    def run_and_read(
        self,
        waiting_time: float = 0.1,
        max_tries: int = 10,
        interval: float = 0.1,
        waiting_line_count: int = 3,
    ) -> dict[str, Any]:
        return super().run_and_read(waiting_time, max_tries, interval, waiting_line_count)
