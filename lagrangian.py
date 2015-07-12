#
#
# Provides Netlogo with analytic solutions to constrained optimization
# requirements for a Cobb-Douglass -like production function
#
#

from sympy import *
import re

l1, n1, ef, q1, p1, pn, pl, S, k, A, xe, xn, xl, lam = symbols('l1, n1, ef, q1, p1, pn, pl, S, k, A, xe, xn, xl, lam')

P, D, f, g, gradf, gradg = symbols('P D f g gradf gradg'); #cls=Function);

productNum = 2 # number of products...over 5 is very computationally
               # expensive
productPrices = symbols('p3:%d'%(productNum+3), seq=True)
productQuants = symbols('q3:%d'%(productNum+3), seq=True)
productQuantExps = symbols('x3:%d'%(productNum+3), seq=True)
productSum = 0
productQuantProd = 1
toSolveFor = (lam, l1, n1, ef, q1) + productQuants

for i in range(productNum):
    productSum += productPrices[i] * productQuants[i]
    productQuantProd *= productQuants[i]**productQuantExps[i]

P = p1 * q1 - (productSum + pn * n1 + pl * l1) # production function
D = -S * ef**k # disutility of effort
f = P + D # to optimize
g = q1 - A * ef**xe * n1**xn * l1**xl * productQuantProd # constraint


# set up all the optimization equations, and avoid appending lam, the
# Lagrangian multiplier
lagrangianEqs = [Eq(g, 0)]
for i in range(1, len(toSolveFor)): 
    lagrangianEqs.append(
        Eq(f.diff(toSolveFor[i]),
        lam*g.diff(toSolveFor[i])))

# solve the Lagrangian
sols = solve(lagrangianEqs, toSolveFor,
    minimal=True, dict=True);
sols = sols[0]

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
