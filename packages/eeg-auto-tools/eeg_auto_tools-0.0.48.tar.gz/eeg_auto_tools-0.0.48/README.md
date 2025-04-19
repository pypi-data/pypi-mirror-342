# EEG Auto Tools

With this package it is possible to automate routine EEG processing, ERP acquisition steps and other signal features, as well as to obtain a detailed performance report after each successive block of the pipeline has been worked out

## Installation

You can install `eeg-auto-tools` directly from PyPI:

```bash
pip install eeg-auto-tools
```

# Quick Start

```python
file = "your_file_path"
raw = mne.io.read_raw(file, preload=True)

pipeline = Sequence(
    ch_selector = ChannelSelector(exclude=['ECG', 'EOG']),
    ffilter = FilterBandpass(l_freq=0.1, h_freq=40, notch_freq=50),
    montager = SetMontage('waveguard64'),
    detector = BadChannelsDetector(method="auto"),
    rerefer = Rereference(exclude='bads'),
    ica = AutoICA(),
    interp = Interpolate(),
    r2e = Raw2Epoch(tmin=-0.15, tmax=0.6),
    bed = BadEpochsDetector(apply=True),
    baseliner = BaselineEpochs(baseline=(-0.1, 0)),
    detrender = DetrendEpochs(detrend_type="linear"),
)

epochs = pipeline(raw, cash=False)
```

# Other Info

You can visit
[my GitHub](https://github.com/MegaSear)
to read other content.

## License

This project is licensed under the Apache License 2.0
