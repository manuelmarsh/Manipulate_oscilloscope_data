RamanSpectroscopy

A Python library for processing Raman spectroscopy data from oscilloscope CSV files. Automatically detects monochromator control signals, extracts scanned regions, converts to Raman shift, and provides peak detection and Gaussian fitting.

Features
Load oscilloscope CSV data (CH1/CH2 channels)

Detect monochromator control pattern (low→high→low voltage)

Extract scanned Raman signal regions

Convert wavelength range to Raman shift (cm⁻¹)

Plot spectra with theoretical Raman line overlays

Peak detection with scipy.signal.find_peaks

Multi-Gaussian curve fitting with scipy.optimize.curve_fit
