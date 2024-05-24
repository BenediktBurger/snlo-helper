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


class TwoDMixSP(MixMethods):
    """The '2D-mix-SP' method."""

    _function = Functions.TWOD_MIX_SP
    _accept_pos = (506, 600)
    _run_pos = (140, 200)
    _close_pos = (540, 140)
    _change_inputs_pos = (150, 266)
    _result_pos = (133, 293)

    # coordinates of the 2DmixLP-function (in FHD standard)
    _configuration_pos = {
        "Wavelengths (nm)": [(400, 186), (460, 186), (520, 186)],
        "Indexes of refraction": [(400, 200), (460, 200), (520, 200)],
        "Group velocity index": [(400, 213), (460, 213), (520, 213)],
        "Group delay dispersion": [(400, 226), (460, 226), (520, 226)],
        "Phase (radians)": [(400, 246), (460, 246), (520, 246)],
        "Input face reflectivity": [(400, 260), (460, 260), (520, 260)],
        "Output face reflectivity": [(416, 280), (483, 280), (550, 280)],
        "Crystal absorption (per mm)": [(400, 293), (460, 293), (520, 293)],
        "n2 red1 (sq cm/W)": [(400, 306), (460, 306), (520, 306)],
        "n2 red2 (sq cm/W)": [(400, 326), (460, 326), (520, 326)],
        "n2 blue (sq cm/W)": [(400, 340), (460, 340), (520, 340)],
        "beta red1 (cm/W)": [(400, 360), (460, 360), (520, 360)],
        "beta red2 (cm/W)": [(400, 373), (460, 373), (520, 373)],
        "beta blue (cm/W)": [(400, 393), (460, 393), (520, 393)],
        "Pulse energy (Joules)": [(400, 406), (460, 406), (520, 406)],
        "Pulse duration (ps)": [(400, 420), (460, 420), (520, 420)],
        "Pulse Delay (ps)": [(400, 440), (460, 440), (520, 440)],
        "Pulse chirp (THz/ps)": [(400, 453), (460, 453), (520, 453)],
        "Beam diameter (mm)": [(400, 473), (460, 473), (520, 473)],
        "Supergaussian coefficient": [(400, 486), (460, 486), (520, 486)],
        "Walkoff angle (mrad)": [(400, 500), (460, 500), (520, 500)],
        "Beam position (mm)": [(400, 520), (460, 520), (520, 520)],
        "Radius of curvature (mm)": [(400, 533), (460, 533), (460, 533)],
        "Number t,x,y points": [(400, 546), (460, 546), (520, 546)],
        "Size of crystal/grid (mm)": [(400, 566), (460, 566), (520, 566)],
        "deff (pm/V)": [(400, 580)],
        "delta k (1/mm)": [(400, 596)],
        "Number of z steps": [(400, 612)],
        "Dist. to detector (mm)": [(400, 628)]
    }
