import statistics as sta

from random import randint


def mover(spheres, move):

    avg = (spheres[move] + spheres[move+1]) / 2
    
    spheres[move] = avg
    spheres[move+1] = avg


move = 0
spheres = []

for i in range(3):
    spheres.append(randint(-10, +10))

avg = sta.mean(spheres)
devs = []
dev = 1
step = 1

while dev != 0:
    mover(spheres, move)
    
    move = (move + 1) % 2  # (mod 2) to cycle 0-1
    dev = sta.stdev(spheres)
    devs.append(dev)
    
    step = step + 1
    
print("stdev is 0 after {} steps".format(step))

