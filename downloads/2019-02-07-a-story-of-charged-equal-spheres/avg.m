syms J(n);
syms a b c;

J(n) = (((2^n) - (-1)^n)) / 3;
expr = (((J(n)) / (2^n)) * a) + (((J(n)) / (2^n)) * b) + ((2^(n-1) - J(n)) / (2^(n-1))) * c;
simp_expr = simplify(expr, 'Steps', 10);

simp_expr

latex(simp_expr)