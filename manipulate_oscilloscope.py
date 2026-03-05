from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

def load_oscilloscope_csv(file_path):
    """
    Load oscilloscope CSV and return time and voltage as numpy arrays.
    """
    
    df = pd.read_csv(file_path, header=None)
    
    # Drop rows that don't contain numeric data
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    df_numeric = df_numeric.dropna(how='all')
    
    # In our format:
    # Column 3 = voltage
    # Column 4 = time
    voltage = df_numeric.iloc[:, 4].dropna().to_numpy()
    time = df_numeric.iloc[:, 3].dropna().to_numpy()
    
    return time, voltage

def oscilloscope_data(shot_num, base_path_str=r"C:\Users\Manuel Martini\Desktop\Raman\Data"):
    """
    Input:
        base_path_str = string path: where you keep the Raman files
        num = integer identifying the folder, example: for folder ALL0005, num=6
    Output:
        dic: dictionary with 3 keys: 'time', 'ch1', 'ch2' = every value is numpy array of time and oscilloscope outputs
    """
    str_num = str(shot_num)

    str_num = (4-len(str_num))*'0' + str_num

    # Specific subfolder name
    subfolder_name = f'ALL{str_num}'

    # Build full path
    main_folder = Path(base_path_str)
    subfolder_path = main_folder / subfolder_name

    # Access CSVs inside it
    file_ch1 = subfolder_path / f"F{str_num}CH1.csv"
    file_ch2 = subfolder_path / f"F{str_num}CH2.csv"
    
    dic = {}

    if file_ch1.exists():
        time, v1 = load_oscilloscope_csv(file_ch1)
        dic["time"]=time
        dic["ch1"]=v1
        
    if file_ch2.exists():
        time, v2 = load_oscilloscope_csv(file_ch2)
        dic["time"]=time
        dic["ch2"]=v2

    return dic


def limits_monochromator_control_old(signal, tol=1, low=0, high=5):
    """
    Input: 
        signal: voltage np array
        tol: tolerance for voltage level
        low: low level of voltage in the monoch
        high: high level of voltage in the monoch
    Output:
        if signal is not monochromator control: return False
        else: retrun list of the index of start and end of the control.
    """

    
    
    # Scanner OFF range
    if not abs(signal[0] - low) < tol: # check first value
        return False
    
    for i in range(len(signal)):
        if not abs(signal[i] - low) < tol:
            start = i
            break

    # If never broke it means that we reached the end
    if i == len(signal) - 1:
        return False
    
    # Scanner ON range
    if not abs(signal[start] - high) < tol: # check first value of this range
        return False
    
    for i in range(start, len(signal)):
        if not abs(signal[i] - high) < tol:
            end = i
            break

    # If never breaked it means that we reached the end
    if i == len(signal) - 1:
        return False
    
    # Scanner OFF range again
    if not abs(signal[end] - low) < tol: # check first value of this range
        return False
    
    return [start, end]


def limits_monochromator_control(signal, tol=1, low=0, high=5):
    """
    Detects a monochromator control signal pattern: OFF (low) -> ON (high) -> OFF (low)
    
    Parameters:
        signal: np.array of voltage values
        tol: tolerance for voltage levels
        low: low voltage level (OFF)
        high: high voltage level (ON)
    
    Returns:
        [start_index, end_index] of the ON region if pattern detected
        False if pattern not found
    """
    
    signal = np.asarray(signal)
    N = len(signal)
    
    # Helper to check if value is within tolerance
    def is_low(val):
        return abs(val - low) < tol
    
    def is_high(val):
        return abs(val - high) < tol
    
    # Step through signal
    i = 0
    while i < N:
        # Find first low→high transition
        if is_low(signal[i]):
            # find start of high
            j = i
            while j < N and is_low(signal[j]):
                j += 1
            if j == N:
                break  # reached end without finding high
            if not is_high(signal[j]):
                i = j
                continue  # not a proper ON region, skip
            start = j  # first index of high region
            
            # find end of high
            k = start
            while k < N and is_high(signal[k]):
                k += 1
            if k == N:
                break  # reached end without OFF after high
            if not is_low(signal[k]):
                i = k
                continue  # not a proper OFF after high, skip
            
            end = k - 1  # last index of high region
            return [start, end]
        i += 1
    
    return False


def get_scanned_signal(dic):
    """
    Inputs:
        dic: dictionary with 3 keys: time, ch1, ch2 = numpy array of time and oscilloscope outputs
    Outputs: 
        scanned_signal : np.array with scanned subsequence 
    """
    v1 = dic["ch1"]
    v2 = dic["ch2"]
    limits_v1 = limits_monochromator_control(v1)
    limits_v2 = limits_monochromator_control(v2)

    if limits_v1 and limits_v2:
        raise KeyError('Both of the two signals are recognized as a monochromator control, check the csv')
    
    if not (limits_v1 or limits_v2):
        raise KeyError('None of the two signals was recognized as a monochromator control, check the csv')

    if limits_v1: # v1 is monochromator control
        start = limits_v1[0]
        end = limits_v1[1]
        # v2 is signal
        scanned_signal = v2[start:end]

    if limits_v2: # v2 is monochromator control
        start = limits_v2[0]
        end = limits_v2[1]
        # v1 is signal
        scanned_signal = v1[start:end]

    return scanned_signal

def plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, lambda_laser=632.8,  theoretical_lines=[], save=True, show=True, save_as=''):
    """
    Inputs:
        scanned_signals: dictionary where key=legend_string_name, value=np.array signal
        lambda_start: starting wavelength in nm
        lambda_end: ending wavelength in nm
        lambda_laser: laser wavelength in nm
    Plots:
        signal with horizontal axis as Raman Shift in cm^-1
    """
    min_len = min([len(signal) for signal in scanned_signals.values()])
    
    # Create wavelength axis (same length as signal)
    wavelengths = np.linspace(lambda_start, lambda_end, min_len)

    # Convert nm → wavenumber (cm^-1)
    nu_laser = 1e7 / lambda_laser
    nu_scattered = 1e7 / wavelengths

    # Raman shift (Stokes)
    raman_shift = nu_laser - nu_scattered

    # Plot
    plt.figure(figsize=(8,5))

    for name, signal in scanned_signals.items():
        plt.plot(raman_shift, signal[:min_len], label=name)

    plt.xlabel("Raman Shift (cm$^{-1}$)")
    plt.ylabel("Voltage (V)")
    plt.title(plot_title)
    plt.grid(True)

    # Standard Raman convention: higher shift on the left
    plt.gca().invert_xaxis()

    plt.tight_layout()

    # add theoretical lines if present
    # Add vertical lines for theoretical Raman peaks
    if theoretical_lines:
        ymin, ymax = plt.ylim()
        y_text = ymax - 0.05 * (ymax - ymin)  # slightly below top
        first_line = True

        for line in theoretical_lines:
            if min(raman_shift) <= line <= max(raman_shift):

                # Draw vertical line (semi-transparent)
                if first_line:
                    plt.vlines(line, ymin, ymax,
                            colors='red',
                            linestyles='dashed',
                            alpha=0.35,
                            linewidth=1.5,
                            label='Theoretical Raman lines')
                    first_line = False
                else:
                    plt.vlines(line, ymin, ymax,
                            colors='red',
                            linestyles='dashed',
                            alpha=0.35,
                            linewidth=1.5)

                # Add small peak label above line
                plt.text(line,
                        y_text,
                        f"{int(line)}",
                        rotation=90,
                        verticalalignment='top',
                        horizontalalignment='center',
                        fontsize=8,
                        color='red',
                        alpha=0.8)
    
    # Add legend if there is more than one thing plotted
    if len(scanned_signals) > 1 or theoretical_lines:
        plt.legend()

    if save:
        if save_as:
            plt.savefig(f'{save_as}.pdf')
        else:
            plt.savefig(f'{plot_title}.pdf')
    if show:
        plt.show()
        


def get_top_n_peaks(raman_shift, signal, n=4):
    """
    Returns the indices, Raman shift values, 
    and intensities of the n highest local maxima.
    """

    peaks, _ = find_peaks(signal)

    if len(peaks) == 0:
        return np.array([]), np.array([]), np.array([])

    # Sort peaks by descending intensity
    peak_heights = signal[peaks]
    sorted_indices = np.argsort(peak_heights)[::-1]

    top_peaks = peaks[sorted_indices[:n]]

    return (
        top_peaks,
        raman_shift[top_peaks],
        signal[top_peaks]
    )


# Curve fit:

# Single Gaussian
def gaussian(x, A, x0, sigma):
    return A * np.exp(-(x - x0)**2 / (2 * sigma**2))

# Multiple Gaussians
def multi_gaussian(x, *params):
    y = np.zeros_like(x)
    n_peaks = len(params) // 3
    for i in range(n_peaks):
        A, x0, sigma = params[3*i:3*i+3]
        y += gaussian(x, A, x0, sigma)
    return y

# Main fitting function
def fit_raman_spectrum(x, y, height=None, distance=None, legend_name=None, plot=True, plot_title=None, theoretical_lines=None):
    """
    x: Raman shift array
    y: intensity array
    height: minimum height for peak detection (optional)
    distance: minimum distance between peaks (optional)
    plot: whether to plot data + fits
    plot_title: string title
    legend_name:
    """
    # Detect approximate peak positions
    peaks, _ = find_peaks(y, height=height, distance=distance)
    if len(peaks) == 0:
        print("No peaks detected!")
        return None
    
    # Prepare initial guesses: [A1, x01, sigma1, A2, x02, sigma2, ...]
    initial_guesses = []
    for p in peaks:
        A_guess = y[p]
        x0_guess = x[p]
        sigma_guess = 30  # rough estimate, can tweak
        initial_guesses += [A_guess, x0_guess, sigma_guess]

    # Fit
    try:
        popt, _ = curve_fit(multi_gaussian, x, y, p0=initial_guesses)
    except RuntimeError:
        print("Fit did not converge!")
        return None
    
    # Extract fitted peak info
    n_peaks = len(popt) // 3
    peak_info = []
    for i in range(n_peaks):
        A, x0, sigma = popt[3*i:3*i+3]
        FWHM = 2.355 * sigma
        peak_info.append({'center': x0, 'amplitude': A, 'sigma': sigma, 'FWHM': FWHM})
    
    # Optional plot
    if plot:
        # plt.figure(figsize=(8,5))
        # plt.plot(x, y, label='Data')
        plt.plot(x, multi_gaussian(x, *popt), 'r-', label=legend_name)
        for i in range(n_peaks):
            A, x0, sigma = popt[3*i:3*i+3]
            plt.plot(x, gaussian(x, A, x0, sigma), '--', label=f'Peak {i+1}')
        plt.xlabel('Raman Shift (cm$^{-1}$)')
        plt.ylabel('Voltage (V)')
        plt.legend()
        # plt.show()
        if plot_title:
            plt.title(plot_title)
        
        # Add vertical lines for theoretical Raman peaks
        if theoretical_lines:
            ymin, ymax = plt.ylim()
            y_text = ymax - 0.05 * (ymax - ymin)  # slightly below top
            first_line = True

            for line in theoretical_lines:
                if min(raman_shift) <= line <= max(raman_shift):

                    # Draw vertical line (semi-transparent)
                    if first_line:
                        plt.vlines(line, ymin, ymax,
                                colors='red',
                                linestyles='dashed',
                                alpha=0.35,
                                linewidth=1.5,
                                label='Theoretical Raman lines')
                        first_line = False
                    else:
                        plt.vlines(line, ymin, ymax,
                                colors='red',
                                linestyles='dashed',
                                alpha=0.35,
                                linewidth=1.5)

                    # Add small peak label above line
                    plt.text(line,
                            y_text,
                            f"{int(line)}",
                            rotation=90,
                            verticalalignment='top',
                            horizontalalignment='center',
                            fontsize=8,
                            color='red',
                            alpha=0.8)
    
    return peak_info



if __name__=='__main__':

    shot_num=22
    plot_title='Full Spectrum EXAMPLE'
    lambda_start = 480 # nm
    lambda_end = 780 # nm

    dic = oscilloscope_data(shot_num)
    scanned_signals={'an important signal': get_scanned_signal(dic)}

    plot_signal(scanned_signals, plot_title, lambda_start, lambda_end, save=False, show=False)

    plt.show()