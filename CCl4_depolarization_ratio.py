from manipulate_oscilloscope import *

import numpy as np
import matplotlib.pyplot as plt

# CCL4
# DEPOLARZIATION RATIOS

# Get Stokes spectra GOOD peaks with polarizer at 90
dic_90 = oscilloscope_data(shot_num= 26)
spectrum_90 = get_scanned_signal(dic_90)

dic_0 = oscilloscope_data(shot_num= 29)
spectrum_0 = get_scanned_signal(dic_0)

lambda_start = 638 # nm
lambda_end = 660 # nm

#------------
# Get x axis (raman shift)
min_len = min([len(spectrum_0), len(spectrum_90)])
spectrum_90 = spectrum_90[:min_len]            # convert to same length
spectrum_0 = spectrum_0[:min_len]
# Create wavelength axis (same length as signal)
wavelengths = np.linspace(lambda_start, lambda_end, min_len)
# Convert nm → wavenumber (cm^-1)
nu_laser = 1e7 / 632.8
nu_scattered = 1e7 / wavelengths
# Raman shift (Stokes)
raman_shift = nu_laser - nu_scattered


#-----------

# Get intensities from the previous indices

# Define the Raman shift windows where we expect peaks
ranges = [
    (400, 500),
    (300, 400),
    (200, 300)
]

print('Data Analysis: \n')

for rmin, rmax in ranges:

    # mask for the range
    mask = (raman_shift >= rmin) & (raman_shift <= rmax)

    # restrict arrays
    shifts_window = raman_shift[mask]
    spec90_window = spectrum_90[mask]
    spec0_window = spectrum_0[mask]
    wavelengths_window = wavelengths[mask]

    # index of max peak in this window
    local_idx = np.argmax(spec90_window)

    shift = shifts_window[local_idx]
    idx_global = np.where(mask)[0][local_idx]

    vol_90 = spec90_window[local_idx]
    vol_0 = spec0_window[local_idx]

    dep_ratio = vol_0 / vol_90

    print(f"Peak in range [{rmin},{rmax}] cm^-1")
    print(f"    wavelength:            {wavelengths[idx_global]:.1f} nm")
    print(f"    Raman shift:           {shift:.1f} cm^-1")
    print(f"    voltage with 90°:      {vol_90} V")
    print(f"    voltage with 0°:       {vol_0} V")
    print(f"    depolarization ratio:  {dep_ratio:.3f}")
    print()