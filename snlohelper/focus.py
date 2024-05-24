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

from typing import Optional

from .base_function import BaseFunction
from .functions import open_function, Functions
from .utils import Point, gui, scale, set_value, get_value_complete


# coordinates of the Focus-function (in FHD standard)
_dict_focus: dict[str, Point] = {
    "Wavelength (nm)": (366, 220),
    "Refractive Index": (366, 240),
    "Waist size (mm)": (366, 260),
    "Face to focus (mm)": (366, 290),
    "Dist. to focus (mm)": (366, 300),
    "Rayleigh z in xtal (mm)": (366, 353),
    "Beam size (mm)": (366, 380),
    "Radius of curv. (mm)": (366, 393),
    "Far field ang air (mrad)": (366, 413),
    "fwhm": (219, 216),
    "1e^2": (166, 216),
}


def focus(
    wavelength_nm: float, ref_index: float, fwhm_mm: float, focus_pos_mm: float
) -> tuple[float, float, float, float]:
    """Call 'focus' function to determine parameters for the radius of curvature.

    inputs: wavelength_nm, ref_index, waist_size_mm (FWHM), focus_pos_mm
    return: zr, diameter (FWHM), radcurv, angle
    """
    open_function(Functions.FOCUS)
    gui.leftClick(*scale(*_dict_focus["fwhm"]))
    set_value(_dict_focus["Wavelength (nm)"], wavelength_nm)
    set_value(_dict_focus["Refractive Index"], ref_index)
    set_value(_dict_focus["Waist size (mm)"], fwhm_mm)
    set_value(_dict_focus["Face to focus (mm)"], focus_pos_mm)
    # Setting 'Dist. to focus (mm)' equal to 'Face to focus (mm)' gives parameters in air at the
    # input face
    set_value(_dict_focus["Dist. to focus (mm)"], focus_pos_mm)
    # readout
    zr = get_value_complete(_dict_focus["Rayleigh z in xtal (mm)"])
    diameter = get_value_complete(_dict_focus["Beam size (mm)"])
    radcurv = get_value_complete(_dict_focus["Radius of curv. (mm)"])
    angle = get_value_complete(_dict_focus["Far field ang air (mrad)"])
    return zr, diameter, radcurv, angle


class Focus(BaseFunction):
    _function = Functions.FOCUS

    def __init__(self) -> None:
        super().__init__()
        self._configuration_pos = {key: [value] for key, value in _dict_focus.items()}

    def read_results(self) -> list[str]:
        return super().read_results()

    def focus(
        self,
        wavelength_nm: Optional[float] = None,
        ref_index: Optional[float] = None,
        fwhm_mm: Optional[float] = None,
        focus_pos_mm: Optional[float] = None,
    ) -> tuple[float, float, float, float]:
        self.configure(
            {
                "Wavelength (nm)": wavelength_nm,
                "Refractive Index": ref_index,
                "Waist size (mm)": fwhm_mm,
                # Set face to focus and dist to focus to same value gives values in air at face
                "Face to focus (mm)": focus_pos_mm,
                "Dist. to focus (mm)": focus_pos_mm,
            }
        )
        zr = get_value_complete(_dict_focus["Rayleigh z in xtal (mm)"])
        diameter = get_value_complete(_dict_focus["Beam size (mm)"])
        radcurv = get_value_complete(_dict_focus["Radius of curv. (mm)"])
        angle = get_value_complete(_dict_focus["Far field ang air (mrad)"])
        return zr, diameter, radcurv, angle
