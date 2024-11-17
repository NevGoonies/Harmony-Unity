import numpy as np
from scipy.signal import find_peaks, welch
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

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

def classify_brainwave(frequency):
    """
    Classify the brainwave based on its frequency.
    
    Parameters:
    frequency (float): Frequency in Hz
    
    Returns:
    str: Brain wave type
    """
    if frequency >= 30:
        return 'Gamma'
    elif 13 <= frequency < 30:
        return 'Beta'
    elif 8 <= frequency < 13:
        return 'Alpha'
    elif 4 <= frequency < 8:
        return 'Theta'
    elif frequency < 4:
        return 'Delta'
    


def read_file(file):
    data = []
    with open(file, 'r') as f:
        for line in f:
            data.append(float(line.strip().split(' ')[1]))
    return np.array(data)
def read_sigals(file_names):
    ret = { }
    for file in file_names:
        data = read_file(file)
        ret[file] = data
    return ret


# Example usage
def generate_sample_waves(duration=1.0, sampling_rate=256):
    """
    Generate sample brainwaves for testing.
    """
    t = np.linspace(0, duration, int(duration * sampling_rate))
    
    # Generate different types of waves
    gamma = np.sin(2 * np.pi * 40 * t) * np.random.uniform(0.5, 1.5, len(t))
    beta = np.sin(2 * np.pi * 20 * t) * np.random.uniform(0.5, 1.5, len(t))
    alpha = np.sin(2 * np.pi * 10 * t) * np.random.uniform(0.5, 1.5, len(t))
    theta = np.sin(2 * np.pi * 6 * t) * np.random.uniform(0.5, 1.5, len(t))
    delta = np.sin(2 * np.pi * 2 * t) * np.random.uniform(0.5, 1.5, len(t))
    
    return {
        'Gamma': gamma,
        'Beta': beta,
        'Alpha': alpha,
        'Theta': theta,
        'Delta': delta
    }


import sys
# Test the functions
if __name__ == "__main__":
    # Generate sample waves
    waves = generate_sample_waves()
    # print(waves)
    waves = read_sigals(sys.argv[1:])
    # Analyze each wave type
    fig, ax = plt.subplots(len(waves), 1)
    i = 0

    
    for wave_type, signal in waves.items():

        

        # Try all methods
        freq_fft = analyze_brainwave(signal, method='fft')
        freq_peaks = analyze_brainwave(signal, method='peaks')
        freq_welch = analyze_brainwave(signal, method='welch')
        
        print(f"\n{wave_type} wave analysis:")
        print(f"FFT method: {freq_fft:.1f} Hz - Classified as: {classify_brainwave(freq_fft)}")
        print(f"Peak method: {freq_peaks:.1f} Hz - Classified as: {classify_brainwave(freq_peaks)}")
        print(f"Welch method: {freq_welch:.1f} Hz - Classified as: {classify_brainwave(freq_welch)}")


        ax[i].plot(signal)
        ax[i].set_title(f"{wave_type} wave")
        ax[i].set_xlabel("Time")
        ax[i].set_ylabel("Amplitude")
        ax[i].grid()



        i+=1

    plt.show()