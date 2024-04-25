from .main_window import open_function, Functions
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
