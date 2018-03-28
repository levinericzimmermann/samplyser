# samplyser

Automatic creation of metadata for short mono sound files. These metadata could be
saved in the json - format.

The standard form of such generated json may be:

{SAMPLENAME: [ESTIMATED_FREQUENCY, RMS, DURATION, ...]}

current state:
-------------
* different frequency analysis - functions (using functions written by [endolith](https://gist.github.com/endolith/255291))
* rms calculation (using functions written by [endolith](https://gist.github.com/endolith/2c786bf5b53b99ca3879#file-wave_analyzer-py) and using [madmom](https://github.com/CPJKU/madmom))
* duration
* calculate spectral centroid and spectral flatness

to-do:
-------------
* add features:
  * find offset
  * find silence
  * add multichannel - support
  * add tests


installation:
-------------
```sh
  $ git clone "https://github.com/uummoo/samplyser"
  $ pip3 install -r requirements.txt
  $ pip3 install .
```

usage:
-------------

1. Analyse one sample
```python
import samplyser
sample_name = "my_harpsichord_sample.wav"
samplyser.SimpleAnalyser(sample_name)
'{"my_harpsichord_sample.wav": [65.34797345919678, 0.0751, 19.4932]}'
```

You could also save the data through the 'output' - Argument:
```python
samplyser.SimpleAnalyser(sample_name, output=True)
```
This will create a file: "my_harpsichord_sample.json".

2. Analyse a bunch of samples
```python
import samplyser
directory_name = "my_harpsichord_samples"
method = samplyser.SimpleAnalyser
samplyser.analyse_bunch(my_harpsichord_samples, method)
'[{"my_harpsichord_sample0.wav": [65.34797345919678, 0.0751, 19.4932]}, {"my_harpsichord_sample1.wav": [69.34797345919678, 0.04312, 14.4932]}]'
```

3. Writing your own analyse - function:
```python
from samplyser import Analyser, pitch
MyAnalyser = Analyser(pitch.detector.freq_from_autocorr,
                      pitch.detector.freq_from_fft)
sample_name = "my_harpsichord_sample.wav"
MyAnalyser(sample_name)
'{"harpsichord/harpsichord00_long_00.wav": [61.431530087766234, 122.00804667935573]}'
```
