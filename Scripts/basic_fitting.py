import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def read_file(file):
    data = []
    with open(file, 'r') as f:
        for line in f:
            data.append(float(line.strip().split(' ')[1]))
    return np.array(data)
# Generate synthetic brainwaves with approximate frequencies
# Gamma (30-100 Hz), Beta (13-30 Hz), Alpha (8-13 Hz), Theta (4-8 Hz), Delta (0.5-4 Hz)

def generate_wave(frequency, duration=1.0, sample_rate=1000, noise_level=0.1):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t) + noise_level * np.random.randn(len(t))
    return t, wave

# Define brainwave frequencies (Hz)
frequencies = {
    "Gamma": 40,
    "Beta": 20,
    "Alpha": 10,
    "Theta": 6,
    "Delta": 2,
}

# Generate and plot signals
sample_rate = 1000  # Samples per second
duration = 1.0      # Duration in 
# brainwaves = {}

# for i, (wave_name, freq) in enumerate(frequencies.items()):
#     t, wave = generate_wave(freq, duration, sample_rate)
#     brainwaves[wave_name] = wave
#     plt.subplot(5, 1, i + 1)
#     plt.plot(t, wave, label=f"{wave_name} ({freq} Hz)")
#     plt.legend()
#     plt.grid()

brainwaves = {}
import sys
files = sys.argv[1:]
for file in files:
    brainwaves[file] = read_file(file)


# for i, (wave_name, freq) in enumerate(frequencies.items()):
#     t, wave = generate_wave(freq, duration, sample_rate)
#     brainwaves[wave_name] = wave
#     plt.subplot(5, 1, i + 1)
#     plt.plot(t, wave, label=f"{wave_name} ({freq} Hz)")
#     plt.legend()
#     plt.grid()


# plt.tight_layout()
# plt.show()


# plot the brainwaves
# Compute FFT and return the dominant frequency for each wave
def compute_fft(wave, sample_rate):
    N = len(wave)
    fft_result = np.fft.fft(wave)
    freqs = np.fft.fftfreq(N, 1 / sample_rate)
    magnitudes = np.abs(fft_result[:N // 2])
    freqs = freqs[:N // 2]
    dominant_freq = freqs[np.argmax(magnitudes)]
    return dominant_freq

fig, ax = plt.subplots(len(brainwaves), 1)


# Calculate and print dominant frequencies
i = 0 
for wave_name, wave in brainwaves.items():
    dominant_freq = compute_fft(wave, sample_rate)
    # print(wave)
    # print(dominant_freq)
    # plot the wave and the dominant frequency
    
    print(f"The dominant frequency of {wave_name} wave is approximately {dominant_freq:.2f} Hz")
    t, wave2 = generate_wave(dominant_freq, duration, sample_rate)
    # ax[i].plot(wave)
    ax[i].set_title(f"Dominant Frequency: {dominant_freq:.2f} Hz")
    ax[i].set_xlabel("Time")
    ax[i].set_ylabel("Amplitude")
    # ax[i].plot(t, wave2)
    ax[i].grid()

    # ax[i].plot(wave2)

    i+=1
plt.show()