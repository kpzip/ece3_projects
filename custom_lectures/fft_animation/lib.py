from functools import cache
from typing import Callable, Sequence
from matplotlib import pyplot as plt
import math
import numpy as np
import scipy as sp


def square_wave_fourier(n: int) -> Callable[[float], float]:
    return lambda x: sum([(4 / ((2 * n2 + 1) * np.pi)) * math.sin((2 * n2 + 1) * np.pi * x) for n2 in range(n)])


def normalized_sin(x: float) -> float:
    return np.sin(2 * np.pi * x)

@cache
def fft_func(func: Callable[[float | np.ndarray[float]], float | np.ndarray[float]], x_max: float, samples: float=1200) -> Callable[[float], float]:
    T = x_max / samples
    linspace: np.ndarray[float] = np.linspace(0.0, samples * T, samples, endpoint=False)
    yf = sp.fft.fft(func(linspace))
    xf = sp.fft.fftfreq(samples, T)[:samples // 2]
    return sp.interpolate.interp1d(xf, 2.0 / samples * np.abs(yf[0:samples // 2]), bounds_error=False, fill_value="extrapolate")


def analytical_fft(amplitudes: Sequence[float], frequencies: Sequence[float]) -> Callable[[float], float]:
    if len(amplitudes) != len(frequencies):
        raise ValueError(f"`amplitudes` and `frequencies` have different lengths!, ({len(amplitudes)}, {len(frequencies)})")
    epsilon = 0.000000001
    new_amplitudes = []
    new_frequencies = []
    for i in range(len(amplitudes)):
        amp = amplitudes[i]
        freq = frequencies[i]
        new_amplitudes.append(0)
        new_frequencies.append(freq - epsilon)
        new_amplitudes.append(amp)
        new_frequencies.append(freq)
        new_amplitudes.append(0)
        new_frequencies.append(freq + epsilon)

    return sp.interpolate.interp1d(new_frequencies, new_amplitudes, bounds_error=False, fill_value=0, kind='linear')


def test():
    x_range = np.linspace(0, 2, 100)
    fourier_5 = square_wave_fourier(5)
    y_range = [fourier_5(y) for y in x_range]
    plt.plot(x_range, y_range)
    plt.show()


if __name__ == '__main__':
    test()
