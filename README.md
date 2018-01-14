# samplyser

Automatic analysis of soundfiles, generating Json, which contain
Metadata about the analysed Samples.

The standard form of generated json may be:

{SAMPLENAME: [ESTIMATED_FREQUENCY, DURATION, ...]}

current state:
-------------
* different frequency analysis - functions (using functions written by [endolith](https://gist.github.com/endolith/255291))

to-do:
-------------
* add features:
  * analyse spectral centroid
  * calculate rms
  * find offset
  * find silence


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
'{"my_harpsichord_sample.wav": [65.34797345919678, 19.4932]}'
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
'[{"my_harpsichord_sample0.wav": [65.34797345919678, 19.4932]}, {"my_harpsichord_sample1.wav": [69.34797345919678, 14.4932]}]'
```
