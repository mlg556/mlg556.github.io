---
layout: post
title:  "A Story of Charged Equal Spheres"
date:   2019-02-07 10:30:42 +0300
comments: true
categories: [Physics, Mathematics]
---

Imagine three conductive spheres $$ A, B, \text{and } C $$ each having charges of respectively $$ 3q, 4q, \text{and } 5q $$.

<img src="/assets/2019-02-07-a-story-of-charged-equal-spheres/ch0.png" width="350">

We know that if we connect all three spheres together, their charges will be the same value: which is the arithmetic mean of the system. So $$ \frac{3 + 4 + 5}{3} = 4 $$.

<img src="/assets/2019-02-07-a-story-of-charged-equal-spheres/ch1.png" width="350">

Now imagine we do not connect all three together, but only two at each time, alternating between the first two and the last two (i.e. $$ AB, BC, AB, BC ... $$). Surprisingly, if you continue this process _ad infinitum_, the charge of each sphere will converge into the arithmetic mean - even though all three spheres never touch each other at any moment.

This seemed intuitive to me, but I have decided to check it numerically with a botched up script:

{% highlight python %}
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

{% endhighlight %}

Here are some results to convince you:

{% highlight python %}
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
Avg: -4.333333333333333
{% endhighlight %}

{% highlight python %}
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
{% endhighlight %}

After convincing myself that this is indeed the case, I have decided to come up with an analytical proof to show that the following relation holds:

$$ \lim_{n\to\infty} {Q_A(n) = Q_B(n) = Q_C(n)} = \frac{Q_A + Q_B + Q_C}{3} $$

where $$n$$ is the number of steps this procedure is repeated, $$Q(n)$$ is the charge of any sphere at the step $$ n $$ and $$ Q_{A, B, C} $$ are the initial charges of the respective spheres. By running a similar python script but utilising symbolic math with `sympy`, we can see how the charge of the middle sphere $$B$$ changes with $$ n $$.

{% highlight python %}
n = 1 --- a/2 + b/2
n = 2 --- a/4 + b/4 + c/2
n = 3 --- 3*a/8 + 3*b/8 + c/4
n = 4 --- 5*a/16 + 5*b/16 + 3*c/8
n = 5 --- 11*a/32 + 11*b/32 + 5*c/16
n = 6 --- 21*a/64 + 21*b/64 + 11*c/32
n = 7 --- 43*a/128 + 43*b/128 + 21*c/64
n = 8 --- 85*a/256 + 85*b/256 + 43*c/128
n = 9 --- 171*a/512 + 171*b/512 + 85*c/256
{% endhighlight %}

By some Googling, I have found that the sequence `1 - 1 - 3 - 5 - 11 - 21 - 43 - 85 - 171 ...` is called the [Jacobsthal sequence](https://oeis.org/A001045). The [Wikipedia page](https://en.wikipedia.org/wiki/Jacobsthal_number) sums it up as: "_in simple terms, the sequence starts with 0 and 1, then each following number is found by adding the number before it to twice the number before that._"

It would seem by inspection that the charge of the middle sphere $$B$$ can be written as:

$$

Q_B(n) = \frac{J(n)}{2^n}a +\frac{J(n)}{2^n}b + \frac{J(n-1)}{2^{n-1}}c

$$

At this point I ran out of my wits and my `sympy` skills. So using the formula $$ J(n) = 2^{n-1} - J(n-1) \Leftrightarrow J(n-1) = 2^{n-1} - J(n) $$ and substituting $$ J(n) $$ with the closed form $$ J(n) = \frac{2^n - (-1)^n}{3} $$ in _MATLAB_:

{% highlight MATLAB %}

syms J(n)
syms a b c

J(n) = (((2^n) - (-1)^n)) / 3
expr = (((J(n)) / (2^n)) * a) + (((J(n)) / (2^n)) * b) + ((2^(n-1) - J(n)) / (2^(n-1))) * c ;
simp_expr = simplify(expr, 'Steps', 10);

simp_expr

{% endhighlight %}

We get:
{% raw %}

$$

\frac{a}{3}+\frac{b}{3}+\frac{c}{3}-\frac{{\left(-1\right)}^n\,a}{3\,2^n}-\frac{{\left(-1\right)}^n\,b}{3\,2^n}+\frac{2\,{\left(-1\right)}^n\,c}{3\,2^n}

$$

{% endraw %}

We finally have the $$ \frac{a}{3}+\frac{b}{3}+\frac{c}{3} $$ we are looking for, but I do not see how the rest goes to $$ 0 $$ as $$ \lim_{n\to\infty} $$, since there are terms like $$ (-1)^n $$ which would prevent it from converging.

## Downloads

[avg.py][1]

[sym_avg.py][2]

[avg.m][3]


[1]:{{ site.url }}/downloads/2019-02-07-a-story-of-charged-equal-spheres/avg.py
[2]:{{ site.url }}/downloads/2019-02-07-a-story-of-charged-equal-spheres/sym_avg.py
[3]:{{ site.url }}/downloads/2019-02-07-a-story-of-charged-equal-spheres/avg.m
