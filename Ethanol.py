from manipulate_oscilloscope import *
import numpy as np
import matplotlib.pyplot as plt


# Ethanol + Water samples

# New Analysys: zoom into where the theoretical lines are:

plot_title='Stokes lines of Ethanol + Water'
lambda_start = 637 # nm
lambda_end = 8000 # nm
theoretical_lines = [
     433, 882, 1051, 1096, 1274, 1454, 2877, 2928, 2974       # Stokes    (all in cm^-1)
] 

scanned_signals = {}

dic_100 = oscilloscope_data(shot_num= 44)
spectrum_100 = get_scanned_signal(dic_100)

dic_0 = oscilloscope_data(shot_num= 45)
spectrum_0 = get_scanned_signal(dic_0)

dic_25 = oscilloscope_data(shot_num= 46)
spectrum_25 = get_scanned_signal(dic_25)

dic_50 = oscilloscope_data(shot_num= 47)
spectrum_50 = get_scanned_signal(dic_50)

dic_75 = oscilloscope_data(shot_num= 48)
spectrum_75 = get_scanned_signal(dic_75)

dic_x = oscilloscope_data(shot_num= 49)
spectrum_x = get_scanned_signal(dic_x)

leng = len(spectrum_x) // 3

scanned_signals[f'{100}% Ethanol'] = spectrum_100[:leng]
scanned_signals[f'{0}% Ethanol'] = spectrum_0[:leng]
scanned_signals[f'{25}% Ethanol'] = spectrum_25[:leng]
scanned_signals[f'{50}% Ethanol'] = spectrum_50[:leng]
scanned_signals[f'{75}% Ethanol'] = spectrum_75[:leng]
scanned_signals[f'{'X'}% Ethanol'] = spectrum_x[:leng]


# Take subsequence

plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='Ethanol_Stokes', theoretical_lines = theoretical_lines)





# Old Anaylisis


"""
- ALL0044 : 637-800, 2.0, Full Stokes, 90 pol, 100 percent ethanol
- ALL0045 : 637-800, 2.0, Full Stokes, 90 pol, 0 percent ethanol
- ALL0046 : 637-800, 2.0, Full Stokes, 90 pol, 25 percent ethanol
- ALL0047 : 637-800, 2.0, Full Stokes, 90 pol, 50 percent ethanol
- ALL0048 : 637-800, 2.0, Full Stokes, 90 pol, 75 percent ethanol
- ALL0049 : 637-800, 2.0, Full Stokes, 90 pol, X percent ethanol
"""


plot_title='Stokes lines of Ethanol + Water'
lambda_start = 637 # nm
lambda_end = 8000 # nm
theoretical_lines = [
     433, 882, 1051, 1096, 1274, 1454, 2877, 2928, 2974       # Stokes    (all in cm^-1)
] 

scanned_signals = {}

dic_100 = oscilloscope_data(shot_num= 44)
spectrum_100 = get_scanned_signal(dic_100)

dic_0 = oscilloscope_data(shot_num= 45)
spectrum_0 = get_scanned_signal(dic_0)

dic_25 = oscilloscope_data(shot_num= 46)
spectrum_25 = get_scanned_signal(dic_25)

dic_50 = oscilloscope_data(shot_num= 47)
spectrum_50 = get_scanned_signal(dic_50)

dic_75 = oscilloscope_data(shot_num= 48)
spectrum_75 = get_scanned_signal(dic_75)

dic_x = oscilloscope_data(shot_num= 49)
spectrum_x = get_scanned_signal(dic_x)


scanned_signals[f'{100}% Ethanol'] = spectrum_100
scanned_signals[f'{0}% Ethanol'] = spectrum_0
scanned_signals[f'{25}% Ethanol'] = spectrum_25
scanned_signals[f'{50}% Ethanol'] = spectrum_50
scanned_signals[f'{75}% Ethanol'] = spectrum_75
scanned_signals[f'{'X'}% Ethanol'] = spectrum_x

# plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=True, show=True, save_as='Ethanol_Stokes', theoretical_lines = theoretical_lines)


# ------------------- 
# Unknown Concetration

def estimate_ethanol_concentration_with_plot(known_conc, known_intensity, unknown_intensity):
    """
    Estimate ethanol concentration using linear interpolation
    and plot the calibration curve.

    Parameters
    ----------
    known_conc : array-like
        Known ethanol concentrations (e.g. [0,25,50,75,100])
    known_intensity : array-like
        Peak intensities measured for those samples
    unknown_intensity : float
        Peak intensity of the unknown sample

    Returns
    -------
    estimated_conc : float
        Estimated ethanol concentration
    """

    known_conc = np.array(known_conc)
    known_intensity = np.array(known_intensity)

    # Sort by intensity (required for interpolation)
    order = np.argsort(known_intensity)
    known_intensity = known_intensity[order]
    known_conc = known_conc[order]

    # Linear interpolation
    estimated_conc = np.interp(unknown_intensity, known_intensity, known_conc)

    # Linear fit (for visualization)
    coeff = np.polyfit(known_conc, known_intensity, 1)
    fit = np.poly1d(coeff)

    conc_fit = np.linspace(min(known_conc), max(known_conc)+50, 300)

    # Plot
    plt.figure()
    plt.scatter(known_conc, known_intensity, label="Measured samples")
    plt.plot(conc_fit, fit(conc_fit), linestyle=":", label="Linear fit")

    plt.scatter(
        estimated_conc,
        unknown_intensity,
        marker="x",
        s=120,
        label=f"Unknown (~{estimated_conc:.1f}%)"
    )

    plt.xlabel("Ethanol concentration (%)")
    plt.ylabel("Peak voltage (a.u.)")
    plt.title("Calibration curve for ethanol concentration")
    plt.legend()
    plt.grid(True)
    plt.show()

    return estimated_conc


known_conc = [0, 25, 50, 75]

max_index = np.argmax(spectrum_x)
peak_0 = spectrum_0[max_index]
peak_25 = spectrum_25[max_index]
peak_50=spectrum_50[max_index]
peak_75=spectrum_75[max_index]
peak_x=spectrum_x[max_index]

known_intensity = [
    peak_0,
    peak_25,
    peak_50,
    peak_75
]

unknown_intensity = peak_x

X = estimate_ethanol_concentration_with_plot(known_conc, known_intensity, unknown_intensity)

print(f"Estimated ethanol concentration: {X:.1f}%")