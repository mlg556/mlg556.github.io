import matplotlib.pyplot as plt
import numpy as np

from collatz import *

number = 42 ** 42

y = collatzer_steps(number, dtype=float)
x = np.arange(len(y))

fig, ax = plt.subplots()

plt.semilogy(x, y, '.', ms=4)

plt.show()
