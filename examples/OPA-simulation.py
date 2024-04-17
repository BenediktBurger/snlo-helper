# -*- coding: utf-8 -*-
"""

created on 25.05.2022 by Jan Frederic Kinder
"""

import pickle
import pyautogui as gui
import matplotlib.pyplot as plt
import analysis.modules_JFK as m  # module from NLOQO/EG-Labor/DataAnalysis, check PYTHONPATH in Spyder
import numpy as np
from socket import gethostname
from datetime import datetime  # get current time

import snlohelper as snlo

# imports all of snlohelper, risk of namespace-confusion...
from snlohelper import *

"""define some global filepath variables based upon the computer name:"""


def get_results_path():
    pc_name = gethostname()
    if pc_name == "WhiteShard":
        return "M:/"
    elif pc_name == "POPS":
        return (
            "C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/simulation/"
        )
    elif pc_name == "Myres":
        return "D:/"
    else:
        print("data location not specified, use generic path: M:/")
        return "M:/"


def get_plots_path():
    pc_name = gethostname()
    if pc_name == "WhiteShard":
        return "M:/"
    elif pc_name == "POPS":
        return (
            f"C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/Ausgabe/"
        )
    elif pc_name == "Myres":
        return "D:/"
    else:
        print("data location not specified, use generic path: M:/")
        return "M:/"


results_path = (
    get_results_path()
)  #'C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/simulation/'
plots_path = (
    get_plots_path()
)  # f'C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/Ausgabe/'


# %% tests

# %%% test for display of pulse durations:
id_beam = snlo.import_snlo_file("ID_BEAM.dat")
sig_beam = snlo.import_snlo_file("SIG_BEAM.dat")
pmp_beam = snlo.import_snlo_file("PMP_BEAM.dat")

# fit idler duration
x = 1e9 * id_beam.T[0]  # ns
y = id_beam.T[1] / max(id_beam.T[1])
idl = m.gaussian_fit(np.array([x, y]).T, False)[0]
fwhm_ns_idl = abs(2 * np.sqrt(2 * np.log(2)) * idl[2])
x_lists = [x.copy()]
y_lists = [y.copy()]

# fit signal duration
x = 1e9 * sig_beam.T[0]  # ns
y = sig_beam.T[1] / max(sig_beam.T[1])
sig = m.gaussian_fit(np.array([x, y]).T, False)[0]
fwhm_ns_sig = abs(2 * np.sqrt(2 * np.log(2)) * sig[2])
x_lists.append(x)
y_lists.append(y)

# fit pump duration
x = 1e9 * pmp_beam.T[0]  # ns
y = pmp_beam.T[1] / max(pmp_beam.T[1])
pmp = m.gaussian_fit(np.array([x, y]).T, False)[0]
fwhm_ns_pmp = abs(2 * np.sqrt(2 * np.log(2)) * pmp[2])
x_lists.append(x)
y_lists.append(y)

fig, ax = plt.subplots(1, 3)
fits = idl, sig, pmp
fwhms = fwhm_ns_idl, fwhm_ns_sig, fwhm_ns_pmp
titles = "idler (Red1)", "signal (Red2)", "pump (Blue)"
colors = "red", "green", "blue"
x_fit = np.arange(min(x), max(x), 0.1)

for i in range(len(ax)):
    m.plot_options(fig, ax[i], xlabel="time (ns)", image_width=15, aspect_ratio=3)
    ax[i].plot(x_lists[i], y_lists[i], ".", color=colors[i])
    ax[i].set_title(titles[i], color=colors[i])
    ax[i].plot(x_fit, m.gauss(x_fit, *fits[i]), "-", color=colors[i])
    ax[i].text(0, 0, f"FWHM\n{fwhms[i]:.1f}ns", ha="center", color=colors[i])
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

# %%% screenshot with offset (top left corner)
off = 300, 300
image = gui.screenshot(region=(off[0], off[1], 500, 550))
plt.figure()
plt.imshow(image)
plt.show()

# %%% import SNLO files
# time, power, phase, Mx^2, My^2, Rad Curv x, Rad Curv y, X-tilt, w_x^2, w_y^2
with open("C:/SNLO/ID_BEAM.dat", "r") as f:
    idler = f.read()
with open("C:/SNLO/SIG_BEAM.dat", "r") as f:
    signal = f.read()
with open("C:/SNLO/PMP_BEAM.dat", "r") as f:
    pump = f.read()
print(idler)

# %%% plot spectra
with open("C:/SNLO/OPA2D_SP.dat", "r") as f:
    input = f.readlines()
spectr = []
for i in input:
    element = i.split()
    # pectr.append(float(j) for j in element)
    spectr.append(
        [float(element[0]), float(element[1]), float(element[2]), float(element[3])]
    )
spectr = np.array(spectr.copy())

x = spectr.T[0]  # in MHz
y_idl = spectr.T[1]
y_sig = spectr.T[2]
y_pmp = spectr.T[3]

idl = m.gaussian_fit(np.array([x, y_idl]).T, False)[0]
sig = m.gaussian_fit(np.array([x, y_sig]).T, False)[0]
pmp = m.gaussian_fit(np.array([x, y_pmp]).T, False)[0]

fwhm_idl = 2 * np.sqrt(2 * np.log(2)) * idl[2]
fwhm_sig = 2 * np.sqrt(2 * np.log(2)) * sig[2]
fwhm_pmp = 2 * np.sqrt(2 * np.log(2)) * pmp[2]
print(f"idl: {fwhm_idl:.3f}MHz => {2*np.log(2)/np.pi/fwhm_idl*1e3:.3f}ns")
print(f"sig: {fwhm_sig:.3f}MHz => {2*np.log(2)/np.pi/fwhm_sig*1e3:.3f}ns")
print(f"pmp: {fwhm_pmp:.3f}MHz => {2*np.log(2)/np.pi/fwhm_pmp*1e3:.3f}ns")

fig, ax = plt.subplots()
m.plot_options(fig, ax, xlabel="detuning (MHz)", ylabel="intensity (arb. u.)")
ax.plot(x, y_idl, "r.", label="idler")
ax.plot(x, y_sig, "g.", label="signal")
ax.plot(x, y_pmp, "b.", label="pump")

x_fit = np.arange(min(x), max(x), 1)
ax.plot(x_fit, m.gauss(x_fit, *idl), "r")
ax.plot(x_fit, m.gauss(x_fit, *sig), "g")
ax.plot(x_fit, m.gauss(x_fit, *pmp), "b")

ax.legend(loc="upper left")
plt.tight_layout()
plt.show()


# %%% import simulation files
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA1_pump-dependence.pkl"
result = pickle.load(open("simulation/" + file_name, "rb"))


# %% parameters for OPA1
# %%% calc radius of curvature OPA1
wavelength_nm = 1064.16
ref_index = snlo.n_lnb(wavelength_nm, axis="o")
waist_size_mm = 0.4897
focus_pos_mm = 25  # focus center of crystal
result = snlo.focus(wavelength_nm, ref_index, waist_size_mm, focus_pos_mm)
print(f"radius of curvature: {result[2]:.3f}mm")


# %%% parameters 2D mix LP for OPA1
idler_nm = 3545
signal_nm = 1520.6
pump_nm = 1064.16  # check!
seedpower_w = 0.96
pump_j = 0.000000499
pumpduration_ns = 8
fwhm_seed_mm = 0.65 / 2 * 1.18  # 1/e^2 radius to FWHM
fwhm_pump_mm = 0.83 / 2 * 1.18  # 1/e^2 radius to FWHM

values = [
    [idler_nm, signal_nm, pump_nm],
    [
        snlo.n_lnb(idler_nm, axis="o"),
        snlo.n_lnb(signal_nm, axis="o"),
        snlo.n_lnb(pump_nm, axis="o"),
    ],
    [0, 0, 0],
    [0.01, 0.02, 0.01],  # coating specs input
    [0.01, 0.02, 0.01],  # coating specs output
    [0, 0, 0],  # crystal loss 1/mm
    [seedpower_w, 0.0000000000000001, pump_j],
    [0, 0, pumpduration_ns],
    [fwhm_seed_mm, fwhm_pump_mm, fwhm_pump_mm],
    [1, 1, 1],  # supergaussian coefficient
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],  # walkoff
    [0, 0, 0],  # offset
    [766.97, 4258, 23270],  # radius of curvature
    [50, 32, 32],  # integration points
    [50, 0, 0],  # crystal length, grid, 0: auto: 2.4485x1.9588mm
    [14.77],  # via QPM, LNB_M
    [0],  # delta k
    [1000],  # distance to image
    [25],  # time steps
]
# todo: crystal reflectivities (data sheet)

# %%% init 2D-mix-LP parameters
snlo.open_function("2D-mix-LP")
for index in range(len(values)):
    if len(values[index]) == 1:
        pos = list(snlo.dict_2dmixlp.values())[index][0]
        snlo.set_value(pos, values[index][0])
    else:
        for element in range(len(values[index])):
            snlo.set_value(
                list(snlo.dict_2dmixlp.values())[index][element], values[index][element]
            )


# %% OPA1 pump energy dependence
# start with 1e-5
energies = np.arange(1e-6, 0.7e-3, 1e-5)
print(energies)
print(len(energies))


# %%% run OPA1 pump energy dependence
results = []
for energy in energies:
    set_value(snlo.dict_2dmixlp["Energy/power (J or W)"][2], energy)
    snlo.moveto(*dict_2dmixlp["Accept"])
    # snlo.moveto(780, 800)
    gui.click()
    dict = run_2dmixlp()
    m.set_key(dict, "pump pulse energy (J)", energy)
    dict2 = get_spectr()
    results.append(merge_dict([dict, dict2]))
    snlo.moveto(*dict_2dmixlp["Change Inputs"])
    # (600, 250)
    gui.click()

# %% save OPA1 pump dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA1_pump-dependence.pkl"
pickle.dump(results, open(results_path + file_name, "wb"))


# %%% plot results
file_name = "2022-06-09_OPA1_pump-dependence.pkl"
# results = snlo.merge_dict(pickle.load(open('simulation/' + file_name, 'rb')))
results = snlo.merge_dict(pickle.load(open(results_path + file_name, "rb")))

x = np.array(results["pump pulse energy (J)"]).T[0] * 1e6
y = np.array(results["Output pulse energy (mJ)"]).T[0][0] * 1e3
y2 = np.array(results["duration_idl_ns"]).T[0]
y3 = np.array(results["duration_sig_ns"]).T[0]
y4 = np.array(results["duration_pmp_ns"]).T[0]

fig, [ax1, ax2] = plt.subplots(1, 2)
m.plot_options(
    fig,
    ax1,
    image_width=15,
    aspect_ratio=2,
    xlabel="pump pulse energy ($\mathrm{\mu J}$)",
    ylabel="idler pulse energy ($\mathrm{\mu J}$)",
)
ax1.plot(x, y, "r-", label="idler pulse energy")
ax1.legend(loc="upper left")
ax12 = ax1.twinx()
m.plot_options(fig, ax12, image_width=15, aspect_ratio=2)
ax12.plot(
    x, 1e-6 * y / (1e-9 * y2), "b--", label="single pass gain"
)  # divided by 1W...
ax12.set_ylabel("single pass gain", color="blue")
ax12.legend(loc="lower right")

m.plot_options(
    fig,
    ax2,
    ticks=["auto", 2],
    image_width=15,
    aspect_ratio=2,
    xlabel="pump pulse energy ($\mathrm{\mu J}$)",
    ylabel="idler pulse duration (ns)",
)
ax2.plot(x, y2, "r-", label="idler")
ax2.plot(x, y3, "g--", label="sig")
ax2.plot(x[y4 < 100], y4[y4 < 100], "b-", label="pump")
ax2.set_ylim([0, max(y4[y4 < 100] + 0.5)])
ax2.legend(loc="lower center", ncol=3, frameon=True, handlelength=1.5, mode="expand")
plt.tight_layout()
# m.save_plot('OPA1_pump_sim')
plt.show()

# %% conversion efficiency OPA1
x = np.array(results["pump pulse energy (J)"]).T[0] * 1e6
y = np.array(results["Output pulse energy (mJ)"]).T * 1e3
eff = ((y[0] + y[1]) / x)[0]

fig, ax1 = plt.subplots()
m.plot_options(
    fig,
    ax1,
    image_width=15,
    xlabel="pump pulse energy ($\mathrm{\mu J}$)",
    ylabel="pulse energy ($\mathrm{\mu J}$)",
)
ax1.plot(x, y[0][0], "r-", label="idler pulse energy")
ax1.plot(x, y[1][0], "g-", label="signal pulse energy")
ax1.plot(x, y[2][0], "b-", label="residual pump pulse energy")
ax1.legend(loc="upper left")

ax12 = ax1.twinx()
m.plot_options(fig, ax12, image_width=15, aspect_ratio=2)
ax12.plot(x[eff < 1], eff[eff < 1], "k--", label="conversion efficiency")
ax12.set_ylabel("conversion efficiency")

ax12.legend(loc="lower right")

plt.tight_layout()
# m.save_plot('OPA1_pump_sim')
plt.show()

# %% OPA1 seed power dependence
powers = np.arange(1e-6, 1.5, 20e-3)

# %%% run seed dependence OPA1
set_value(dict_2dmixlp["Energy/power (J or W)"][2], 0.5e-3)
results = []
for power in powers:
    set_value(dict_2dmixlp["Energy/power (J or W)"][0], power)
    gui.moveTo(*coords(780, 800))
    gui.click()
    dict1 = run_2dmixlp()
    m.set_key(dict1, "seed power (W)", power)
    dict2 = get_spectr()
    results.append(merge_dict([dict1, dict2]))
    gui.moveTo(*coords(600, 250))
    gui.click()
# save OPA1 seed dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA1_seed-dependence.pkl"
pickle.dump(results, open("simulation/" + file_name, "wb"))

# %%% import and plot OPA1 pump dependence
file_name = "2022-06-09_OPA1_seed-dependence.pkl"
results = merge_dict(pickle.load(open(results_path + file_name, "rb")))

x = np.array(results["seed power (W)"]).T[0]
y = np.array(results["Output pulse energy (mJ)"]).T[0][0] * 1e3
y2 = np.array(results["duration_idl_ns"]).T[0]

fig, [ax1, ax2] = plt.subplots(1, 2)
m.plot_options(
    fig,
    ax1,
    xlabel="(cw) idler power (W)",
    ylabel="idler pulse energy ($\mathrm{\mu J}$)",
)
ax1.plot(x, y, "-")

m.plot_options(
    fig, ax2, xlabel="(cw) idler power (W)", ylabel="idler pulse duration (ns)"
)
ax2.plot(x, y2, "-")
plt.tight_layout()
# m.save_plot('OPA1_seed_sim')
plt.show()

# %% OPA1: Paper values
pump_energy = 0.5e-3
seed_power = 1
set_value(dict_2dmixlp["Energy/power (J or W)"][2], pump_energy)
set_value(dict_2dmixlp["Energy/power (J or W)"][0], seed_power)
moveto(dict_2dmixlp["Accept"])
gui.click()
dict1 = run_2dmixlp()
m.set_key(dict1, "seed power (W)", seed_power)
m.set_key(dict1, "pump pulse energy (J)", pump_energy)
dict2 = get_spectr()
results = merge_dict([dict1, dict2])
# %% gather OPA1 values
duration_idl_ns = results["duration_idl_ns"][0]
fwhm_idl_MHz = results["fwhm_idl_MHz"][0]
energy_idl_mJ = results["Output pulse energy (mJ)"][0][0]
y = np.array(results["Output pulse energy (mJ)"]) * 1e3
efficiency = (y[0, 0] + y[0, 1]) / y[0, 2]
gain = (1e-3 * energy_idl_mJ) / (1e-9 * duration_idl_ns) / results["seed power (W)"][0]

print(f"idler pulse energy: {energy_idl_mJ * 1e3:.3f}uJ")
print(f"conversion efficiency: {efficiency*1e2:.3f}%")
print(f"single pass gain: {gain:.1f}")
print(f"idler duration:{duration_idl_ns:.3f}ns")
print(f"idler bandwidth: {fwhm_idl_MHz:.3f}MHz")

# %% parameters for OPA2
# %%% calc radius of curvature OPA2 - pump
idler_nm = 3545
wavelength_nm = 1064.16
ref_index = n(pm_theta(idler_nm, wavelength_nm), wavelength_nm, 25)
waist_size_mm = 1.6 / 2 * 1.18  # 1/e^2 radius to FWHM
focus_pos_mm = 15  # focus center of crystal
result = focus(wavelength_nm, ref_index, waist_size_mm, focus_pos_mm)
print(f"radius of curvature: {result[2]:.3f}mm")

# %%% calc radius of curvature OPA2 - idler
wavelength_nm = 3545
ref_index = n_lnb(wavelength_nm, axis="o")
waist_size_mm = 3.9 / 2 * 1.18  # 1/e^2 radius to FWHM
focus_pos_mm = 15  # focus center of crystal
result = focus(wavelength_nm, ref_index, waist_size_mm, focus_pos_mm)
print(f"radius of curvature: {result[2]:.3f}mm")

# %%% calc radius of curvature OPA2 - signal
wavelength_nm = 1520.6
ref_index = n_lnb(wavelength_nm, axis="o")
waist_size_mm = 3.9 / 2 * 1.18  # 1/e^2 radius to FWHM
focus_pos_mm = 15  # focus center of crystal
result = focus(wavelength_nm, ref_index, waist_size_mm, focus_pos_mm)
print(f"radius of curvature: {result[2]:.3f}mm")

# %%% calc pulse duration of the idler seed
file_name = "2022-05-23_OPA1_seed-dependence.pkl"
results = merge_dict(pickle.load(open(results_path + file_name, "rb")))
i = 50
print("pump pulse energy: 0.5mJ")
power = results["seed power (W)"][i][0]
print(f"idler seed power: {power}W")
duration = results["duration_idl_ns"][i][0]
print(f"idler duration: {duration:.3f}ns")
energy = 1e3 * results["Output pulse energy (mJ)"][i][0][0]
print(f"idler pulse energy: {energy:.3f}uJ")

# %%% parameters 2D-mix-LP for OPA2
idler_nm = 3545
signal_nm = 1520.6
pump_nm = 1064.16
seedenergy_j = 44.5e-6  # was 46.9uJ (seed: 1W, pump: 0.5mJ)
pump_j = 23e-3
pulseduration_idler_ns = 6.217  # abgelesen aus seed dep
pumpduration_ns = 8
fwhm_seed_mm = 3.9 / 2 * 1.18  # 1/e^2 radius to FWHM
fwhm_pump_mm = 1.6 / 2 * 1.18  # 1/e^2 radius to FWHM

values = [
    [idler_nm, signal_nm, pump_nm],
    [
        n_lnb(idler_nm, axis="o"),
        n_lnb(signal_nm, axis="o"),
        n(pm_theta(idler_nm, pump_nm), pump_nm, 25),
    ],
    [0, 0, 0],
    [0.05, 0.005, 0.001],  # coating specs input, NC24, NC25
    [0.05, 0.005, 0.001],  # coating specs output
    [0, 0, 0],  # crystal loss 1/mm
    [seedenergy_j, 1e-16, pump_j],
    [pulseduration_idler_ns, 0, pumpduration_ns],
    [fwhm_seed_mm, fwhm_seed_mm, fwhm_pump_mm],
    [1, 1, 1],  # supergaussian coefficient
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 37.14],  # walkoff
    [0, 0, 0],  # offset
    [1631400, 9172700, 525250],  # todo: radius of curvature
    [50, 32, 32],  # integration points
    [30, 8, 8],  # crystal length, grid in mm
    [-4.04],  # via QPM, LNB_M
    [0],  # delta k
    [1000],  # distance to image
    [25],  # time steps
]
# todo: import power time traces and calculate Gaussian FWHM for idler after OPA1 and OPA2-1

# %%% init 2D-mix-LP parameters for OPA2
open_function("2D-mix-LP")
for index in range(len(values)):
    if len(values[index]) == 1:
        pos = list(dict_2dmixlp.values())[index][0]
        set_value(pos, values[index][0])
    else:
        for element in range(len(values[index])):
            set_value(
                list(dict_2dmixlp.values())[index][element], values[index][element]
            )


# %% OPA2 pump energy dependence
# start with 1e-5
energies = np.arange(1e-6, 25e-3, 250e-6)
print(energies)
print(len(energies))
# set seed energy (was 20uJ)
set_value(dict_2dmixlp["Energy/power (J or W)"][0], 4.45e-05)

# %%% run OPA2 pump energy dependence
results = []
for energy in energies:
    set_value(dict_2dmixlp["Energy/power (J or W)"][2], energy)
    gui.moveTo(*coords(780, 800))
    gui.click()
    dict = run_2dmixlp()
    m.set_key(dict, "pump pulse energy (J)", energy)
    dict2 = get_spectr()
    results.append(merge_dict([dict, dict2]))
    gui.moveTo(*coords(600, 250))
    gui.click()

# %% save OPA2 pump dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA2_pump-dependence.pkl"
# pickle.dump(results, open('simulation/' + file_name, 'wb'))
pickle.dump(results, open(results_path + file_name, "wb"))


# %%% plot results
file_name = "2022-06-09_OPA2_pump-dependence.pkl"
# results = merge_dict(pickle.load(open('simulation/' + file_name, 'rb')))
results = merge_dict(pickle.load(open(results_path + file_name, "rb")))


x = np.array(results["pump pulse energy (J)"]).T[0] * 1e3
y = np.array(results["Output pulse energy (mJ)"]).T[0][0]
y2 = np.array(results["duration_idl_ns"]).T[0]

fig, [ax1, ax2] = plt.subplots(1, 2)
m.plot_options(
    fig, ax1, xlabel="pump pulse energy (mJ)", ylabel="idler pulse energy (mJ)"
)
ax1.plot(x, y, "b-")

m.plot_options(
    fig, ax2, xlabel="pump pulse energy (mJ)", ylabel="idler pulse duration (ns)"
)
ax2.plot(x[y2 < 100], y2[y2 < 100], "-")
# ax2.set_ylim([0, 20])
plt.tight_layout()
# m.save_plot('OPA2_pump_sim')
plt.show()

# %% OPA2 seed energy dependence
energies = np.arange(1e-7, 40e-6, 0.5e-6)
print(energies)
print(len(energies))

# %%% run seed dependence OPA2
set_value(dict_2dmixlp["Energy/power (J or W)"][2], 22.8e-3)
results = []
for energy in energies:
    set_value(dict_2dmixlp["Energy/power (J or W)"][0], energy)
    snlo.moveto(*dict_2dmixlp["Accept"])
    # gui.moveTo(*coords(780, 800))
    gui.click()
    dict = run_2dmixlp()
    m.set_key(dict, "seed pulse energy (J)", energy)
    dict2 = get_spectr()
    results.append(merge_dict([dict, dict2]))
    # gui.moveTo(*coords(600, 250))
    snlo.moveto(*dict_2dmixlp["Change Inputs"])
    gui.click()


# save OPA2 seed dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA2_seed-dependence.pkl"
pickle.dump(results, open(results_path + file_name, "wb"))

# %%% import OPA2 seed dependence
file_name = "2022-06-09_OPA2_seed-dependence.pkl"
results = merge_dict(pickle.load(open(results_path + file_name, "rb")))

x = np.array(results["seed pulse energy (J)"]).T[0] * 1e6
y = np.array(results["Output pulse energy (mJ)"]).T[0][0]
y2 = np.array(results["duration_idl_ns"]).T[0]

fig, [ax1, ax2] = plt.subplots(1, 2)
m.plot_options(
    fig,
    ax1,
    xlabel="seed pulse energy ($\mathrm{\mu J}$)",
    ylabel="idler pulse energy (mJ)",
)
ax1.plot(x, y, "b-")

m.plot_options(
    fig,
    ax2,
    xlabel="seed pulse energy ($\mathrm{\mu J}$)",
    ylabel="idler pulse duration (ns)",
)
ax2.plot(x[y2 < 100], y2[y2 < 100], "-")
plt.tight_layout()
# m.save_plot('OPA2_seed_sim')
plt.show()

# %%% init 2D mix LP for second OPA2 crystal
idler_nm = 3545
signal_nm = 1520.6
pump_nm = 1064.16
seedenergy_j = 20e-6
pump_j = 23e-3
pumpduration_ns = 8
fwhm_seed_mm = 3.9 / 2 * 1.18  # 1/e^2 radius to FWHM
fwhm_pump_mm = 1.6 / 2 * 1.18  # 1/e^2 radius to FWHM

values = [
    [idler_nm, signal_nm, pump_nm],
    [
        n_lnb(idler_nm, axis="o"),
        n_lnb(signal_nm, axis="o"),
        n(pm_theta(idler_nm, pump_nm), pump_nm, 25),
    ],
    [0, 0, 0],
    [0.05, 0.005, 0.001],  # coating specs input, NC24, NC25
    [0.05, 0.005, 0.001],  # coating specs output
    [0, 0, 0],
    [seedenergy_j, 1e-16, pump_j],
    [pumpduration_ns, 0, pumpduration_ns],
    [fwhm_seed_mm, fwhm_seed_mm, fwhm_pump_mm],
    [1, 1, 1],  # supergaussian coefficient
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, -37.14],  # walkoff
    [0, 0, 1.123],  # offset
    [1631400, 9172700, 515780],  # todo: radius of curvature
    [50, 32, 32],  # integration points
    [30, 8, 8],  # crystal length, grid
    [-4.04],  # via QPM, LNB_M
    [0],  # delta k
    [1000],  # distance to image
    [25],  # time steps
]
# variables: idler-energy, signal-energy, pump-energy, pulse-duratios (?)

# %%% full input 2D-mix-LP - OPA2
open_function("2D-mix-LP")
for index in range(len(values)):
    if len(values[index]) == 1:
        pos = list(dict_2dmixlp.values())[index][0]
        set_value(pos, values[index][0])
    else:
        for element in range(len(values[index])):
            set_value(
                list(dict_2dmixlp.values())[index][element], values[index][element]
            )

# %% OPA2 pump energy dependence second crystal
energies = np.arange(1e-6, 25e-3, 250e-6)
print(energies)
print(len(energies))
# need pump dependence for first crystal
file_name = "2022-06-15_OPA2_pump-dependence.pkl"
result_xtal1 = pickle.load(open(results_path + file_name, "rb"))

# print(np.array(result_xtal1[0]['Output pulse energy (mJ)']))

# %%% run OPA2 pump energy dependence for the second crystal
results = []
for energy in energies:
    index = list(energies).index(energy)
    pump_energy = result_xtal1[index]["pump pulse energy (J)"][0]
    input_energies = np.array(result_xtal1[index]["Output pulse energy (mJ)"])[0]
    input_durations = (
        result_xtal1[index]["duration_idl_ns"],
        result_xtal1[index]["duration_sig_ns"],
        result_xtal1[index]["duration_pmp_ns"],
    )

    # ignore the rest, if the Gaussian fit failed after the first stage
    if (
        input_durations[0][0] > 100
        or input_durations[1][0] > 100
        or input_durations[2][0] > 100
    ):
        continue

    set_value(dict_2dmixlp["Energy/power (J or W)"][0], 1e-3 * input_energies[0])
    set_value(dict_2dmixlp["Energy/power (J or W)"][1], 1e-3 * input_energies[1])
    set_value(dict_2dmixlp["Energy/power (J or W)"][2], 1e-3 * input_energies[2])

    set_value(dict_2dmixlp["Pulse duration (fwhm ns)"][0], input_durations[0][0])
    set_value(dict_2dmixlp["Pulse duration (fwhm ns)"][1], input_durations[1][0])
    set_value(dict_2dmixlp["Pulse duration (fwhm ns)"][2], input_durations[2][0])

    snlo.moveto(*dict_2dmixlp["Accept"])
    gui.click()
    dict = run_2dmixlp()
    m.set_key(dict, "pump pulse energy (J)", energy)
    m.set_key(dict, "xtal1 pump pulse energy (J)", pump_energy)
    dict2 = get_spectr()
    results.append(merge_dict([dict, dict2]))
    snlo.moveto(*dict_2dmixlp["Change Inputs"])
    gui.click()

# save OPA2 pump dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA2_pump-dependence_xtal2.pkl"
pickle.dump(results, open(results_path + file_name, "wb"))


# %%% plot results OPA2 pump dep
energies = np.arange(1e-6, 25e-3, 250e-6)

file_name = "2022-06-09_OPA2_pump-dependence.pkl"
# results = merge_dict(pickle.load(open('simulation/' + file_name, 'rb')))
results = merge_dict(pickle.load(open(results_path + file_name, "rb")))

file_name = "2022-06-15_OPA2_pump-dependence_xtal2.pkl"
# results2 = merge_dict(pickle.load(open('simulation/' + file_name, 'rb')))
results2 = merge_dict(pickle.load(open(results_path + file_name, "rb")))


x1 = np.array(results["pump pulse energy (J)"]).T[0] * 1e3
y1 = np.array(results["Output pulse energy (mJ)"]).T[0][0]
x2 = np.array(results2["pump pulse energy (J)"]).T[0] * 1e3
y2 = np.array(results2["Output pulse energy (mJ)"]).T[0][0]


fig, [ax1, ax2] = plt.subplots(1, 2)
m.plot_options(
    fig, ax1, xlabel="pump pulse energy (mJ)", ylabel="idler pulse energy (mJ)"
)
ax1.plot(x1, y1, "b--", label="only first crystal")
ax1.plot(x2, y2, "r-", label="both crystals")
ax1.legend(loc="upper left")

y1 = np.array(results["duration_idl_ns"]).T[0]
y2 = np.array(results2["duration_idl_ns"]).T[0]

limit = 10
m.plot_options(
    fig, ax2, xlabel="pump pulse energy (mJ)", ylabel="idler pulse duration (ns)"
)
ax2.plot(x1[y1 < limit], y1[y1 < limit], "b--", label="only first crystal")
ax2.plot(x2[y2 < limit], y2[y2 < limit], "r-", label="both crystals")
ax2.set_ylim([-1, 10])
ax2.legend(loc="upper left")
plt.tight_layout()
# m.save_plot('OPA2_pump_sim_full')
plt.show()

# %% OPA2 seed energy dependence second crystal
energies = np.arange(1e-7, 40e-6, 0.5e-6)
print(energies)
print(len(energies))
# need pump dependence for first crystal
file_name = "2022-06-15_OPA2_seed-dependence.pkl"
# result_xtal1 = pickle.load(open('simulation/' + file_name, 'rb'))
result_xtal1 = pickle.load(open(results_path + file_name, "rb"))

# print(np.array(result_xtal1[0]['Output pulse energy (mJ)']))

# %%% run OPA2 seed energy dependence for the second crystal
results = []
for energy in energies:
    index = list(energies).index(energy)
    seed_energy = result_xtal1[index]["seed pulse energy (J)"][0]
    input_energies = np.array(result_xtal1[index]["Output pulse energy (mJ)"])[0]
    input_durations = (
        result_xtal1[index]["duration_idl_ns"],
        result_xtal1[index]["duration_sig_ns"],
        result_xtal1[index]["duration_pmp_ns"],
    )

    # ignore the rest, if the Gaussian fit failed after the first stage
    if (
        input_durations[0][0] > 100
        or input_durations[1][0] > 100
        or input_durations[2][0] > 100
    ):
        continue

    set_value(dict_2dmixlp["Energy/power (J or W)"][0], 1e-3 * input_energies[0])
    set_value(dict_2dmixlp["Energy/power (J or W)"][1], 1e-3 * input_energies[1])
    set_value(dict_2dmixlp["Energy/power (J or W)"][2], 1e-3 * input_energies[2])

    set_value(dict_2dmixlp["Pulse duration (fwhm ns)"][0], input_durations[0][0])
    set_value(dict_2dmixlp["Pulse duration (fwhm ns)"][1], input_durations[1][0])
    set_value(dict_2dmixlp["Pulse duration (fwhm ns)"][2], input_durations[2][0])
    snlo.moveto(*dict_2dmixlp["Accept"])
    gui.click()
    dict = run_2dmixlp()
    m.set_key(dict, "seed pulse energy (J)", energy)
    m.set_key(dict, "xtal1 seed pulse energy (J)", seed_energy)
    dict2 = get_spectr()
    results.append(merge_dict([dict, dict2]))
    snlo.moveto(*dict_2dmixlp["Change Inputs"])
    gui.click()

# save OPA2 seed dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + "_" + "OPA2_seed-dependence_xtal2.pkl"
# pickle.dump(results, open('simulation/' + file_name, 'wb'))
pickle.dump(results, open(results_path + file_name, "wb"))

# %%% plot results
file_name = "2022-06-09_OPA2_seed-dependence.pkl"
results = merge_dict(pickle.load(open(results_path + file_name, "rb")))

file_name = "2022-06-15_OPA2_seed-dependence_xtal2.pkl"
results2 = merge_dict(pickle.load(open(results_path + file_name, "rb")))

# x = np.array(result['seed pulse energy (J)']).T[0]*1e6
# y1 = np.array(result['Output pulse energy (mJ)']).T[0][0]
# y2 = np.array(result2['Output pulse energy (mJ)']).T[0][0]

x1 = np.array(results["seed pulse energy (J)"]).T[0] * 1e6
y1 = np.array(results["Output pulse energy (mJ)"]).T[0][0]
x2 = np.array(results2["seed pulse energy (J)"]).T[0] * 1e6
y2 = np.array(results2["Output pulse energy (mJ)"]).T[0][0]


fig, [ax1, ax2] = plt.subplots(1, 2)
m.plot_options(
    fig,
    ax1,
    xlabel="seed pulse energy ($\mathrm{\mu J}$)",
    ylabel="idler pulse energy (mJ)",
)
ax1.plot(x1, y1, "b--", label="only first crystal")
ax1.plot(x2, y2, "r-", label="both crystals")
ax1.legend(loc="upper left")

limit = 10
m.plot_options(
    fig,
    ax2,
    xlabel="seed pulse energy ($\mathrm{\mu J}$)",
    ylabel="idler pulse duration (ns)",
)
ax2.plot(x1[y1 < limit], y1[y1 < limit], "b--", label="only first crystal")
ax2.plot(x2[y2 < limit], y2[y2 < limit], "r-", label="both crystals")

ax2.legend(loc="upper left")

plt.tight_layout()
# m.save_plot('OPA2_seed_sim_full', path=plots_path)
plt.show()

# %% conversion efficiency OPA2
file_name = "2022-06-15_OPA2_pump-dependence_xtal2.pkl"
results2 = merge_dict(pickle.load(open(results_path + file_name, "rb")))

x = np.array(results2["pump pulse energy (J)"]).T[0] * 1e3
y = np.array(results2["Output pulse energy (mJ)"]).T
eff = ((y[0] + y[1]) / x)[0]

fig, ax1 = plt.subplots()
m.plot_options(
    fig,
    ax1,
    image_width=15,
    xlabel="pump pulse energy (mJ)",
    ylabel="pulse energy ($\mathrm{\mu J}$)",
)
ax1.plot(x, y[0][0], "r-", label="idler pulse energy")
ax1.plot(x, y[1][0], "g-", label="signal pulse energy")
ax1.plot(x, y[2][0], "b-", label="residual pump pulse energy")
ax1.legend(loc="upper left")

ax12 = ax1.twinx()
m.plot_options(fig, ax12, image_width=15, aspect_ratio=2)
ax12.plot(x[eff < 1], eff[eff < 1], "k--", label="conversion efficiency")
ax12.set_ylabel("conversion efficiency")

ax12.legend(loc="lower right")

plt.tight_layout()
# m.save_plot('OPA1_pump_sim')
plt.show()
