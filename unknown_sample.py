from manipulate_oscilloscope import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Unknown solution
"""
- ALL0040 : 636-690, 0.1, Stokes, 90 Pol
=> Good zoom
- ALL0041 : 636-690, 0.1, Stokes, 90 Pol, (0) Vert. POL
=> full noise
- ALL0042 : 636-690, 0.1, Stokes, 90 Pol, (90) Horiz. POL
=> peaks remain , good

- ALL0043 : 560-629, 0.1, AntiStokes, 90 Pol
"""

# Stokes [636-690] nm
plot_title='Stokes lines of the unknown sample'
lambda_start = 636 # nm
lambda_end = 690 # nm

scanned_signals = {}

# Laser always 90°

dic_noPol = oscilloscope_data(shot_num= 40) 
spectrum_noPol = get_scanned_signal(dic_noPol)

dic_90 = oscilloscope_data(shot_num= 42) 
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 41) 
spectrum_0 = get_scanned_signal(dic_0)

scanned_signals['Not polarized'] = spectrum_noPol
scanned_signals['0° polarization (Polarizer)'] = spectrum_0
scanned_signals['90° polarization (Polarizer)'] = spectrum_90

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='unknown_Stokes')

# Get the peaks of spectrum_noPol

# Create wavelength axis (same length as signal)
wavelengths = np.linspace(lambda_start, lambda_end, len(spectrum_noPol))
nu_laser = 1e7 / 632.8
nu_scattered = 1e7 / wavelengths

# Raman shift
raman_shift = nu_laser - nu_scattered

# Get raman lines
n=4
indices, shifts, intensities = get_top_n_peaks(raman_shift, spectrum_noPol, n=n)
print(f"Looking at Stokes Spectrum of the unknown sample, the Raman shifts (cm^-1) corresponding to first {n} peaks are : ", list(shifts))


#-----------------------------
# Anti Stokes [560-629] nm
plot_title='Anti Stokes lines of the unknown sample'
lambda_start = 560 # nm
lambda_end = 629 # nm

scanned_signals = {}

# Laser always 90°

dic = oscilloscope_data(shot_num= 43) 
spectrum = get_scanned_signal(dic)


scanned_signals['90° polarization (Laser)'] = spectrum

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='unknown_Anti_Stokes')


# find peaks of NoPol

ranges = [
    (250, 380),
    (400, 500),
    (750, 900),
    (900, 1000)
]

for rmin, rmax in ranges:

    # mask for the range
    mask = (raman_shift >= rmin) & (raman_shift <= rmax)

    # restrict arrays
    shifts_window = raman_shift[mask]
    spec_window = spectrum_noPol[mask]
    wavelengths_window = wavelengths[mask]

    # index of max peak in this window
    local_idx = np.argmax(spec_window)

    shift = shifts_window[local_idx]
    idx_global = np.where(mask)[0][local_idx]

    vol = spectrum_noPol[idx_global]


    print(f"Peak in range [{rmin},{rmax}] cm^-1")
    print(f"    wavelength:            {wavelengths[idx_global]:.1f} nm")
    print(f"    Raman shift:           {shift:.1f} cm^-1")
    print(f"    voltage:               {vol} V")
    print()