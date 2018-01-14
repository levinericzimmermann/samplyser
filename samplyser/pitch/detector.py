from numpy.fft import rfft
from matplotlib.mlab import find
from scipy.signal import blackmanharris, fftconvolve
from samplyser.pitch.parabolic import parabolic
import numpy as np
from scipy.signal import kaiser, decimate

"""
Frequeny detection functions written by endolith:
https://gist.github.com/endolith/255291
and
https://github.com/endolith/waveform_analysis/blob/master/waveform_analysis/freq_estimation.py
"""


def freq_from_crossings(sig, fs):
    """
    Estimate frequency by counting zero crossings
    """
    # Find all indices right before a rising-edge zero crossing
    indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    # crossings = indices

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

    # Some other interpolation based on neighboring points might be better.
    # Spline, cubic, whatever

    return fs / np.mean(np.diff(crossings))


def freq_from_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * blackmanharris(len(sig))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = parabolic(np.log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)


def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = np.diff(corr)
    start = find(d > 0)[0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = np.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px


def freq_from_hps(signal, fs):
    """
    Original by endolith:
    https://github.com/endolith/waveform_analysis/blob/master/waveform_analysis/freq_estimation.py
    Estimate frequency using harmonic product spectrum
    Low frequency noise piles up and overwhelms the desired peaks
    Doesn't work well if signal doesn't have harmonics
    """
    signal = np.asarray(signal) + 0.0

    N = len(signal)
    signal -= np.mean(signal)  # Remove DC offset

    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)

    # Get spectrum
    X = np.log(abs(rfft(windowed)))

    # Remove np.mean of spectrum (so sum is not increasingly offset
    # only in overlap region)
    X -= np.mean(X)

    # Downsample sum np.logs of spectra instead of multiplying
    hps = np.copy(X)
    for h in range(2, 9):  # TODO: choose a smarter upper limit
        dec = decimate(X, h, zero_phase=True)
        hps[:len(dec)] += dec

    # Find the peak and interpolate to get a more accurate peak
    i_peak = np.argmax(hps[:len(dec)])
    i_interp = parabolic(hps, i_peak)[0]

    # Convert to equivalent frequency
    return fs * i_interp / N  # Hz
