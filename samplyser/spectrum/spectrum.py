from scipy import signal
from scipy.stats.mstats import gmean
import numpy as np


def spectral_density(x, sr):
    return signal.periodogram(x, sr)


def spectral_flatness(x, sr):
    freqs, psd = spectral_density(x, sr)
    return gmean(psd) / np.mean(psd)


def spectral_centroid(x, sr):
    length = len(x)
    magnitudes = np.abs(np.fft.rfft(x))
    freqs = np.abs(np.fft.fftfreq(length, 1 / sr)
                   [:length // 2 + 1])
    return np.sum(magnitudes * freqs) / np.sum(magnitudes)
