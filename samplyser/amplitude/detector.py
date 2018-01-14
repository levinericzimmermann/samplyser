import numpy as np

"""
The following functions have been written by endolith.
https://gist.github.com/endolith/2c786bf5b53b99ca3879#file-wave_analyzer-py
"""

def rms_flat(a):
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a)**2))


def ac_rms(signal, fs):
    """
    Return the RMS level of the signal after removing any fixed DC offset
    """
    return rms_flat(signal - np.mean(signal))
