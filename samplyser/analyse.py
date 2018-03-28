from samplyser import pitch
from samplyser import amplitude
from samplyser import duration
from samplyser import spectrum
import madmom
import soundfile as sf
import json
import os


class Analyser:
    def __init__(self, *analyse_function):
        self.functions = analyse_function

    def __call__(self, f, output=False):
        signal, fs = sf.read(f)
        # convert to mono
        signal = madmom.audio.signal.remix(signal, 1)
        analysis = self.analyse(signal, fs)
        json = self.convert2json(f, analysis)
        if output is True:
            filename = os.path.splitext(f)[0]
            with open(filename + ".json", "w") as f:
                f.write(json)
        return json

    def analyse(self, sample, fs):
        return tuple(func(sample, fs) for func in self.functions)

    def convert2json(self, name, data):
        return json.dumps({name: data})


SimpleAnalyser = Analyser(pitch.detector.freq_from_autocorr,
                          amplitude.detector.ac_rms,
                          duration.detector.duration_detection)

ComplexAnalyser = Analyser(pitch.detector.freq_from_autocorr,
                           amplitude.detector.ac_rms,
                           duration.detector.duration_detection,
                           spectrum.spectrum.spectral_centroid,
                           spectrum.spectrum.spectral_flatness)


def analyse_bunch(directory: str, analyser: callable=SimpleAnalyser,
                  output: bool=False):
    """
    Analyse a bunch of samples.
    Arguments are:
        directory: name of the directory, where the bunch of samples is stored
        analyser: Object of type Analyser
        output: True for creating json - files. Default: False
    """
    def find_audio_files(directory):
        def is_valid_sf(f):
            return any(f.lower().endswith(
                ending.lower()) for ending in sf.available_formats())
        files = os.listdir(directory)
        return tuple(f for f in files if is_valid_sf(f))
    files = find_audio_files(directory)
    data = tuple(analyser(directory + f, output)
                 for f in files)
    return data
