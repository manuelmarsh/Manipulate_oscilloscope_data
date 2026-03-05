from manipulate_oscilloscope import *
import numpy as np
import matplotlib.pyplot as plt
"""
BENZENE

- ALL0030 : 627-640, 0.1, Rayleigh, 0 Pol
- ALL0031 : 627-640, 0.1, Rayleigh, 90 Pol

For Stokes lines we see a peak at ~674.6 nm
    - ALL0032 : 637-690, 1.0, Stokes, 90 Pol % ignored
- ALL0033 : 637-750, 1.0, Stokes, 90 Pol        % use 
- ALL0034 : 637-750, 1.0, Stokes, 0 Pol          % use

- ALL0035 : 637-750, 1.0, Stokes, 90 Pol, (0) Vert. POL  => Seems to be just noise
- ALL0036 : 637-750, 1.0, Stokes, 90 Pol, (90) Horiz. POL   & use

- ALL0037 : 520-629, 1.0, AntiStokes, 90 Pol            %use in another graph
=> Only noise
"""


# Rayleigh [627-640] nm
plot_title='Rayleigh line of Benzene'
lambda_start = 627 # nm
lambda_end = 640 # nm
theoretical_lines = [
    -3063, -2947, -1584, -1176, -992, -606,   # Anti-Stokes
     0,                                       # Rayleigh
     606, 992, 1176, 1584, 2947, 3063         # Stokes
]

scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 31) 
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 30) 
spectrum_0 = get_scanned_signal(dic_0)


scanned_signals['0° polarization (Laser)'] = spectrum_0
scanned_signals['90° polarization (Laser)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=False, save_as='Benzene_Rayleigh', theoretical_lines=theoretical_lines)

# ------------------------------
# Stokes with different laser polariz.
plot_title='Stokes lines of Benzene'
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

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=False, save_as='Benzene_Stokes', theoretical_lines=theoretical_lines)

# ------------------------------------
# Stokes with different Polarizer polarization
plot_title='Stokes lines of Benzene after polarization'
lambda_start = 637 # nm
lambda_end = 750 # nm
theoretical_lines = [
    -3063, -2947, -1584, -1176, -992, -606,   # Anti-Stokes
     0,                                       # Rayleigh
     606, 992, 1176, 1584, 2947, 3063         # Stokes
]

scanned_signals = {}

dic_90 = oscilloscope_data(shot_num= 36) 
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 35) 
spectrum_0 = get_scanned_signal(dic_0)


scanned_signals['0° polarization (Polarizer)'] = spectrum_0
scanned_signals['90° polarization (Polarizer)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=False, save_as='Benzene_Stokes_polarizer', theoretical_lines=theoretical_lines)

#---------------------------------
# Antistokes 520-629
plot_title='Anti-Stokes lines of Benzene'
lambda_start = 520 # nm
lambda_end = 629 # nm
theoretical_lines = [
    -3063, -2947, -1584, -1176, -992, -606,   # Anti-Stokes
     0,                                       # Rayleigh
     606, 992, 1176, 1584, 2947, 3063         # Stokes
]

scanned_signals = {}

dic = oscilloscope_data(shot_num= 37) 
spectrum = get_scanned_signal(dic)


scanned_signals['Anti-Stokes lines'] = spectrum


plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=False, save_as='Benzene_AntiStokes', theoretical_lines=theoretical_lines)