from manipulate_oscilloscope import *

import numpy as np
import matplotlib.pyplot as plt

# CCl4
# Show full noise with :
plot_title='Stokes lines of CCl4 (Polarizer 0° Polarization)'
lambda_start = 638 # nm
lambda_end = 660 # nm
theoretical_lines = [
    -790, -459, -314, -218,   # Anti-Stokes
     0,                       # Rayleigh
     218, 314, 459, 790       # Stokes    (all in cm^-1)
] 

scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 27)
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 28)
spectrum_0 = get_scanned_signal(dic_0)


scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='CCl4_Stokes_0pol', theoretical_lines = theoretical_lines)



# Show peaks with polarizer at 90
plot_title='Stokes lines of CCl4 (Polarizer 90° Polarization)'
lambda_start = 638 # nm
lambda_end = 660 # nm

scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 26)
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 29)
spectrum_0 = get_scanned_signal(dic_0)


scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='CCl4_Stokes_90pol', theoretical_lines=theoretical_lines)



