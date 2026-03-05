from manipulate_oscilloscope import *
import numpy as np
import matplotlib.pyplot as plt

"""
- ALL0024 : 627-636, 0.1, Rayleigh, 0 Pol
- ALL0025 : 627-636, 0.1, Rayleigh, 90 Pol
"""

# Rayleigh [627-636] nm
plot_title='Rayleigh line of CCl4 (Polarizer 90° Polarization)'
lambda_start = 627 # nm
lambda_end = 636 # nm
theoretical_lines = [
    -790, -459, -314, -218,   # Anti-Stokes
     0,                       # Rayleigh
     218, 314, 459, 790       # Stokes    (all in cm^-1)
] 

scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 25) 
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 24) 
spectrum_0 = get_scanned_signal(dic_0)


scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='CCl4_Rayleigh', theoretical_lines=theoretical_lines)