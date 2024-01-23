import statistics as sta

from random import randint
from timeit import default_timer as timer


def mover(spheres, move):

    avg = (spheres[move] + spheres[move+1]) / 2
    
    spheres[move] = avg
    spheres[move+1] = avg


move = 0
spheres = []

for i in range(10):
    spheres.append(randint(-10, +10))

avg = sta.mean(spheres)
devs = []
dev = 1
step = 1

start = timer()

while dev != 0:
    mover(spheres, move)
    
    move = (move + 1) % 9  # (mod 9) to cycle 0-8
    dev = sta.stdev(spheres)
    devs.append(dev)
    
    step = step + 1

end = timer()
time_elapsed = end-start


print("stdev is 0 after {} steps".format(step))
print("this took {} seconds".format(time_elapsed))

