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

from .main_window import Functions
from .mix_methods import MixMethods


class TwoDMixLP(MixMethods):
    """The '2D-mix-LP' method."""

    _function = Functions.TWOD_MIX_LP
    _accept_pos = (506, 520)
    _run_pos = (140, 220)
    _close_pos = (540, 140)
    _change_inputs_pos = (373, 166)
    _result_pos = (133, 293)

    # coordinates of the 2DmixLP-function (in FHD standard)
    _configuration_pos = {
        "Wavelengths (nm)": [(400, 186), (460, 186), (520, 186)],
        "Indexes of refraction": [(400, 200), (460, 200), (520, 200)],
        "Phases at input (rad)": [(400, 213), (460, 213), (520, 213)],
        "Input face reflectivity (0-1)": [(400, 226), (460, 226), (520, 226)],
        "Output face reflectivity (0-1)": [(400, 246), (460, 246), (520, 246)],
        "Crystal loss (1/mm)": [(400, 260), (460, 260), (520, 260)],
        "Energy/power (J or W)": [(416, 280), (483, 280), (550, 280)],
        "Pulse duration (fwhm ns)": [(400, 293), (460, 293), (520, 293)],
        "Beam diam. (fwhm mm)": [(400, 306), (460, 306), (520, 306)],
        "Supergaussian coeff.": [(400, 326), (460, 326), (520, 326)],
        "n2 red1 (sq cm/W)": [(400, 340), (460, 340), (520, 340)],
        "n2 red2 (sq cm/W)": [(400, 360), (460, 360), (520, 360)],
        "n2 blue (sq cm/W)": [(400, 373), (460, 373), (520, 373)],
        "beta red1 (cm/W)": [(400, 393), (460, 393), (520, 393)],
        "beta red2 (cm/W)": [(400, 406), (460, 406), (520, 406)],
        "beta blue (cm/W)": [(400, 420), (460, 420), (520, 420)],
        "Walkoff angles (mrad)": [(400, 440), (460, 440), (520, 440)],
        "Offset in wo dir. (mm)": [(400, 453), (460, 453), (520, 453)],
        "Rad. curv. (mm/air)": [(400, 473), (460, 473), (520, 473)],
        "# of integ/grid points": [(400, 486), (460, 486), (520, 486)],
        "Crystal/grid sizes (mm)": [(400, 500), (460, 500), (520, 500)],
        "Deff (pm/V)": [(400, 520)],
        "Delta k (1/mm)": [(400, 533)],
        "Dist. to image (mm)": [(400, 546)],
        "# time steps": [(400, 566)],
    }

    def interpret_results(self, rows: list[str]) -> dict[str, float | list[float]]:
        """Interpret the results."""
        return {
            "Input peak irradiance (W/sq cm)": [float(i) for i in rows[0].split()[5:]],
            "Input peak fluence (J/sq cm)": [float(i) for i in rows[1].split()[6:]],
            "Input peak powers (W)": [float(i) for i in rows[2].split()[5:]],
            "Output peak fluence (J/sq cm)": [float(i) for i in rows[3].split()[6:]],
            "Output pulse energy (mJ)": [float(i) for i in rows[4].split()[5:]],
            "So (W/sq cm)": float(rows[5].split()[4]),
        }
