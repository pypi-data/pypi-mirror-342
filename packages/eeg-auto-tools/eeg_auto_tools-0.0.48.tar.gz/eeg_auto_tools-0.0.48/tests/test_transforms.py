import mne 

def test_cs():
    from eeg_auto_tools.transforms import ChannelSelector, Sequence
    file_path = "./tests/test-eeg.vhdr"
    raw = mne.io.read_raw(file_path, preload=True, verbose=False)
    pipeline = Sequence(
        cs = ChannelSelector(exclude=["Fpz"]),
    )
    raw_filtered = pipeline(raw, cash=False)
    assert "Fpz" not in raw_filtered.ch_names

def test_filter():
    from eeg_auto_tools.transforms import FilterBandpass, Sequence
    file_path = "./tests/test-eeg.vhdr"
    raw = mne.io.read_raw(file_path, preload=True, verbose=False)
    pipeline = Sequence(
        ffilter = FilterBandpass(l_freq=1, h_freq=45, notch_freq=50, report=True),
    )
    raw_filtered = pipeline(raw, cash=False)
    assert (pipeline.ffilter.repo_images) != {} and (pipeline.ffilter.repo_data == {})

