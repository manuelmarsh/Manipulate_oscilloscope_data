from manipulate_oscilloscope import *
import numpy as np
import matplotlib.pyplot as plt

"""                               Laser Polariz.:
- ALL0022 : 600-628, 0.1, AntiStokes, 90 Pol   
- ALL0023 : 600-633, 0.1, AntiStokes, 0 Pol
"""

# Antistokes [600-628]  , Problem : 2 different lengths of the scan !!!
plot_title='Anti-Stokes lines of CCl4'
lambda_start = 600 # nm
lambda_end = 628 # nm
theoretical_lines = [
    -790, -459, -314, -218,   # Anti-Stokes
     0,                       # Rayleigh
     218, 314, 459, 790       # Stokes    (all in cm^-1)
] 


scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 22) # [600-628]
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 23) 
spectrum_0 = get_scanned_signal(dic_0)[:len(spectrum_90)] # [600-633] reduced to [600-628]


scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='CCl4_Anti_Stokes', theoretical_lines=theoretical_lines)
