import sympy as s

def mover(spheres, move):

    if move == 0:
        avg = (spheres[0] + spheres[1]) / 2

        spheres[0] = avg
        spheres[1] = avg

    else:
        avg = (spheres[1] + spheres[2]) / 2

        spheres[1] = avg
        spheres[2] = avg


a, b, c = s.symbols('a b c')

spheres = [a, b, c]

move = 0

for n in range (1, 10):
    mover(spheres, move)

    print("n = " + str(n) + " --- " + str(spheres[1]))

    move = int(not move)




