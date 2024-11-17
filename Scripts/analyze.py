import numpy as np
from scipy.signal import find_peaks, welch
from scipy.fft import fft, fftfreq

# peaks is bad we average the FFT and Welch's
def analyze_brainwave(signal, sampling_rate=256, method='fft'):
    """
    Analyze brainwave signal to determine its primary frequency.
    
    Parameters:
    signal (array): The input signal time series
    sampling_rate (int): Number of samples per second
    method (str): 'fft' or 'peaks' or 'welch'
    
    Returns:
    float: Primary frequency in Hz
    """
    # Normalize the signal to remove amplitude variations
    normalized_signal = (signal - np.mean(signal)) / np.std(signal)
    
    if method == 'fft':
        # FFT method
        n = len(signal)
        yf = np.abs(fft(normalized_signal))
        xf = fftfreq(n, 1/sampling_rate)
        
        # Consider only positive frequencies
        positive_freqs = xf[1:n//2]
        positive_amps = yf[1:n//2]
        
        # Find the frequency with maximum amplitude
        primary_freq = positive_freqs[np.argmax(positive_amps)]
        
    elif method == 'peaks':
        # Peak counting method
        peaks, _ = find_peaks(normalized_signal, distance=5)
        if len(peaks) > 1:
            # Calculate average distance between peaks
            avg_peak_distance = np.mean(np.diff(peaks))
            # Convert to frequency
            primary_freq = sampling_rate / avg_peak_distance
        else:
            primary_freq = 0
            
    else:  # Welch's method
        frequencies, psd = welch(normalized_signal, fs=sampling_rate)
        primary_freq = frequencies[np.argmax(psd)]
    
    return primary_freq

def get_freq(signal):
    signal = np.array(signal)
    # print(signal)
    fft = analyze_brainwave(signal, method='fft')
    peaks = analyze_brainwave(signal, method='peaks')
    welch = analyze_brainwave(signal, method='welch')
    return {
        "fft": fft,
        "peaks": peaks,
        "welch": welch
    }