
import numpy as np
import time
from typing import cast

import matplotlib.pyplot as plt
import pyautogui as gui

import analysis.modules_JFK as m
from snlohelper import scale, import_snlo_file


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
        titles = "idler (Red1)", "signal (Red2)", "pump (Blue)"
        colors = "red", "green", "blue"
        for i in range(len(ax)):
            m.plot_options(
                fig, ax[i], xlabel="time (ns)", image_width=15, aspect_ratio=3
            )
            ax[i].plot(x_lists[i], y_lists[i], ".", color=colors[i])
            ax[i].set_title(titles[i], color=colors[i])

            x_fit = np.arange(min(x_lists[i]), max(x_lists[i]), 0.1)

            ax[i].plot(x_fit, m.gauss(x_fit, *fits[i]), "-", color=colors[i])
            ax[i].text(0, 0, f"FWHM\n{fwhms[i]:.1f}ns", ha="center", color=colors[i])
            # ax[i].set_xlim([min(x_lists[i]), max(x_lists[i])])
        m.plot_options(
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

    idl = cast(list[float], m.gaussian_fit(np.array([x, y_idl]).T, False)[0])
    sig = cast(list[float], m.gaussian_fit(np.array([x, y_sig]).T, False)[0])
    pmp = cast(list[float], m.gaussian_fit(np.array([x, y_pmp]).T, False)[0])

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
            m.plot_options(
                fig, ax[i], xlabel="detuning (MHz)", image_width=15, aspect_ratio=3
            )
            ax[i].plot(x, y_lists[i], ".", color=colors[i])
            ax[i].set_title(titles[i], color=colors[i])

            x_fit = np.arange(min(x), max(x), 0.1)

            ax[i].plot(x_fit, m.gauss(x_fit, *fits[i]), "-", color=colors[i])
            ax[i].text(0, 0, f"FWHM\n{fwhms[i]:.1f}MHz", ha="center", color=colors[i])
            ax[i].set_xlim([-2 * fwhms[i], 2 * fwhms[i]])
        m.plot_options(
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
