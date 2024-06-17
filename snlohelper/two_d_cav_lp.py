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


class TwoDCavLP(MixMethods):
    """The '2D-cav-LP' method."""

    _function = Functions.TWOD_CAV_LP
    _accept_pos = (480, 537)
    _run_pos = (148, 275)
    _result_pos = (148, 357)
    _change_inputs_pos = (157, 310)
    _close_pos = (480, 135)
    _configuration_pos = {"Wavelengths (nm)": [(330, 151), (397, 151), (464, 151)],
                          "Indexes of refraction": [(330, 167), (397, 167), (464, 167)],
                          "Crystal left reflectivity": [(330, 183), (397, 183), (464, 183)],
                          "Crystal right reflectivity": [(330, 199), (397, 199), (464, 199)],
                          "Crystal loss (per mm)": [(330, 215), (397, 215), (464, 215)],
                          "Enrgy/Pwr left (J/W)": [(330, 231), (397, 231), (464, 231)],
                          "Enrgy/Pwr right (J/W)": [(330, 247), (397, 247)],
                          "Pulse duration (FWHM ns)": [(330, 263), (397, 263), (464, 263)],
                          "Pulse delay (ns)": [(330, 279), (397, 279)],
                          "Beam diameter (FWHM mm)": [(330, 295), (397, 295), (464, 295)],
                          "Supergaussian coefficient": [(330, 311), (397, 311), (464, 311)],
                          "Walk off angle (mard)": [(330, 327), (397, 327), (464, 327)],
                          "Beam offset (mm)": [(397, 343), (464, 343)],
                          "Beam radius of curv. (mm)": [(330, 359), (397, 359), (464, 359)],
                          "Left mirror reflectivity": [(330, 375), (397, 375), (464, 375)],
                          "Right mirror reflectivity": [(330, 391), (397, 391), (464, 391)],
                          "Phase L-C (radians)": [(330, 407), (397, 407), (464, 407)],
                          "Phase C-R (radians)": [(330, 423), (397, 423), (464, 423)],
                          "Phase R-L (radians)": [(330, 439), (397, 439), (464, 439)],
                          "Mirror roc L R (mm)": [(330, 463), (397, 463)],
                          "Dist. L-C C-R R-L (mm)": [(330, 479), (397, 479), (464, 479)],
                          "Grid numbers z x y": [(330, 495), (397, 495), (464, 495)],
                          "Crystal/grid sizes (mm)": [(330, 511), (397, 511), (464, 511)],
                          "Cavity type/inversion": [(330, 527), (397, 527)],
                          "Deff (pm/V)/delta k (1/mm)": [(330, 543), (397, 543)]}

    def interpret_results(self, rows: list[str]) -> dict[str, float | list[float]]:
        """Interpret the results."""
        print(rows)
        return {
            "Right input (W W -)": [float(i) for i in rows[0].split()[6:]],
            "Left input (W W J)": [float(i) for i in rows[1].split()[6:]],
            "Left output energy (J)": [float(i) for i in rows[2].split()[5:]],
            "Right output energy (J)": [float(i) for i in rows[3].split()[5:]],
            "So (W/sq cm)": float(rows[4].split()[4]),
        }
