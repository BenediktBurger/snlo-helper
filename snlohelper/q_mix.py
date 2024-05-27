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


class QMix(BaseFunction):
    _function = Functions.QMIX
    _run_pos = (174, 61)
    _result_pos = (160, 260)
    _close_pos = (446, 20)
    _configuration_pos = {
        "Crystal": [(250, 76)],
        "Temperature": [(360, 76)],
        "Red1": [(155, 155)],
        "Red2": [(209, 155)],
        "Blue": [(266, 155)],
        "XY": [(357, 128)],
        "XZ": [(396, 128)],
        "YZ": [(429, 128)],
        "Mix": [(359, 168)],
        "OPO": [(416, 168)]
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
