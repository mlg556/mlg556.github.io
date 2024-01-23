+++
title = "A Story of Charged Equal Spheres"
date = 2019-02-07T10:30:42+03:00
categories = ["Physics", "Mathematics"]
draft = false
+++

# Problem

Imagine three conductive spheres $A, B$ and $C$ each having charges of respectively $ 3q, 4q, \text{and } 5q $.

{{< figure src="images/ch0.png" width="350">}}

We know that if we connect all three spheres together, their charges will be the same value: which is the arithmetic mean of the system. So $ \frac{3 + 4 + 5}{3} = 4 $.

{{< figure src="images/ch1.png" width="350">}}

Now imagine we do not connect all three together, but only two at each time, alternating between the first two and the last two (i.e. $ AB, BC, AB, BC ... $). Surprisingly, if you continue this process _ad infinitum_, the charge of each sphere will converge into the arithmetic mean - even though all three spheres never touch each other at any moment.

This seemed intuitive to me, but I have decided to check it numerically with a botched up script:

```python
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
```

Here are some results to convince you:

```
[-7, -6, 0]
[-6.5, -6.5, 0]
[-6.5, -3.25, -3.25]
[-4.875, -4.875, -3.25]
[-4.875, -4.0625, -4.0625]
[-4.46875, -4.46875, -4.0625]
[-4.46875, -4.265625, -4.265625]
[-4.3671875, -4.3671875, -4.265625]
[-4.3671875, -4.31640625, -4.31640625]
[-4.341796875, -4.341796875, -4.31640625]
[-4.341796875, -4.3291015625, -4.3291015625]
[-4.33544921875, -4.33544921875, -4.3291015625]
[-4.33544921875, -4.332275390625, -4.332275390625]
[-4.3338623046875, -4.3338623046875, -4.332275390625]
[-4.3338623046875, -4.33306884765625, -4.33306884765625]
(...)
[-4.333333333333334, -4.333333333333334, -4.333333333333334]
Avg: -4.333333333333333```

[-4, 10, -1]
[3.0, 3.0, -1]
[3.0, 1.0, 1.0]
[2.0, 2.0, 1.0]
[2.0, 1.5, 1.5]
[1.75, 1.75, 1.5]
[1.75, 1.625, 1.625]
[1.6875, 1.6875, 1.625]
[1.6875, 1.65625, 1.65625]
[1.671875, 1.671875, 1.65625]
[1.671875, 1.6640625, 1.6640625]
[1.66796875, 1.66796875, 1.6640625]
[1.66796875, 1.666015625, 1.666015625]
[1.6669921875, 1.6669921875, 1.666015625]
[1.6669921875, 1.66650390625, 1.66650390625]
[1.666748046875, 1.666748046875, 1.66650390625]
[1.666748046875, 1.6666259765625, 1.6666259765625]
[1.66668701171875, 1.66668701171875, 1.6666259765625]
[1.66668701171875, 1.666656494140625, 1.666656494140625]
[1.6666717529296875, 1.6666717529296875, 1.666656494140625]
(...)
[1.6666666666666665, 1.6666666666666665, 1.6666666666666665]
Avg: 1.6666666666666667
```

After convincing myself that this is indeed the case, I have decided to come up with an analytical proof to show that the following relation holds:

$\lim_{n\to\infty} {Q_A(n) = Q_B(n) = Q_C(n)} = \frac{Q_A + Q_B + Q_C}{3}$

where $n$ is the number of steps this procedure is repeated, $Q(n)$ is the charge of any sphere at the step $ n $ and $ Q_{A, B, C} $ are the initial charges of the respective spheres. By running a similar python script but utilising symbolic math with `sympy`, we can see how the charge of the middle sphere $B$ changes with $ n $.


```
n = 1 +++ a/2 + b/2
n = 2 +++ a/4 + b/4 + c/2
n = 3 +++ 3*a/8 + 3*b/8 + c/4
n = 4 +++ 5*a/16 + 5*b/16 + 3*c/8
n = 5 +++ 11*a/32 + 11*b/32 + 5*c/16
n = 6 +++ 21*a/64 + 21*b/64 + 11*c/32
n = 7 +++ 43*a/128 + 43*b/128 + 21*c/64
n = 8 +++ 85*a/256 + 85*b/256 + 43*c/128
n = 9 +++ 171*a/512 + 171*b/512 + 85*c/256
```


By some Googling, I have found that the sequence `1 - 1 - 3 - 5 - 11 - 21 - 43 - 85 - 171 ...` is called the [Jacobsthal sequence](https://oeis.org/A001045). The [Wikipedia page](https://en.wikipedia.org/wiki/Jacobsthal_number) sums it up as: "_in simple terms, the sequence starts with 0 and 1, then each following number is found by adding the number before it to twice the number before that._"

It would seem by inspection that the charge of the middle sphere $B$ can be written as:

$$
Q_B(n) = \frac{J(n)}{2^n}a +\frac{J(n)}{2^n}b + \frac{J(n-1)}{2^{n-1}}c
$$

At this point I ran out of my wits and my `sympy` skills. So using the formula $ J(n) = 2^{n-1} - J(n-1) \Leftrightarrow J(n-1) = 2^{n-1} - J(n) $ and substituting $ J(n) $ with the closed form $ J(n) = \frac{2^n - (-1)^n}{3} $ in _MATLAB_:

```octave
syms J(n)
syms a b c

J(n) = (((2^n) - (-1)^n)) / 3
expr = (((J(n)) / (2^n)) * a) + (((J(n)) / (2^n)) * b) + ((2^(n-1) - J(n)) / (2^(n-1))) * c ;
simp_expr = simplify(expr, 'Steps', 10);

simp_expr
```

We get:
$$
\frac{a}{3}+\frac{b}{3}+\frac{c}{3}-\frac{{\left(-1\right)}^n a}{3 \cdot 2^n}-\frac{{\left(-1\right)}^n b}{3 \cdot 2^n}+\frac{2{\left(-1\right)}^n c}{3 \cdot 2^n}
$$


We finally have the $\frac{a}{3}+\frac{b}{3}+\frac{c}{3}$ we are looking for, and the right hand side converges to $0$, as $\lim_{n\to\infty} (\frac{-1}{2})^n = 0$.

# Convergence Rate

This proof was about the special case $N = 3$ spheres, but I am guessing it can be extended to any finite number of spheres as long as no sphere is left unconnected. Also the convergence rate to the arithmetic mean probably is _slower_ as the number of spheres increase. To get a sense of the convergence rate in the numerical results, I will calculate the [standard deviation](http://mathworld.wolfram.com/StandardDeviation.html) of the sphere charges at step $N$ to see how quickly it decreases. The script I wrote checks when the standard deviation is $0$ and reports the number of steps it took. Running it a few times, it seems that for the three sphere case, the standard deviation converges to $0$ at about $55-60$ steps. For the case of 10 spheres, the script ran for about 15 mins and the standard deviation failed to converge to `0` (of course checking equalities in floating-point arithmetic is a bit sloppy) after 8 million steps; so we can empirically conclude that the convergence rate indeed decreases for larger number of spheres.


# Downloads

[avg.m](files/avg.m)

[sym_avg.py](files/sym_avg.py)

[avg.py](files/avg.py)

[avg_conv.py](files/avg_conv.py)

[avg10.py](files/avg10.py)

[avg10_conv.py](files/avg10_conv.py)

