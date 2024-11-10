from typing import Callable
from matplotlib import pyplot as plt
import math
import numpy as np

def square_wave_fourier(n: int) -> Callable:
    return lambda x: sum([(4/((2 * n2 + 1) * np.pi)) * math.sin((2 * n2 + 1) * np.pi * x) for n2 in range(n)])

def normalized_sin(x: float) -> float:
    return np.sin(2 * np.pi * x)


def test():
    x_range = np.linspace(0, 2, 100)
    fourier_5 = square_wave_fourier(5)
    y_range = [fourier_5(y) for y in x_range]
    plt.plot(x_range, y_range)
    plt.show()

if __name__ == '__main__':
    test()