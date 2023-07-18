# -*- coding: utf-8 -*-
"""

created on 25.05.2022 by Jan Frederic Kinder
"""
import time
import pickle
import pyautogui as gui
import matplotlib.pyplot as plt
import modules_JFK as m  # module from NLOQO/EG-Labor/DataAnalysis, check PYTHONPATH in Spyder
import numpy as np
import scipy
from pyperclip import paste
from socket import gethostname
from collections import defaultdict
from datetime import datetime  # get current time

import snlohelper as snlo
# imports all of snlohelper, risk of namespace-confusion...
from snlohelper import *

"""define some global filepath variables based upon the computer name:"""
def get_results_path():
    pc_name = gethostname()
    if pc_name == 'WhiteShard':
        return 'M:/'
    elif pc_name == 'POPS':
        return 'C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/simulation/'
    elif pc_name == 'Myres':
        return 'D:/'
    else:
        print('data location not specified, use generic path: M:/')
        return 'M:/'
    
def get_plots_path():
    pc_name = gethostname()
    if pc_name == 'WhiteShard':
        return 'M:/'
    elif pc_name == 'POPS':
        return f'C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/Ausgabe/'
    elif pc_name == 'Myres':
        return 'D:/'
    else:
        print('data location not specified, use generic path: M:/')
        return 'M:/'
results_path = get_results_path()#'C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/simulation/'
plots_path = get_plots_path()#f'C:/Users/kinder.NLOQO/HESSENBOX-DA/OPA-Paper/analysis (python)/Ausgabe/'


#%% parameters for OPA1
#%%% calc radius of curvature: Red1 (horizontal)
wavelength_nm = 1064
ref_index = snlo.n_bbo(wavelength_nm, axis='o')
fwhm_mm = 1.11
focus_pos_mm = 6  # focus center of crystal
result = snlo.focus(wavelength_nm, ref_index, fwhm_mm, focus_pos_mm)
print(f'Red1 ({wavelength_nm}nm): radius of curvature: {result[2]:.3f} mm')

#%%% calc radius of curvature: Red1 (vertical)
wavelength_nm = 1064
ref_index = snlo.n_bbo(wavelength_nm, axis='o')
fwhm_mm = 1.48
focus_pos_mm = 6  # focus center of crystal
result = snlo.focus(wavelength_nm, ref_index, fwhm_mm, focus_pos_mm)
print(f'Red1 ({wavelength_nm}nm): radius of curvature: {result[2]:.3f} mm')

#%%% calc radius of curvature: Red2 (horizontal)
wavelength_nm = 1417
ref_index = snlo.n_bbo(wavelength_nm, axis='o')
fwhm_mm = 0.153
focus_pos_mm = 6  # focus center of crystal
result = snlo.focus(wavelength_nm, ref_index, fwhm_mm, focus_pos_mm)
print(f'Red2 ({wavelength_nm}nm): radius of curvature: {result[2]:.3f} mm')

#%%% calc radius of curvature: Red2 (vertical)
wavelength_nm = 1417
ref_index = snlo.n_bbo(wavelength_nm, axis='o')
fwhm_mm = 0.151
focus_pos_mm = 6  # focus center of crystal
result = snlo.focus(wavelength_nm, ref_index, fwhm_mm, focus_pos_mm)
print(f'Red2 ({wavelength_nm}nm): radius of curvature: {result[2]:.3f} mm')

#%%% calc radius of curvature: Blue
wavelength_nm = 608
ref_index = snlo.n_bbo(wavelength_nm, axis='o')
fwhm_mm = 0.15
focus_pos_mm = 6  # focus center of crystal
result = snlo.focus(wavelength_nm, ref_index, fwhm_mm, focus_pos_mm)
print(f'Blue ({wavelength_nm}nm): radius of curvature: {result[2]:.3f} mm')

#%%% parameters 2D mix LP for OPA1
red1_nm = 1064
red2_nm = 1417
blue_nm = 1/(1/red1_nm + 1/red2_nm)
theta = 28.2  # from QMIX, SFG pm calculation currently broken...
seedpower_w = 70e-6
pump_j = 9.16e-3
pumpduration_ns = 8

values = [
    [red1_nm, red2_nm, blue_nm],
    [snlo.n_bbo(red1_nm, axis='o'), snlo.n(theta, red2_nm, crystal='BBO'), snlo.n(theta, blue_nm, crystal='BBO')],
    [0, 0, 0],  # phases at input
    [0, 0, 0],  # coating specs input
    [0, 0, 0],  # coating specs output
    [0, 0, 0],  # crystal loss 1/mm
    [pump_j, seedpower_w, 0],
    [8, 0, 0],
    [[1.11, 1.48], [0.153, 0.151], 0.15],
    [1, 1, 1],  # supergaussian coefficient
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 62.92, 63.64],  # walkoff form QMIX
    [0, 0, 0],  # offset
    [[1898700, 6001000], [388.73, 368.99], 1959.4],  # radius of curvature
    [30, 32, 32],  # integration points
    [12, 5.55, 5.92], # crystal length, grid, 0: auto: 2.4485x1.9588mm
    [1.55],  # via QPM, LNB_M
    [0],  # delta k
    [0],  # distance to image
    [20]  # time steps
]

#%%% init 2D-mix-LP parameters
snlo.open_function('2D-mix-LP')
for index in range(len(values)):
    if len(values[index])==1:
        pos = list(snlo.dict_2dmixlp.values())[index][0]
        snlo.set_value(pos, values[index][0])
    else:
        for element in range(len(values[index])):
            # if there are different values for horizontal and vertical
            if type(values[index][element])==list:
                value = str(values[index][element][0])+' '+str(values[index][element][1])
                gui.moveTo(*coords(*list(snlo.dict_2dmixlp.values())[index][element]))
                gui.doubleClick()
                gui.press('delete')
                gui.doubleClick()
                gui.write(value)
            else:
                snlo.set_value(list(snlo.dict_2dmixlp.values())[index][element], values[index][element])


#%% OPA1 pump energy dependence
# start with 1e-5
energies = np.arange(1e-6,0.7e-3,1e-5)
print(energies)
print(len(energies))


#%%% run OPA1 pump energy dependence
results = []
for energy in energies:
    set_value(snlo.dict_2dmixlp['Energy/power (J or W)'][2], energy)
    snlo.moveto(*dict_2dmixlp['Accept'])
    #snlo.moveto(780, 800)
    gui.click()
    dict = run_2dmixlp()
    m.set_key(dict, 'pump pulse energy (J)', energy)
    dict2 = get_spectr()
    results.append(merge_dict([dict, dict2]))
    snlo.moveto(*dict_2dmixlp['Change Inputs'])
        #(600, 250)
    gui.click()

#%% save OPA1 pump dependence
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + '_' + 'OPA1_pump-dependence.pkl'
pickle.dump(results, open(results_path + file_name, 'wb'))


#%%% plot results
file_name = '2022-06-09_OPA1_pump-dependence.pkl'
#results = snlo.merge_dict(pickle.load(open('simulation/' + file_name, 'rb')))
results = snlo.merge_dict(pickle.load(open(results_path + file_name, 'rb')))

x = np.array(results['pump pulse energy (J)']).T[0]*1e6
y = np.array(results['Output pulse energy (mJ)']).T[0][0]*1e3
y2 = np.array(results['duration_idl_ns']).T[0]
y3 = np.array(results['duration_sig_ns']).T[0]
y4 = np.array(results['duration_pmp_ns']).T[0]

fig, [ax1, ax2] = plt.subplots(1,2)
m.plot_options(fig, ax1, image_width=15, aspect_ratio=2, xlabel='pump pulse energy ($\mathrm{\mu J}$)', ylabel='idler pulse energy ($\mathrm{\mu J}$)')
ax1.plot(x, y, 'r-', label='idler pulse energy')
ax1.legend(loc='upper left')
ax12 = ax1.twinx()
m.plot_options(fig, ax12, image_width=15, aspect_ratio=2)
ax12.plot(x, 1e-6*y/(1e-9*y2), 'b--', label='single pass gain')  # divided by 1W...
ax12.set_ylabel('single pass gain', color="blue")
ax12.legend(loc='lower right')

m.plot_options(fig, ax2, ticks=['auto', 2], image_width=15, aspect_ratio=2, xlabel='pump pulse energy ($\mathrm{\mu J}$)',
               ylabel='idler pulse duration (ns)')
ax2.plot(x, y2, 'r-', label='idler')
ax2.plot(x, y3, 'g--', label='sig')
ax2.plot(x[y4<100], y4[y4<100], 'b-', label='pump')
ax2.set_ylim([0, max(y4[y4<100]+0.5)])
ax2.legend(loc='lower center', ncol=3, frameon=True, handlelength=1.5, mode="expand")
plt.tight_layout()
#m.save_plot('OPA1_pump_sim')
plt.show()

#%% conversion efficiency OPA1
x = np.array(results['pump pulse energy (J)']).T[0]*1e6
y = np.array(results['Output pulse energy (mJ)']).T*1e3
eff = ((y[0]+y[1])/x)[0]

fig, ax1 = plt.subplots()
m.plot_options(fig, ax1, image_width=15, xlabel='pump pulse energy ($\mathrm{\mu J}$)', ylabel='pulse energy ($\mathrm{\mu J}$)')
ax1.plot(x, y[0][0], 'r-', label='idler pulse energy')
ax1.plot(x, y[1][0], 'g-', label='signal pulse energy')
ax1.plot(x, y[2][0], 'b-', label='residual pump pulse energy')
ax1.legend(loc='upper left')

ax12 = ax1.twinx()
m.plot_options(fig, ax12, image_width=15, aspect_ratio=2)
ax12.plot(x[eff<1], eff[eff<1], 'k--', label='conversion efficiency')
ax12.set_ylabel('conversion efficiency')

ax12.legend(loc='lower right')

plt.tight_layout()
#m.save_plot('OPA1_pump_sim')
plt.show()

#%% seed power dependence
powers1 = np.arange(10e-6, 100e-6, 5e-6)
powers2 = np.array([1e-19, 1e-18, 1e-17, 1e-16, 1e-15, 1e-14, 1e-13, 1e-12, 1e-11, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6])
powers = m.flatten([powers1, powers2])

#%%% run seed dependence
set_value(dict_2dmixlp['Energy/power (J or W)'][0], pump_j)
results = []
for power in powers:
    set_value(dict_2dmixlp['Energy/power (J or W)'][1], power)
    gui.moveTo(*coords(780, 800))
    gui.click()
    dict1 = run_2dmixlp()
    m.set_key(dict1, 'seed power (W)', power)
    dict2 = get_spectr()
    results.append(merge_dict([dict1, dict2]))
    gui.moveTo(*coords(600, 250))
    gui.click()

# save OPA1 seed dependence
#%%
now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + '_' + 'upconversion_seed-dependence.pkl'
pickle.dump(results, open('results/'+file_name, 'wb'))

#%%% import and plot seed dependence
file_name = '2022-08-02_upconversion_seed-dependence.pkl'
results = merge_dict(pickle.load(open('results/'+file_name, 'rb')))

x = np.array(results['seed power (W)']).T[0] * 1e6
y1 = np.array(results['Output pulse energy (mJ)']).T[1][0] * 1e6
y2 = np.array(results['Output pulse energy (mJ)']).T[2][0] * 1e6

fig, ax1 = plt.subplots()
m.plot_options(fig, ax1, xlabel='(cw) seed power ($\mu$W)', ylabel='idler pulse energy ($\mathrm{\mu J}$)')
ax1.plot(x, y1, '-', label='seed')
ax1.plot(x, y2, '-', label='SFM')
ax1.legend()
#m.plot_options(fig, ax2, xlabel='(cw) idler power (W)',ylabel='idler pulse duration (ns)')
#ax2.plot(x, y2, '-')
plt.tight_layout()
# m.save_plot('OPA1_seed_sim')
plt.show()

#%% import and plot seed dependence
file_name = '2022-08-02_upconversion_seed-dependence.pkl'
results = merge_dict(pickle.load(open('results/'+file_name, 'rb')))
h = scipy.constants.h
c = scipy.constants.c
seed_nm = 1417
pump_nm = 1064
sfm_nm = 1/(1/seed_nm + 1/pump_nm)
x = seed_nm*1e-3*np.array(results['Output pulse energy (mJ)']).T[1][0]/(h*c)
y1 = seed_nm*1e-3*np.array(results['Output pulse energy (mJ)']).T[1][0]/(h*c)
y2 = sfm_nm*1e-3*np.array(results['Output pulse energy (mJ)']).T[2][0]/(h*c)

fig, ax1 = plt.subplots()
m.plot_options(fig, ax1, xlabel='(cw) seed photons', ylabel='idler pulse energy ($\mathrm{\mu J}$)')

ax1.plot(x, y1, '.', label='seed')
ax1.plot(x, y2, '^', label='SFM')
#ax1.set_xscale('log')
#ax1.set_yscale('log')
ax1.loglog()
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
#ax1.set_xlim(left=1e10)
#ax1.set_ylim(bottom=1e10)
ax1.legend()
#m.plot_options(fig, ax2, xlabel='(cw) idler power (W)',ylabel='idler pulse duration (ns)')
#ax2.plot(x, y2, '-')
plt.tight_layout()
plt.ticklabel_format(axis='both',  useOffset=False, style='plain')
# m.save_plot('OPA1_seed_sim')
plt.show()

#%%
#%% plot conversion efficiency
fig, ax1 = plt.subplots()
m.plot_options(fig, ax1, xlabel='(cw) seed photons', ylabel='conversion efficiency (%)')
h = scipy.constants.h
c = scipy.constants.c
seed_nm = 1417
pump_nm = 1064
sfm_nm = 1/(1/seed_nm + 1/pump_nm)
x = 1e-3*np.array(results['Output pulse energy (mJ)']).T[1][0]
y1 = 100*sfm_nm*np.array(results['Output pulse energy (mJ)']).T[2][0]/(seed_nm*np.array(results['Output pulse energy (mJ)']).T[1][0])

ax1.plot(x[y1<50], y1[y1<50], '-')
#ax1.set_xscale('log')
#ax1.set_yscale('log')
#ax1.set_xlim(left=1e10)
#ax1.set_ylim(bottom=1e10)
#ax1.legend()
#m.plot_options(fig, ax2, xlabel='(cw) idler power (W)',ylabel='idler pulse duration (ns)')
#ax2.plot(x, y2, '-')
plt.tight_layout()
# m.save_plot('OPA1_seed_sim')
plt.show()

#%% get result
pump_energy =  0.00916
seed_power = 7e-05
set_value(dict_2dmixlp['Energy/power (J or W)'][2], seed_power)
set_value(dict_2dmixlp['Energy/power (J or W)'][0], pump_energy)
moveto(dict_2dmixlp['Accept'])
gui.click()
dict1 = run_2dmixlp()
m.set_key(dict1, 'seed power (W)', seed_power)
m.set_key(dict1, 'pump pulse energy (J)', pump_energy)
dict2 = get_spectr()
results = merge_dict([dict1, dict2])
#%% gather OPA1 values
duration_idl_ns = results['duration_idl_ns'][0]
fwhm_idl_MHz = results['fwhm_idl_MHz'][0]
energy_sfm_mJ = results['Output pulse energy (mJ)'][0][2]
y = np.array(results['Output pulse energy (mJ)'])*1e3
input_energy_mJ = results['seed power (W)'][0]*8e-9*1e3
efficiency = (results['Output pulse energy (mJ)'][0][2]/input_energy_mJ)
#gain = (1e-3*energy_idl_mJ)/(1e-9 * duration_idl_ns)/results['seed power (W)'][0]

print(f'idler pulse energy: {energy_idl_mJ * 1e3:.3f}uJ')
print(f'conversion efficiency: {efficiency*1e2:.3f}%')
print(f'single pass gain: {gain:.1f}')
print(f'idler duration:{duration_idl_ns:.3f}ns')
print(f'idler bandwidth: {fwhm_idl_MHz:.3f}MHz')
