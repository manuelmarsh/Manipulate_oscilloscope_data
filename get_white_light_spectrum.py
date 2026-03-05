from manipulate_oscilloscope import *

import numpy as np
import matplotlib.pyplot as plt

# White Light Spectrum
plot_title='White Light Spectrum'
lambda_start = 480 # nm
lambda_end = 780 # nm

scanned_signals = {}

dic_h = oscilloscope_data(shot_num=4)
spectrum_h = get_scanned_signal(dic_h)

dic_v = oscilloscope_data(shot_num=5)
spectrum_v = get_scanned_signal(dic_v)

len_signal = len(spectrum_h)

print(f'length white horizontal={len(spectrum_h)}, vertical={len(spectrum_v)}')

scanned_signals['Horizontal polarization'] = spectrum_h
scanned_signals['Vertical polarization'] = spectrum_v

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True)


# Blab Body radiation plot

h = 6.626e-34
c = 3.0e8
kB = 1.381e-23

T = 2800  # Temperature (K)

# Laser wavelength (nm)
lambda_laser = 632.8
nu_laser = 1e7 / lambda_laser  # cm^-1

# Wavelength range (meters)
# get the number of samples from any signal in the dictionary (all the same)
lam = np.linspace(480e-9, 780e-9, len(list(scanned_signals.items())[0]))

# Planck's Law
B = (2*h*c**2) / (lam**5) / (np.exp(h*c / (lam*kB*T)) - 1)

# Convert wavelength → nm
lam_nm = lam * 1e9

# Convert wavelength → Raman shift (cm^-1)
nu_scattered = 1e7 / lam_nm
raman_shift = nu_laser - nu_scattered

# Plot
plt.figure()
plt.plot(raman_shift, B, linewidth=2)
plt.xlabel("Raman Shift (cm$^{-1}$)")
plt.ylabel(r'$B(\lambda, T)$  [W sr$^{-1}$ m$^{-3}$]')
plt.title('Blackbody Radiation at 2800 K (converted to Raman axis)')
plt.grid(True)

# Raman convention
plt.gca().invert_xaxis()

plt.savefig(f'Blackbody Radiation.pdf')
plt.show()