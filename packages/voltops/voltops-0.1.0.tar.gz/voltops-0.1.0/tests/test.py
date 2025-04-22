import pytest
import numpy as np
from voltops.formulas.basic import BasicFormulas
from voltops.signal_processing.filters import Filters
from voltops.signal_processing.transforms import Transforms

def test_ohms_law():
    assert BasicFormulas.ohms_law(current=2, resistance=5) == 10
    assert BasicFormulas.ohms_law(voltage=10, resistance=5) == 2
    assert BasicFormulas.ohms_law(voltage=10, current=2) == 5

def test_power():
    assert BasicFormulas.power(voltage=10, current=2) == 20

def test_frequency_spectrum():
    t = np.linspace(0, 1, 1000, endpoint=False)
    signal = np.sin(2 * np.pi * 10 * t)
    freqs, amps = Transforms.frequency_spectrum(signal, sampling_rate=1000)
    assert len(freqs) == 500
    assert len(amps) == 500

def test_low_pass_filter():
    t = np.linspace(0, 1, 1000, endpoint=False)
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    filtered_signal = Filters.low_pass_filter(signal, cutoff=15, sampling_rate=1000)
    assert len(filtered_signal) == len(signal)
    assert np.all(np.abs(filtered_signal) <= 1.5)

def test_high_pass_filter():
    t = np.linspace(0, 1, 1000, endpoint=False)
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    filtered_signal = Filters.high_pass_filter(signal, cutoff=15, sampling_rate=1000)
    assert len(filtered_signal) == len(signal)
    assert np.all(np.abs(filtered_signal) <= 1.5)

def test_band_pass_filter():
    t = np.linspace(0, 1, 1000, endpoint=False)
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    filtered_signal = Filters.band_pass_filter(signal, lowcut=5, highcut=15, sampling_rate=1000)
    assert len(filtered_signal) == len(signal)
    assert np.all(np.abs(filtered_signal) <= 1.5)

def test_band_stop_filter():
    t = np.linspace(0, 1, 1000, endpoint=False)
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    filtered_signal = Filters.band_stop_filter(signal, lowcut=5, highcut=15, sampling_rate=1000)
    assert len(filtered_signal) == len(signal)
    assert np.all(np.abs(filtered_signal) <= 1.5)

if __name__ == "__main__":
    pytest.main()