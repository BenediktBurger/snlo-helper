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
Example of a simulation using SNLO

A hash followed by two or more percent signs (e.g. "# %%") indicates cells to execute in ipython.

1. Start SNLO (do not move it!)
2. Execute the cells.
   If a cell starts with `alt_tab`, SNLO should be the program run last
"""

# %%
# Imports

import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as cs

from snlohelper.main_window import MainWindow
from snlohelper import utils

# open the class for the main window
mw = MainWindow()


# %%
"Hard facts"
"""
Values which are given by physics or by the whole setup
"""

# Wavelengths etc.
signal_wl = 3534 / 3  # nm == 1178 nm
pump_wl = 532  # nm
temperature = 300  # K

# Result of qmix for the crystal (BBO)
"""
1178.0(o)+  532.0(o)=  366.5(e)
Walkoff [mrad]   =     0.00   0.00  69.90
Phase velocities = c/  1.652  1.674  1.667
Group velocities = c/  1.672  1.722  1.769
GrpDelDisp(fs^2/mm) =   32.7  136.0  229.4
At theta             =   29.8    deg.
Deff                 =  2.03E0   pm/V
S_o × L^2            =  2.35E7   Watt
Crystal ang. tol.×L  =    0.31   mrad°cm
Temperature range×L  =   17.39   K°cm
Mix accpt ang×L =     1.02    0.45 mrad°cm
Mix accpt bw×L  =   310.43  640.98 GHz°cm
"""
upconverted_wl = 366.5  # resulting wavelength
theta = 29.8
Deff = 2.03e0
walkoff = (0, 0, 69.9)  # angles in mrad
length = 12  # mm


# %%%
# calculate the refractive indices

def get_n():
    utils.alt_tab()
    ref = mw.open_refractive_index()
    s, _ = ref.refractive_indices("Ab", Temperature=temperature, theta=theta, Wavelength=signal_wl)
    p, _ = ref.refractive_indices(Wavelength=pump_wl)
    _, u = ref.refractive_indices(Wavelength=upconverted_wl)
    ref.close()
    return (s, p, u)


n = get_n()

# %%%
# Laser system

# fwhm pulse duration in ns
signal_ns = 3.3
pump_ns = 6

# fwhm beam diameter at entry face in mm (for elliptical 1st in walkoff, second orthogonal)
signal_mm = 1.3647e-1
signal_curv_mm = 3.4981e2
pump_mm = "0.914 0.397"
pump_curv_mm = "-1.7e3 -3.34E3"
upconverted_mm = 0.07788
upconverted_curv_mm = 7.4392e2

# grid size: length, width_walkoff, height_orthogonal, all in mm
grid = (length, 2.5, 1)


# %%
"Simulation settings"

signal_photons = 100_000
pump_E = 1e-9  # in J

# Calculate
signal_E = signal_photons * cs.h * cs.c / signal_wl / 1e-9  # in J
walkoff_offset = (0, 0, walkoff[2] * -1e-3 * length / 2)  # to have overlap in the center


# %%%
# Configure SNLO initially

utils.alt_tab()
mix = mw.open_two_d_mix_lp()

# start configuration: set all values in order to have a predefined configuration
mix.configure({
    "Wavelengths (nm)": (signal_wl, pump_wl, upconverted_wl),
    "Indexes of refraction": n,
    "Phases at input (rad)": [0.0, 0.0, 0.0],
    "Input face reflectivity (0-1)": [0.0, 0.0, 0.0],
    "Output face reflectivity (0-1)": [0.0, 0.0, 0.0],
    "Crystal loss (1/mm)": [0.0, 0.0, 0.0],
    "Energy/power (J or W)": (signal_E, pump_E, 0),
    "Pulse duration (fwhm ns)": (signal_ns, pump_ns, 0),
    "Beam diam. (fwhm mm)": (signal_mm, pump_mm, upconverted_mm),
    "Supergaussian coeff.": [1.0, 1.0, 1.0],
    "n2 red1 (sq cm/W)": [0.0, 0.0, 0.0],
    "n2 red2 (sq cm/W)": [0.0, 0.0, 0.0],
    "n2 blue (sq cm/W)": [0.0, 0.0, 0.0],
    "beta red1 (cm/W)": [0.0, 0.0, 0.0],
    "beta red2 (cm/W)": [0.0, 0.0, 0.0],
    "beta blue (cm/W)": [0.0, 0.0, 0.0],
    "Walkoff angles (mrad)": walkoff,
    "Offset in wo dir. (mm)": walkoff_offset,
    "Rad. curv. (mm/air)": (signal_curv_mm, pump_curv_mm, upconverted_curv_mm),
    "# of integ/grid points": [30.0, 32.0, 32.0],
    "Crystal/grid sizes (mm)": grid,
    "Deff (pm/V)": Deff,
    "Delta k (1/mm)": [0.0],
    "Dist. to image (mm)": [0.0],
    "# time steps": [20.0],
})


# %%
# Run simulation

# Parameters
inputs = np.linspace(1e-4, 15e-3, 20, endpoint=False)

utils.alt_tab()
output = []
for i in inputs:
    print(i)
    result = mix.configure_run_read({"Energy/power (J or W)": (None, i, None)})
    output.append(result["Output pulse energy (mJ)"][2])  # type: ignore
utils.alt_tab()
print(output)


# %%%
# Plot most recent values

fig = plt. figure()
ax = plt.gca()
ax.plot(inputs, output, ls=":", marker="+")

ax.set_xlabel("pump energy in mJ")
ax.set_ylabel("upconversion energy in mJ")

plt.show()
