# -*- coding: utf-8 -*-
"""
Helper for SNLO simulations ("autoclicker")

This file clicks automatically on buttons of SNLO program.


created on 25.05.2022 by Jan Frederic Kinder
"""

import logging
import time
import re

import pyautogui as gui
import matplotlib.pyplot as plt
import numpy as np
from pyperclip import paste

import analysis.modules_JFK as m


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


"""
Setup of the screen and scaling.

All positions in code are given on a Full HD (1920 * 1080) screen and dynamically adjusted to the
screen resolution.
"""


def get_screenfactors(standard=[1920, 1080]):
    """Get the scaling factor from Full HD to the current display resolution."""
    width, height = gui.size()
    return standard[0] / width, standard[1] / height


def scale(x: float, y: float = None) -> tuple:
    """Scale coordinates from the definition standard to the current screen."""
    global factors
    if y is None and isinstance(x, (list, tuple)):
        x, y = x
    return x / factors[0], y / factors[1]


def standard_position() -> tuple:
    """Get the mouse position in standard coordinates (x, y)."""
    point = gui.position()
    global factors
    return point.x * factors[0], point.y * factors[1]


"""
Begin of dictionaries/lists etc.
"""


# coordinates of the functions (in FHD standard)
_functions_coord = {
    'Ref. Ind.': [66, 46],
    'Qmix': [66, 66],
    'Bmix': [66, 93],
    'QPM': [66, 120],
    'Opoangles': [66, 146],
    'Ncpm': [66, 173],
    'GVM': [66, 200],
    'PW-mix-LP': [66, 233],
    'PW-mix-SP': [66, 260],
    'PW-mix-BB': [66, 286],
    '2D-mix-LP': [66, 313],
    '2D-mix-SP': [66, 340],
    'PW-cav-LP': [66, 366],
    'PW-OPO-SP': [66, 393],
    'PW-OPO-BB': [66, 420],
    '2D-cav-LP': [66, 446],
    'Focus': [66, 473],
    'Cavity': [66, 500],
}


# coordinates of the Focus-function (in FHD standard)
off = 200, 200
_dict_focus = {
    'Wavelength (nm)': [366, off[1] + 20],
    'Refractive Index': [366, off[1] + 40],
    'Waist size (mm)': [366, off[1] + 60],
    'Face to focus (mm)': [366, off[1] + 90],
    'Dist. to focus (mm)': [366, 300],
    'Rayleigh z in xtal (mm)': [366, 353],
    'Beam size (mm)': [366, 380],
    'Radius of curv. (mm)': [366, 393],
    'Far field ang air (mrad)': [366, 413],
    'fwhm': [219, 216],
    '1e^2': [166, 216]
}


# coordinates of the 2DmixLP-function (in FHD standard)
_configuration_2dmixlp = {
    'Wavelengths (nm)': [[403, 186], [470, 186], [536, 186]],
    'Indexes of refraction': [[403, 200], [470, 200], [536, 200]],
    'Phases at input (rad)': [[403, 213], [470, 213], [536, 213]],
    'Input face reflectivity (0-1)': [[403, 226], [470, 226], [536, 226]],
    'Output face reflectivity (0-1)': [[403, 246], [470, 246], [536, 246]],
    'Crystal loss (1/mm)': [[403, 260], [470, 260], [536, 260]],
    'Energy/power (J or W)': [[416, 280], [483, 280], [550, 280]],
    'Pulse duration (fwhm ns)': [[403, 293], [470, 293], [536, 293]],
    'Beam diam. (fwhm mm)': [[403, 306], [470, 306], [536, 306]],
    'Supergaussian coeff.': [[403, 326], [470, 326], [536, 326]],
    'n2 red1 (sq cm/W)': [[403, 340], [470, 340], [536, 340]],
    'n2 red2 (sq cm/W)': [[403, 360], [470, 360], [536, 360]],
    'n2 blue (sq cm/W)': [[403, 373], [470, 373], [536, 373]],
    'beta red1 (cm/W)': [[403, 393], [470, 393], [536, 393]],
    'beta red2 (cm/W)': [[403, 406], [470, 406], [536, 406]],
    'beta blue (cm/W)': [[403, 420], [470, 420], [536, 420]],
    'Walkoff angles (mrad)': [[403, 440], [470, 440], [536, 440]],
    'Offset in wo dir. (mm)': [[403, 453], [470, 453], [536, 453]],
    'Rad. curv. (mm/air´)': [[403, 473], [470, 473], [536, 473]],
    '# of integ/grid points': [[403, 486], [470, 486], [536, 486]],
    'Crystal/grid sizes (mm)': [[403, 500], [470, 500], [536, 500]],
    'Deff (pm/V)': [[403, 520]],
    'Delta k (1/mm)': [[403, 533]],
    'Dist. to image (mm)': [[403, 546]],
    '# time steps': [[403, 566]],
}


_buttons_2dmixlp = {
    'Accept': [506, 536],
    'Run': [140, 220],
    'Change Inputs': [373, 166],
}


# TODO: remove following three definitions from this file (already in modules_JFK)
def n_lnb(lambda_nm, temp_degc=25, axis='o'):
    """refractive index of 5% MgO doped congruent LNB (supplied by HC Photonics)
    data and functions from Gayer et al. (Appl. Optics, 2008)"""
    if axis == "e":
        a1, a2, a3, a4, a5, a6 = 5.756, 0.0983, 0.2020, 189.32, 12.52, 1.32e-2
        b1, b2, b3, b4 = 2.86e-6, 4.7e-8, 6.113e-8, 1.516e-4
    elif axis == "o":
        a1, a2, a3, a4, a5, a6 = 5.653, 0.1185, 0.2091, 89.61, 10.85, 1.97e-2
        b1, b2, b3, b4 = 7.941e-7, 3.134e-8, -4.641e-9, -2.188e-6
    f = (np.array(temp_degc) - 24.5) * (np.array(temp_degc) + 570.82)
    lambda_um = np.array(lambda_nm) * 1e-3
    # Sellmeier equation for lambda in micrometers!
    return np.sqrt(
        a1 + b1 * f + (a2 + b2 * f) / (lambda_um ** 2 - (a3 + b3 * f) ** 2)
        + (a4 + b4 * f) / (lambda_um ** 2 - a5 ** 2) - a6 * lambda_um ** 2)


def n_bbo(lambda_nm, axis='o'):
    """refractive index of BBO
    data and functions from Zhang et al. (Opt. Comm., 2000)
    => no temperature dependence!"""
    if axis == "o":
        a1, a2, a3, a4, a5, a6 = 2.7359, 0.01878, 0.01822, 0.01471, 0.0006081, 0.00006740
    elif axis == "e":
        a1, a2, a3, a4, a5, a6 = 2.3753, 0.01224, 0.01667, 0.01627, 0.0005716, 0.00006305
    lambda_um = np.array(lambda_nm) * 1e-3
    # Sellmeier equation for lambda in micrometers!
    return np.sqrt(
        a1 + a2 / (lambda_um ** 2 - a3) - a4 * lambda_um ** 2 + a5 * lambda_um ** 4
        - a6 * lambda_um ** 6)


def n(theta, lambda_nm, temp_degc=25, crystal='LNB'):
    """Return the refractive index under propagation with angle of theta with the crystal c-axis."""
    if crystal == 'LNB':
        return (1 / (np.sqrt(
            np.cos(np.deg2rad(np.array(theta))) ** 2
            / n_lnb(np.array(lambda_nm), np.array(temp_degc), 'o') ** 2
            + np.sin(np.deg2rad(np.array(theta))) ** 2
            / n_lnb(np.array(lambda_nm), np.array(temp_degc), 'e') ** 2)))
    elif crystal == 'BBO':
        return (1 / (np.sqrt(
            np.cos(np.deg2rad(np.array(theta))) ** 2
            / n_bbo(np.array(lambda_nm), 'o') ** 2
            + np.sin(np.deg2rad(np.array(theta))) ** 2
            / n_bbo(np.array(lambda_nm), 'e') ** 2)))

    else:
        print('no Sellmeier equation for ' + crystal + '!')


def pm_theta(idler_nm, pump_nm, temp_degc=25, crystal='LNB'):
    """ returns the angle, which provides critical phase matching in MgO:LNB"""
    signal_nm = m.idler2signal(idler_nm, pump_nm)
    if crystal == 'LNB':
        n1 = n_lnb(idler_nm, temp_degc, 'o')
        n2 = n_lnb(signal_nm, temp_degc, 'o')
        n_pump_e = n_lnb(pump_nm, temp_degc, 'e')
        n_pump_o = n_lnb(pump_nm, temp_degc, 'o')
    elif crystal == 'BBO':
        n1 = n_bbo(idler_nm, 'o')
        n2 = n_bbo(signal_nm, 'o')
        n_pump_e = n_bbo(pump_nm, 'e')
        n_pump_o = n_bbo(pump_nm, 'o')
    n_soll = (n1 / idler_nm + n2 / signal_nm) * pump_nm

    return 180 / np.pi * np.arctan(
        n_pump_e / n_pump_o
        * np.sqrt((n_soll ** 2 - n_pump_o ** 2) / (n_pump_e ** 2 - n_soll ** 2)))


def pm_theta_bbo(red1_nm, red2_nm):
    """ returns the angle, which provides critical phase matching in MgO:LNB"""
    blue_nm = 1 / (1 / red1_nm + 1 / red2_nm)
    n1 = n_bbo(red1_nm, 'o')
    n2 = n_bbo(red2_nm, 'e')
    n_blue_e = n_bbo(blue_nm, 'e')
    n_blue_o = n_bbo(blue_nm, 'o')
    n_soll = (n1 / red1_nm + n2 / red2_nm) * blue_nm

    return 180 / np.pi * np.arctan(
        n_blue_e / n_blue_o
        * np.sqrt((n_soll ** 2 - n_blue_o ** 2) / (n_blue_e ** 2 - n_soll ** 2)))


# Helper functions
def get_content(position: tuple) -> str:
    """Get the content of the field at position via double click.

    If there is a "-" in the text, the extraction fails!
    """
    gui.doubleClick(*scale(*position))
    gui.hotkey('ctrl', 'c')
    return paste()


def get_value(position: tuple) -> float:
    """move to position, retrieve value and return float"""
    return float(get_content(position))


def get_content_complete(position: tuple) -> str:
    """Go to position and retrieve the content there, marking all."""
    gui.click(*scale(*position))
    gui.hotkey("ctrl", "home")
    gui.hotkey("ctrl", "shiftleft", "shiftright", "end")  # both shift keys necessary if keylock on.
    gui.hotkey('ctrl', 'c')
    return paste()


def get_value_complete(position: tuple) -> float:
    """moves to position, retrieves value via context menu (slower) and returns float"""
    return float(get_content_complete(position))


def set_value(position: tuple, value) -> None:
    """move to position, insert value as string"""
    gui.doubleClick(*scale(*position))
    gui.press('delete')
    gui.doubleClick()
    gui.write(str(value))


# SNLO calls
def open_function(key: str) -> None:
    """opens function according to key"""
    gui.click(*scale(*_functions_coord[key]))


def focus(wavelength_nm: float, ref_index: float, fwhm_mm: float, focus_pos_mm: float) -> tuple:
    """calls focus function to determine parameters for the radius of curvature.
    inputs: wavelength_nm, ref_index, waist_size_mm (FWHM), focus_pos_mm
    returns: zr, diameter (FWHM), radcurv, angle
    """
    open_function('Focus')
    gui.leftClick(*scale(*_dict_focus['fwhm']))
    set_value(_dict_focus['Wavelength (nm)'], wavelength_nm)
    set_value(_dict_focus['Refractive Index'], ref_index)
    set_value(_dict_focus['Waist size (mm)'], fwhm_mm)
    set_value(_dict_focus['Face to focus (mm)'], focus_pos_mm)
    # Setting 'Dist. to focus (mm)' equal to 'Face to focus (mm)' gives parameters in air at the
    # input face
    set_value(_dict_focus['Dist. to focus (mm)'], focus_pos_mm)
    # readout
    zr = get_value_complete(_dict_focus['Rayleigh z in xtal (mm)'])
    diameter = get_value_complete(_dict_focus['Beam size (mm)'])
    radcurv = get_value_complete(_dict_focus['Radius of curv. (mm)'])
    angle = get_value_complete(_dict_focus['Far field ang air (mrad)'])
    return zr, diameter, radcurv, angle


class TwoDMixLP:
    """The '2D-mix-LP' method."""

    def open(self):
        """Open the function."""
        open_function("2D-mix-LP")

    def accept(self):
        """Click 'Accept'."""
        gui.click(*scale(506, 536))

    def run(self):
        """Click 'Run'."""
        gui.click(*scale(140, 220))

    def change_inputs(self):
        """Click 'Change Inputs'."""
        gui.click(*scale(373, 166))

    def configure(self, data: dict = None):
        """Configure the values and leave the config window open."""
        open_function("2D-mix-LP")
        if data is None:
            return
        for key, value in data.items():
            positions = _configuration_2dmixlp[key]
            for i, val in enumerate(value):
                if val is not None:
                    set_value(positions[i], val)

    def get_configuration(self) -> dict:
        data = {}
        for key, positions in _configuration_2dmixlp.items():
            d = []
            for pos in positions:
                val = get_content_complete(pos)
                try:
                    d.append(float(val))
                except ValueError:
                    d.append(val)
            data[key] = d
        return data

    def run_and_read(self, waiting_time: float = 1, max_tries: int = 10, interval: float = 0.5
                     ) -> dict:
        """Run an analysis and return the result."""
        gui.click(*scale(*_buttons_2dmixlp['Run']))
        time.sleep(waiting_time)

        for _ in range(max_tries):
            entries = get_content_complete((133, 293)).split("\r\n")
            if len(entries) > 3:
                break
            time.sleep(interval)

        # interpret results and save as dictionary:
        return {
            'Input peak irradiance (W/sq cm)': [float(i) for i in entries[0].split()[5:]],
            'Input peak fluence (J/sq cm)': [float(i) for i in entries[1].split()[6:]],
            'Input peak powers (W)': [float(i) for i in entries[2].split()[5:]],
            'Output peak fluence (J/sq cm)': [float(i) for i in entries[3].split()[6:]],
            'Output pulse energy (mJ)': [float(i) for i in entries[4].split()[5:]],
            'So (W/sq cm)': float(entries[5].split()[4])
        }

    def configure_run_read(self, data: dict = None, **kwargs) -> dict:
        """Configure and run an analysis and return the result."""
        self.configure(data)
        self.accept()
        return self.run_and_read(**kwargs)


def import_snlo_file(file_name, file_path='C:/SNLO/'):
    """import a file generated by SNLO, specified by filename and return array (no header)"""
    with open(file_path + file_name, 'r') as f:
        input = f.readlines()
    data = []
    e_numbers = re.compile(r"-*[\d.]*?E-*[+]*\d*")
    r""" Regex
        -*        "-" or nothing
        [\d.]*?   decimal number (0 or more characters)
        -*        "-" or nothing
        [+]*      "+" or nothing
        \d*       decimal number (0 or more characters)
    """
    for i in input:
        temp = []
        # old implementation, suffers from strings without whitespace, e.g.:
        #    '9.206897E-100-1.616264E-2'
        #    element = i.split()
        #    for item in element:
        #        temp.append(float(item))
        new_element = e_numbers.findall(i)
        for item in new_element:
            temp.append(float(item))
        data.append(temp)
    return np.array(data.copy())


def get_spectr(call_function: bool = True, display_results: bool = False) -> dict:
    """imports spectra and power vs. time data for all three fields of the mixing process.
    call_function: for 2D-mix-LP you have to click on 'Spectra' to calculate the spectra.
    display_results: gives plots for spectra and powers
    returns dictionary with bandwidths and durations (given as FWHMs)"""
    if call_function:
        gui.click(*scale(400, 260))
        time.sleep(0.5)

    # detuning [MHz], Red1, Red2, Blue
    spectr = import_snlo_file('OPA2D_SP.dat')
    # time, power, phase, Mx^2, My^2, Rad Curv c, Rad Curv y, X-tilt, w_x^2, w_y^2
    id_beam = import_snlo_file('ID_BEAM.dat')
    sig_beam = import_snlo_file('SIG_BEAM.dat')
    pmp_beam = import_snlo_file('PMP_BEAM.dat')

    # fit idler duration
    x = 1e9 * id_beam.T[0]  # ns
    y = id_beam.T[1]
    idl = m.gaussian_fit(np.array([x, y]).T, False)[0]
    fwhm_ns_idl = abs(2 * np.sqrt(2 * np.log(2)) * idl[2])
    x_lists = [x.copy()]
    y_lists = [y.copy()]

    # fit signal duration
    x = 1e9 * sig_beam.T[0]  # ns
    y = sig_beam.T[1]
    sig = m.gaussian_fit(np.array([x, y]).T, False)[0]
    fwhm_ns_sig = abs(2 * np.sqrt(2 * np.log(2)) * sig[2])
    x_lists.append(x)
    y_lists.append(y)

    # fit pump duration
    x = 1e9 * pmp_beam.T[0]  # ns
    y = pmp_beam.T[1]
    pmp = m.gaussian_fit(np.array([x, y]).T, False)[0]
    fwhm_ns_pmp = abs(2 * np.sqrt(2 * np.log(2)) * pmp[2])
    x_lists.append(x)
    y_lists.append(y)
    fits = idl, sig, pmp
    if display_results:
        # plot pulse durations
        fig, ax = plt.subplots(1, 3)
        fwhms = fwhm_ns_idl, fwhm_ns_sig, fwhm_ns_pmp
        titles = 'idler (Red1)', 'signal (Red2)', 'pump (Blue)'
        colors = 'red', 'green', 'blue'
        for i in range(len(ax)):
            m.plot_options(fig, ax[i], xlabel='time (ns)', image_width=15, aspect_ratio=3)
            ax[i].plot(x_lists[i], y_lists[i], '.', color=colors[i])
            ax[i].set_title(titles[i], color=colors[i])

            x_fit = np.arange(min(x_lists[i]), max(x_lists[i]), 0.1)

            ax[i].plot(x_fit, m.gauss(x_fit, *fits[i]), '-', color=colors[i])
            ax[i].text(0, 0, f'FWHM\n{fwhms[i]:.1f}ns', ha='center', color=colors[i])
            # ax[i].set_xlim([min(x_lists[i]), max(x_lists[i])])
        m.plot_options(fig, ax[0], image_width=15, aspect_ratio=3, xlabel='time (ns)',
                       ylabel='normalized power')
        plt.tight_layout()
        plt.show()

    # fit spectra
    x = spectr.T[0]  # in MHz
    y_idl = spectr.T[1]
    y_sig = spectr.T[2]
    y_pmp = spectr.T[3]

    idl = m.gaussian_fit(np.array([x, y_idl]).T, False)[0]
    sig = m.gaussian_fit(np.array([x, y_sig]).T, False)[0]
    pmp = m.gaussian_fit(np.array([x, y_pmp]).T, False)[0]

    fwhm_spec_idl = abs(2 * np.sqrt(2 * np.log(2)) * idl[2])
    fwhm_spec_sig = abs(2 * np.sqrt(2 * np.log(2)) * sig[2])
    fwhm_spec_pmp = abs(2 * np.sqrt(2 * np.log(2)) * pmp[2])

    y_lists = y_idl, y_sig, y_pmp

    fits = idl, sig, pmp
    if display_results:
        # plot spectra durations
        fig, ax = plt.subplots(1, 3)
        fwhms = fwhm_spec_idl, fwhm_spec_sig, fwhm_spec_pmp
        titles = 'idler (Red1)', 'signal (Red2)', 'pump (Blue)'
        colors = 'red', 'green', 'blue'
        for i in range(len(ax)):
            m.plot_options(fig, ax[i], xlabel='detuning (MHz)', image_width=15, aspect_ratio=3)
            ax[i].plot(x, y_lists[i], '.', color=colors[i])
            ax[i].set_title(titles[i], color=colors[i])

            x_fit = np.arange(min(x), max(x), 0.1)

            ax[i].plot(x_fit, m.gauss(x_fit, *fits[i]), '-', color=colors[i])
            ax[i].text(0, 0, f'FWHM\n{fwhms[i]:.1f}MHz', ha='center', color=colors[i])
            ax[i].set_xlim([-2 * fwhms[i], 2 * fwhms[i]])
        m.plot_options(fig, ax[0], image_width=15, aspect_ratio=3, xlabel='time (ns)',
                       ylabel='normalized power')
        plt.tight_layout()
        plt.show()

    return {
        'fwhm_idl_MHz': fwhm_spec_idl,
        'fwhm_sig_MHz': fwhm_spec_sig,
        'fwhm_pmp_MHz': fwhm_spec_pmp,
        'duration_idl_ns': fwhm_ns_idl,
        'duration_sig_ns': fwhm_ns_sig,
        'duration_pmp_ns': fwhm_ns_pmp
    }


if __name__ == "__main__":
    if len(log.handlers) < 2:
        log.addHandler(logging.StreamHandler())
    log.setLevel(logging.INFO)
    factors = get_screenfactors()
    log.info(f"Setting screenfactors to {factors}.")
