# -*- coding: utf-8 -*-
"""
Created on Thu May 25 13:01:56 2023

@author: moneke
"""

# %% imports

from time import perf_counter

import numpy as np
import matplotlib as plt

from snlohelper import *

# %% Setup


sim = TwoDMixLP()
sim.open()

start = sim.get_configuration()


# %%%

# Parameters
absorption = np.linspace(0, 41e-1, 30)

# Loop
results = []
for a in absorption:
    r = sim.configure_run_read({'Crystal loss (1/mm)': [a, None, None]})
    results.append(r['Output pulse energy (mJ)'][0])
    print(a, results[-1])


# %% Test

interval = 0#.5
s0 = perf_counter()
gui.click(*scale(133,293))
gui.hotkey("ctrl", "home")
gui.hotkey("ctrl", "shiftleft", "shiftright", "end")
# gui.hotkey('ctrl', 'c')

print(perf_counter()-s0)



s0 = perf_counter()
gui.rightClick(*scale(133,293))
gui.press(6 * ['down'])
gui.press('enter')
# gui.hotkey('ctrl', 'c')

print(perf_counter()-s0)



# %%


with gui.hold("shift", interval=interval):
    with gui.hold("ctrl", interval=interval):
        gui.press("end", interval=interval)
# 


#%%
gui.hotkey("shift", "a")


# %%

results = []

#%%

sim.open()

for data in (ags_o, ags_e):
    results.append(sim.configure_run_read(data))



# %%

pe = np.linspace(0, 0.20, 40)
for v in pe:
    results.append(sim.configure_run_read({'Energy/power (J or W)': [None, None, v]})['Output pulse energy (mJ)'])


# %%

plt.figure()
ax = plt.gca()
ax.plot(pe, [r[0] for r in results], label="losless")
ax.plot(pe, [0.00103, 0.00331, 0.00869, 0.0196, 0.0397, 0.074, 0.129, 0.213, 0.333, 0.494, 0.696, 0.934, 1.2, 1.47, 1.74, 2.0, 2.24, 2.46, 2.66, 2.84, 3.0, 3.14, 3.27, 3.4, 3.51, 3.62, 3.72, 3.82, 3.92, 4.03, 4.13, 4.24, 4.36, 4.49, 4.62, 4.77, 4.92, 5.09, 5.27, 5.46], label="absorption")
ax.set_xlabel("Pumpenergie in J")
ax.set_ylabel("MIR-Energie in mJ")
ax.legend()

