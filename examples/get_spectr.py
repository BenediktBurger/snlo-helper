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

"""
Example on how to use the SNLO data files.
"""


import numpy as np
import time
from typing import cast

import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import pyautogui as gui
from scipy import constants as cs
from scipy.optimize import curve_fit

from snlohelper.utils import scale
from snlohelper.import_snlo_file import import_snlo_file


def gauss(x, x0, a, sigma):
    """Gaussian function"""
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def plotdata(data, xScale=1, yScale=1):
    """Returns the x and y components of a two dimensional list as individual lists, e.g., for
    plotting. Optional linear scale factors as additional commands"""
    xValues = []
    yValues = []
    for i in range(len(data)):
        xValues.append(xScale * data[i][0])
        yValues.append(yScale * data[i][1])
    return xValues, yValues


def gaussian_fit(data, print_output=False):
    """performs Gaussian fit (position, amplitude, standard deviation), returns popt, sdev, serr,
    pcov"""
    # arguments of gauss-function: gauss(x, x0, a, sigma)
    x, y = plotdata(data)

    # find peak position
    peak_pos = x[list(y).index(max(y))]

    try:
        popt, pcov = curve_fit(gauss, x, y, p0=[peak_pos, 1, 1])
    except RuntimeError:
        print("fit failed!")
        popt, pcov = [0, 0, 0], np.zeros((3, 3)).tolist()

    # covariance matrix: diagonal elements are the variances, hence, the square root is the
    # standard deviation
    sdev = np.sqrt(abs(pcov.diagonal()).tolist())

    # standard errors are sd/sqrt(n) with the sample size n
    serr = sdev / (np.sqrt(len(data)))

    return popt, sdev, serr, pcov


def plot_options(
    fig,
    ax,
    xlabel=None,
    ylabel=None,
    font_size=11,
    ticks=["auto", "auto"],
    image_width=10,
    aspect_ratio=cs.golden,
    dpi=200,
):
    """
    sets plot options just like in Mathematica
    :param fig: figure object from pyplot (necessary)
    :param ax: axes object from pyplot (necessary)
    :param xlabel: x-axis label (string or None)
    :param ylabel: y-axis label (string or None)
    :param font_size: font size (number, standard=11)
    :param ticks: custom or auto ticks (list of x and y: 'auto' or major tick increment)
    :param image_width: width of the image in cm (number, standard=10)
    :param aspect_ratio: aspect ratio of the image (number, standard=golden ratio)

    Parameters
    ----------
    dpi : dpi for displaying in jupyterlab (standard = 200)
    """
    # set size and aspect ratio
    fig.set_size_inches(image_width / 2.54, image_width / 2.54 / aspect_ratio)

    fig = plt.gcf()
    plt.rcParams["font.family"] = "Arial"
    fig.set_dpi(dpi)  # only for display in jupyterlab!
    fig.patch.set_facecolor("white")  # type: ignore

    # plt.style.use('classic')
    ax.tick_params(
        axis="both", which="major", labelsize=font_size, right=True, top=True, direction="in"
    )
    ax.tick_params(
        axis="both", which="minor", labelsize=font_size - 2, right=True, top=True, direction="in"
    )

    # custom major ticks
    if ticks[0] == "auto":
        ax.xaxis.set_major_locator(tic.AutoLocator())
    else:
        ax.xaxis.set_major_locator(tic.MultipleLocator(ticks[0]))
    if ticks[1] == "auto":
        ax.yaxis.set_major_locator(tic.AutoLocator())
    else:
        ax.yaxis.set_major_locator(tic.MultipleLocator(ticks[1]))

    # activate automatic minor ticks
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator())

    # changes fontsize of the labels
    ax.set_xlabel(xlabel, color="black", fontsize=font_size)
    ax.set_ylabel(ylabel, color="black", fontsize=font_size)

    # reduce tick lengths
    ax.tick_params(axis="both", which="minor", length=2)
    ax.tick_params(axis="both", which="major", length=3)


def get_spectr(
    call_function: bool = True, display_results: bool = False
) -> dict[str, float]:
    """imports spectra and power vs. time data for all three fields of the mixing process.
    call_function: for 2D-mix-LP you have to click on 'Spectra' to calculate the spectra.
    display_results: gives plots for spectra and powers
    returns dictionary with bandwidths and durations (given as FWHMs)"""
    if call_function:
        gui.click(*scale(400, 260))
        time.sleep(0.5)

    # detuning [MHz], Red1, Red2, Blue
    spectr = import_snlo_file("OPA2D_SP.dat")
    # time, power, phase, Mx^2, My^2, Rad Curv c, Rad Curv y, X-tilt, w_x^2, w_y^2
    id_beam = import_snlo_file("ID_BEAM.dat")
    sig_beam = import_snlo_file("SIG_BEAM.dat")
    pmp_beam = import_snlo_file("PMP_BEAM.dat")

    # fit idler duration
    x = 1e9 * id_beam.T[0]  # ns
    y = id_beam.T[1]
    idl = gaussian_fit(np.array([x, y]).T, False)[0]
    fwhm_ns_idl = abs(2 * np.sqrt(2 * np.log(2)) * idl[2])
    x_lists = [x.copy()]
    y_lists = [y.copy()]

    # fit signal duration
    x = 1e9 * sig_beam.T[0]  # ns
    y = sig_beam.T[1]
    sig = gaussian_fit(np.array([x, y]).T, False)[0]
    fwhm_ns_sig = abs(2 * np.sqrt(2 * np.log(2)) * sig[2])
    x_lists.append(x)
    y_lists.append(y)

    # fit pump duration
    x = 1e9 * pmp_beam.T[0]  # ns
    y = pmp_beam.T[1]
    pmp = gaussian_fit(np.array([x, y]).T, False)[0]
    fwhm_ns_pmp = abs(2 * np.sqrt(2 * np.log(2)) * pmp[2])
    x_lists.append(x)
    y_lists.append(y)
    fits = idl, sig, pmp
    if display_results:
        # plot pulse durations
        fig, ax = plt.subplots(1, 3)
        fwhms = fwhm_ns_idl, fwhm_ns_sig, fwhm_ns_pmp
        titles = "idler (Red1)", "signal (Red2)", "pump (Blue)"
        colors = "red", "green", "blue"
        for i in range(len(ax)):
            plot_options(
                fig, ax[i], xlabel="time (ns)", image_width=15, aspect_ratio=3
            )
            ax[i].plot(x_lists[i], y_lists[i], ".", color=colors[i])
            ax[i].set_title(titles[i], color=colors[i])

            x_fit = np.arange(min(x_lists[i]), max(x_lists[i]), 0.1)

            ax[i].plot(x_fit, gauss(x_fit, *fits[i]), "-", color=colors[i])
            ax[i].text(0, 0, f"FWHM\n{fwhms[i]:.1f}ns", ha="center", color=colors[i])
            # ax[i].set_xlim([min(x_lists[i]), max(x_lists[i])])
        plot_options(
            fig,
            ax[0],
            image_width=15,
            aspect_ratio=3,
            xlabel="time (ns)",
            ylabel="normalized power",
        )
        plt.tight_layout()
        plt.show()

    # fit spectra
    x = spectr.T[0]  # in MHz
    y_idl = spectr.T[1]
    y_sig = spectr.T[2]
    y_pmp = spectr.T[3]

    idl = cast(list[float], gaussian_fit(np.array([x, y_idl]).T, False)[0])
    sig = cast(list[float], gaussian_fit(np.array([x, y_sig]).T, False)[0])
    pmp = cast(list[float], gaussian_fit(np.array([x, y_pmp]).T, False)[0])

    fwhm_spec_idl = abs(2 * np.sqrt(2 * np.log(2)) * idl[2])
    fwhm_spec_sig = abs(2 * np.sqrt(2 * np.log(2)) * sig[2])
    fwhm_spec_pmp = abs(2 * np.sqrt(2 * np.log(2)) * pmp[2])

    y_lists = y_idl, y_sig, y_pmp

    fits = idl, sig, pmp
    if display_results:
        # plot spectra durations
        fig, ax = plt.subplots(1, 3)
        fwhms = fwhm_spec_idl, fwhm_spec_sig, fwhm_spec_pmp
        titles = "idler (Red1)", "signal (Red2)", "pump (Blue)"
        colors = "red", "green", "blue"
        for i in range(len(ax)):
            plot_options(
                fig, ax[i], xlabel="detuning (MHz)", image_width=15, aspect_ratio=3
            )
            ax[i].plot(x, y_lists[i], ".", color=colors[i])
            ax[i].set_title(titles[i], color=colors[i])

            x_fit = np.arange(min(x), max(x), 0.1)

            ax[i].plot(x_fit, gauss(x_fit, *fits[i]), "-", color=colors[i])
            ax[i].text(0, 0, f"FWHM\n{fwhms[i]:.1f}MHz", ha="center", color=colors[i])
            ax[i].set_xlim([-2 * fwhms[i], 2 * fwhms[i]])
        plot_options(
            fig,
            ax[0],
            image_width=15,
            aspect_ratio=3,
            xlabel="time (ns)",
            ylabel="normalized power",
        )
        plt.tight_layout()
        plt.show()

    return {
        "fwhm_idl_MHz": fwhm_spec_idl,
        "fwhm_sig_MHz": fwhm_spec_sig,
        "fwhm_pmp_MHz": fwhm_spec_pmp,
        "duration_idl_ns": fwhm_ns_idl,
        "duration_sig_ns": fwhm_ns_sig,
        "duration_pmp_ns": fwhm_ns_pmp,
    }
