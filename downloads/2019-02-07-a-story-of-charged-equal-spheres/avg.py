from random import randint


def mover(spheres, move):

    if move == 0:
        avg = (spheres[0] + spheres[1]) / 2
        
        spheres[0] = avg
        spheres[1] = avg

    else:
        avg = (spheres[1] + spheres[2]) / 2

        spheres[1] = avg
        spheres[2] = avg


move = 0

sph0 = randint(-10, +10)
sph1 = randint(-10, +10)
sph2 = randint(-10, +10)

spheres = [sph0, sph1, sph2]

print(spheres)

for i in range(0, 100):
    mover(spheres, move)

    move = int(not move)

    print(spheres)

print("Avg: " + str((sph0 + sph1 + sph2) / 3))
