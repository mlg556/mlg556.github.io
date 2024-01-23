import matplotlib.pyplot as plt
import numpy as np

from collatz import *
from timeit import default_timer as timer

start = timer()

limit = 1000

y = np.zeros(limit, dtype=int)
x = np.arange(limit, dtype=int)

for n in x:
    y[n] = collatzer(x[n])

fig, ax = plt.subplots()
ax.plot(x, y, '.', ms=4)

end = timer()
print(end-start)

plt.show()



