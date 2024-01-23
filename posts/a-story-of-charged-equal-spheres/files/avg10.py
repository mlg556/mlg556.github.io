from random import randint
from statistics import mean

# for 10 spheres, there are 9 moves. 1-2, 2-3, 3-4, 4-5, 5-6, 6-7, 7-8, 8-9, 9-10
# denote the "moves" as 0-8.
def mover(spheres, move):
    
    avg = (spheres[move] + spheres[move+1]) / 2
    
    spheres[move] = avg
    spheres[move+1] = avg


move = 0
spheres = []

for i in range(10):
    spheres.append(randint(-10, +10))

avg = mean(spheres)

for i in range(1000):
    mover(spheres, move)
    move = (move + 1) % 9  # (mod 9) to cycle 0-8
    print(spheres)

print("avg: " + str(avg))
