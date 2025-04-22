# PinkLAB Signal Processor

A simple Python package providing a moving average, a first-order low-pass filter, FFT analysis, and STFT analysis. This project is brought to you by PinkWink from PinkLAB, aiming to help everyone easily integrate signal-processing functions in their applications or data-processing workflows.

## Features

1. **Moving Average**: Compute the average of the most recent N samples (sliding window).
2. **First-Order Low-Pass Filter**: Smooth out noisy data with an exponential moving average.
3. **FFT Analysis**: Compute and visualize the frequency spectrum of time-domain signals.
4. **STFT Analysis**: Compute and display the time–frequency representation of signals using Short-Time Fourier Transform (spectrogram).

All methods are simple to configure and use, reducing complexity for quick results in signal processing or time-series data smoothing.

---

## Installation

### From PyPI (recommended)

```bash
pip install pw-signal-processor
```

### From source

1. Clone (or download) this repository.
2. Navigate to the project root (where `setup.py` or `pyproject.toml` is located).
3. Install locally with:

```bash
pip install -e .
```

---

## Usage

Once installed, import and create an instance of the `SignalProcessor` class. Configure the `window_size` and `alpha` parameters as needed:

```python
from signal_processor import SignalProcessor

# Create a processor with a window size of 5 and alpha=0.2 for the low-pass filter
sp = SignalProcessor(window_size=5, alpha=0.2)
```

### Moving Average & Low-Pass Filter

```python
data = [10, 12, 13, 20, 22, 21, 18, 15]

for val in data:
    ma_val = sp.moving_average(val)
    lp_val = sp.low_pass_filter(val)
    print(f"Input: {val} | Moving Avg: {ma_val:.2f} | Low Pass: {lp_val:.2f}")
```

### FFT Analysis

#### `compute_fft(signal, dt)`

Compute the FFT of a time-domain signal.

- **Args**:
  - `signal` (array-like): Time-domain signal.
  - `dt` (float): Sampling interval in seconds.
- **Returns**:
  - `freq` (numpy array): Frequency bins (Hz).
  - `Y` (numpy array): FFT result (complex spectrum).

```python
import numpy as np
# Example signal: sinusoids combined
time = np.linspace(0, 1, 1000)
signal = np.sin(2*np.pi*5*time) + 0.5*np.sin(2*np.pi*12*time)
dt = time[1] - time[0]

freq, Y = sp.compute_fft(signal, dt)
print(freq[:5])     # first few frequency bins
print(np.abs(Y[:5]))  # magnitude of FFT
```

#### `plot_fft(time, signal, dt=None, freq_limit=(0, 20))`

Plot the time-domain signal and its frequency spectrum side by side.

- **Args**:
  - `time` (array-like): Time axis data.
  - `signal` (array-like): Time-domain signal.
  - `dt` (float, optional): Sampling interval. If `None`, inferred from `time`.
  - `freq_limit` (tuple, optional): Frequency axis limits for FFT plot.

```python
# Using the same signal from above
dt = None  # let the method infer from `time`
sp.plot_fft(time, signal, dt=dt, freq_limit=(0, 20))
```

### STFT Analysis

#### `draw_stft(f, t, Zxx)`

Plot the magnitude spectrogram from STFT results.

- **Args**:
  - `f` (array-like): Frequency bins (Hz).
  - `t` (array-like): Time bins (sec).
  - `Zxx` (2D array): STFT complex output.

```python
# Assuming f, t, Zxx obtained from calc_stft
draw_stft(f, t, Zxx)
```

#### `calc_stft(signal, Fs, nperseg)`

Compute the STFT of a signal and plot its spectrogram.

- **Args**:
  - `signal` (array-like): Input time-domain signal.
  - `Fs` (float): Sampling frequency in Hz.
  - `nperseg` (int): Number of samples per STFT segment.

```python
import numpy as np
# Generate a sample signal
Fs = 100.0  # Sampling frequency
time = np.linspace(0, 2, int(2*Fs), endpoint=False)
sin_concat = np.sin(2*np.pi*10*time) + 0.5*np.sin(2*np.pi*20*time)

# Compute and display STFT
sp.calc_stft(sin_concat, Fs, nperseg=128)
```

---

## Example

```python
import numpy as np
import matplotlib.pyplot as plt
from signal_processor import SignalProcessor

# Generate some noisy sinusoidal data
time = np.linspace(0, 10, 100)
noise = np.random.normal(0, 0.5, size=time.shape)
signal = np.sin(time) + noise

# Initialize the SignalProcessor
sp = SignalProcessor(window_size=5, alpha=0.1)

# Moving average and low-pass
ma_output = []
lp_output = []
for val in signal:
    ma_output.append(sp.moving_average(val))
    lp_output.append(sp.low_pass_filter(val))

# Plot time-domain filters
plt.figure(figsize=(10,6))
plt.plot(time, signal, label='Noisy Signal', alpha=0.5)
plt.plot(time, ma_output, label='Moving Average', linewidth=2)
plt.plot(time, lp_output, label='Low Pass Filter', linewidth=2)
plt.legend()
plt.title('My-Signal-Processor Demo')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()

# FFT demonstration
dt = time[1] - time[0]
sp.plot_fft(time, signal, dt=dt, freq_limit=(0, 20))

# STFT demonstration
Fs = 100.0
sp.calc_stft(signal, Fs, nperseg=64)
```

---

## Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the project.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a Pull Request back to the main repository.

We'll review your PR as soon as possible.

---

## License

This project is licensed under the MIT License - feel free to modify and use it as you see fit.

---

## Contact

If you have any questions or feedback, feel free to reach out:

- PinkWink from PinkLAB
- GitHub: [https://github.com/pinklab-art/signal\_processor](https://github.com/pinklab-art/signal_processor)
- Email: [pinkwink@pinklab.art](mailto\:pinkwink@pinklab.art)

Happy filtering and analysis!

