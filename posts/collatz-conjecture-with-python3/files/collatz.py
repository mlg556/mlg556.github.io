import numpy as np


def collatzer(i):
    count = 0

    while i > 1:
        if i % 2 == 0:
            i = i // 2
        else:
            i = (3 * i) + 1
        count = count + 1

    return count


def collatzer_steps(i, dtype=int):
    i = int(i)

    steps = [i]

    while i > 1:
        if i % 2 == 0:
            i = i // 2
            steps.append(i)
        else:
            i = (3 * i) + 1
            steps.append(i)

    if dtype == int:
        return np.array(steps, dtype=np.int64)
    else:
        return np.array(steps, dtype=float)
