#
#
# Provides Netlogo with analytic solutions to constrained optimization
# requirements for a Cobb-Douglass -like production function
#
#

from sympy import *
import re

l1, n1, q1, q3, q4, ef, p1, p3, p4, pn, pl, S, k, A, xa, xb, xc, xd, xe = symbols('l1 n1 q1 q3 q4 ef p1 p3 p4 pn pl S k A xa xb xc xd xe');

P, D, f, g, gradf, gradg = symbols('P D f g gradf gradg'); #cls=Function);

P = p1 * q1 - (p3 * q3 + p4 * q4 + pn * n1 + pl * l1); # production function
D = -S * ef**k; # disutility of effort
f = P + D;
g = q1 - A * q3**xa * q4**xb * n1**xc * l1**xd * ef**xe; # constraint
lam = symbols('lam'); # Lagrange multiplier

# test simplify=True
sols = solve([
    Eq(f.diff(l1), lam*g.diff(l1)),
    Eq(f.diff(n1), lam*g.diff(n1)),
    Eq(f.diff(q1), lam*g.diff(q1)),
    Eq(f.diff(q3), lam*g.diff(q3)),
    Eq(f.diff(q4), lam*g.diff(q4)),
    Eq(f.diff(ef), lam*g.diff(ef)),
    Eq(g, 0)],
    l1, n1, q1, q3, q4, ef, lam,
    minimal=True, dict=True);
sols = sols[0];

# format for NetLogo
for i, j in sols.iteritems():
    if i != lam:
        js = str(j)
        p = re.compile(r'log\(([^)]+)\)')
        js = p.sub(r'ln \1', js)
        p = re.compile(r'\*\*')
        js = p.sub(r'^', js)
        p = re.compile(r'([*+/^-])')
        js = p.sub(r' \1 ', js)
        print 'set', i, js, "\n"
