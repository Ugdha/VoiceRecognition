import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import pandas as pd


def pre_process(sample_rate, signal):
    # Normalize
    normalized_signal = signal/np.nanmax(signal)

    # Trim outlying values
    window = sample_rate // 50
    avg = pd.rolling_mean(abs(normalized_signal), window)
    std = pd.rolling_std(normalized_signal, window)
    trimmed_signal = np.clip(abs(normalized_signal), 0, std + avg)
    corrected_signal = trimmed_signal ** 2 / np.nanmax(trimmed_signal)

    # Find where the start and end of the speech are
    envelope = pd.rolling_std(corrected_signal, window) ** 2 / np.nanmax(pd.rolling_std(corrected_signal, window))
    start, end = np.nanmin(np.where(envelope-0.01 > 0)), np.nanmax(np.where(envelope-0.01 > 0))

    # Retrieve it in the original sample
    actual_sample = normalized_signal[start-window:end+window]

    # plot some stuff
    if __name__ == "__main__":
        axes[0].plot(signal)
        axes[1].plot(corrected_signal)
        axes[1].plot(envelope)
        axes[2].plot(actual_sample)

    return actual_sample


if __name__ == "__main__":
    fig, axes = plt.subplots(3, 1)
    sample_rate, signal = wavfile.read('Datasets//Lys//enreg-01.wav')
    pre_process(sample_rate, signal)
    plt.show()