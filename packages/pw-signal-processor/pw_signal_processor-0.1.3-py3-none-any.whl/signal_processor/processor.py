import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class SignalProcessor:
    def __init__(self, window_size=5, alpha=0.1):
        """
        Initialize the SignalProcessor.

        Args:
            window_size (int): Window size for moving average.
            alpha (float): Smoothing factor for low-pass filter.
        """
        self.window_size = window_size
        self.alpha = alpha
        self._buffer = []
        self._prev_filtered_value = 0.0

    def moving_average(self, new_value):
        """
        Update the buffer with new_value and compute moving average.

        Args:
            new_value (float): New data point.

        Returns:
            float: Current moving average.
        """
        self._buffer.append(new_value)
        if len(self._buffer) > self.window_size:
            self._buffer.pop(0)
        return sum(self._buffer) / len(self._buffer)

    def low_pass_filter(self, new_value):
        """
        Apply exponential low-pass filter to new_value.

        Args:
            new_value (float): New data point.

        Returns:
            float: Filtered value.
        """
        filtered_value = self.alpha * new_value + (1 - self.alpha) * self._prev_filtered_value
        self._prev_filtered_value = filtered_value
        return filtered_value

    def reset(self):
        """
        Reset the internal buffer and previous filtered value.
        """
        self._buffer = []
        self._prev_filtered_value = 0.0

    def plot_signals(self, time, signal, ma_output, lp_output, x_range=None):
        """
        Plot the original noisy signal, moving average output, and low-pass filter output.

        Args:
            time (array-like): Time axis data.
            signal (array-like): Original noisy signal.
            ma_output (array-like): Moving average output.
            lp_output (array-like): Low-pass filter output.
            x_range (tuple, optional): (start, end) range for x-axis to zoom in.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(time, signal, label='Noisy Signal', alpha=0.5)
        plt.plot(time, ma_output, label='Moving Average', linewidth=2)
        plt.plot(time, lp_output, label='Low Pass Filter', linewidth=2)
        plt.legend()
        plt.title('Signal Processor Demo')
        plt.xlabel('Time (second)')
        plt.ylabel('Amplitude')
        plt.grid()

        if x_range is not None:
            plt.xlim(x_range)
            mask = (np.array(time) >= x_range[0]) & (np.array(time) <= x_range[1])
            y_values = np.concatenate([
                np.array(signal)[mask],
                np.array(ma_output)[mask],
                np.array(lp_output)[mask]
            ])
            y_min, y_max = y_values.min(), y_values.max()
            margin = 0.1 * (y_max - y_min)
            plt.ylim(y_min - margin, y_max + margin)
        plt.show()

    def compute_fft(self, signal, dt):
        """
        Compute the FFT of a time-domain signal.

        Args:
            signal (array-like): Time-domain signal.
            dt (float): Sampling interval in seconds.

        Returns:
            tuple: (freq, Y) where freq is frequency axis (Hz), and Y is FFT result (complex).
        """
        n = len(signal)
        k = np.arange(n)
        Fs = 1.0 / dt
        T = n / Fs
        freq = k / T
        freq = freq[:n // 2]
        Y = np.fft.fft(signal) / n
        Y = Y[:n // 2]
        return freq, Y

    def plot_fft(self, time, signal, dt=None, freq_limit=(0, 20)):
        """
        Plot the time-domain signal and its frequency spectrum side by side.

        Args:
            time (array-like): Time axis data.
            signal (array-like): Time-domain signal.
            dt (float, optional): Sampling interval. If None, inferred from time.
            freq_limit (tuple, optional): Frequency axis limits for the FFT plot.
        """
        if dt is None:
            dt = time[1] - time[0]

        freq, Y = self.compute_fft(signal, dt)
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        ax[0].plot(time, signal)
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Amplitude')
        ax[0].grid(True)
        ax[1].plot(freq, np.abs(Y), linestyle='', marker='^', color='red')
        ax[1].set_xlabel('Frequency (Hz)')
        ax[1].set_ylabel('|Y(freq)|')
        ax[1].vlines(freq, [0], np.abs(Y))
        ax[1].set_xlim(freq_limit)
        ax[1].grid(True)
        plt.tight_layout()
        plt.show()

    def draw_stft(self, f, t, Zxx):
        """
        Draw the magnitude of a Short-Time Fourier Transform.

        Args:
            f (array-like): Frequency bins.
            t (array-like): Time bins.
            Zxx (2D array): STFT complex result.
        """
        plt.figure(figsize=(12, 5))
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=1, shading='gouraud')
        plt.title('STFT Magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.ylim([0, 20])
        plt.colorbar(label='Magnitude')
        plt.show()

    def calc_stft(self, sin_concat, Fs, nperseg):
        """
        Compute and plot the STFT of a signal.

        Args:
            sin_concat (array-like): Input time-domain signal.
            Fs (float): Sampling frequency (Hz).
            nperseg (int): Length of each segment for STFT.
        """
        f, t, Zxx = signal.stft(sin_concat, Fs, nperseg=nperseg)
        self.draw_stft(f, t, Zxx)
