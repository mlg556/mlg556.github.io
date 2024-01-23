import matplotlib.pyplot as plt
import numpy as np

from collatz import *
from timeit import default_timer as timer

start = timer()

limit = 1000000

col_y = np.zeros(limit, dtype=int)
log_y = np.zeros(limit)

x = np.arange(limit, dtype=int)

for n in x:

    col_y[n] = collatzer(x[n])
    log_y[n] = np.log2(x[n])

log_y[0] = 0  # because log2(0) gives -inf

fig, ax = plt.subplots()
ax.plot(x, col_y, '.', ms=2)
ax.plot(x, log_y, 'r')

end = timer()
print(end-start)

np.savetxt('collatz_plot_1M.txt', col_y, fmt='%d')

plt.show()
