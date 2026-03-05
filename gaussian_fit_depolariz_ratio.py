from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from manipulate_oscilloscope import *


# Fit, Raman wavelengths and Depolarization Ratio

# CCl4 Stokes
plot_title='Gaussian fit of Stokes lines of CCl4'
lambda_start = 638 # nm
lambda_end = 660 # nm
theoretical_lines = [
    -790, -459, -314, -218,   # Anti-Stokes
     0,                       # Rayleigh
     218, 314, 459, 790       # Stokes    (all in cm^-1)
] 
scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 26)
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 29)
spectrum_0 = get_scanned_signal(dic_0)

scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

#----------------------------------------
# Get x axis (raman shift)
min_len = min([len(signal) for signal in scanned_signals.values()])
# Create wavelength axis (same length as signal)
wavelengths = np.linspace(lambda_start, lambda_end, min_len)
# Convert nm → wavenumber (cm^-1)
nu_laser = 1e7 / 632.8
nu_scattered = 1e7 / wavelengths
# Raman shift (Stokes)
raman_shift = nu_laser - nu_scattered

#----------------------------------------
# Plot
plt.figure(figsize=(8,5))
peak_info_90 = fit_raman_spectrum(raman_shift, spectrum_90, height=0.5, legend_name='Fit of 90° Laser Pol. spectrum', distance=None, plot=True, plot_title=plot_title, theoretical_lines=theoretical_lines)
peak_info_0 = fit_raman_spectrum(raman_shift, spectrum_0, height=0.5, legend_name='Fit of 0° Laser Pol. spectrum', distance=None, plot=True, plot_title=plot_title, theoretical_lines=theoretical_lines)
plt.show()


exit()

#----------------------------------------
#----------------------------------------
#----------------------------------------

# BENZENE Stokes with different laser polariz.
plot_title='Gaussian fit of Stokes lines of Benzene'
lambda_start = 637 # nm
lambda_end = 750 # nm
theoretical_lines = [
    -3063, -2947, -1584, -1176, -992, -606,   # Anti-Stokes
     0,                                       # Rayleigh
     606, 992, 1176, 1584, 2947, 3063         # Stokes
]

scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 33) 
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 34) 
spectrum_0 = get_scanned_signal(dic_0)

scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

#----------------------------------------
# Get x axis (raman shift)
min_len = min([len(signal) for signal in scanned_signals.values()])
# Create wavelength axis (same length as signal)
wavelengths = np.linspace(lambda_start, lambda_end, min_len)
# Convert nm → wavenumber (cm^-1)
nu_laser = 1e7 / 632.8
nu_scattered = 1e7 / wavelengths
# Raman shift (Stokes)
raman_shift = nu_laser - nu_scattered

#----------------------------------------
# Plot
plt.figure(figsize=(8,5))
peak_info_90 = fit_raman_spectrum(raman_shift, spectrum_90, height=0.5, legend_name='Fit of 90° Laser Pol. spectrum', distance=None, plot=True, plot_title=plot_title, theoretical_lines=theoretical_lines)
peak_info_0 = fit_raman_spectrum(raman_shift, spectrum_0, height=0.5, legend_name='Fit of 0° Laser Pol. spectrum', distance=None, plot=True, plot_title=plot_title, theoretical_lines=theoretical_lines)
plt.show()
scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

# Benzene Stokes
plot_title='Gaussian fit of Stokes lines of CCl4'
lambda_start = 638 # nm
lambda_end = 660 # nm
theoretical_lines = [
    -790, -459, -314, -218,   # Anti-Stokes
     0,                       # Rayleigh
     218, 314, 459, 790       # Stokes    (all in cm^-1)
] 
scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 26)
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 29)
spectrum_0 = get_scanned_signal(dic_0)

scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

#----------------------------------------
# Get x axis (raman shift)
min_len = min([len(signal) for signal in scanned_signals.values()])
# Create wavelength axis (same length as signal)
wavelengths = np.linspace(lambda_start, lambda_end, min_len)
# Convert nm → wavenumber (cm^-1)
nu_laser = 1e7 / 632.8
nu_scattered = 1e7 / wavelengths
# Raman shift (Stokes)
raman_shift = nu_laser - nu_scattered

#----------------------------------------
# Plot
plt.figure(figsize=(8,5))
peak_info_90 = fit_raman_spectrum(raman_shift, spectrum_90, height=0.5, legend_name='Fit of 90° Laser Pol. spectrum', distance=None, plot=True, plot_title=plot_title, theoretical_lines=theoretical_lines)
peak_info_0 = fit_raman_spectrum(raman_shift, spectrum_0, height=0.5, legend_name='Fit of 0° Laser Pol. spectrum', distance=None, plot=True, plot_title=plot_title, theoretical_lines=theoretical_lines)
plt.show()