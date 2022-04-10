import sympy as sym
import numpy as np
from math import sqrt


# 0.1*x1^2+x1+0.2*x2^2-0.3
# 0.2*x1^2+x2-0.1*x1*x2-0.7
def norm_vector(v):
    sum_ = 0
    for i in range(len(v)):
        sum_ += v[i] * v[i]

    return sqrt(sum_)


def newton_method_systems_(expr1, expr2, a1, b1, a2, b2, eps):
    x1_old = 0.5 * (a1 + b1)
    x2_old = 0.5 * (a2 + b2)

    x1 = sym.Symbol('x1')
    x2 = sym.Symbol('x2')

    f1 = sym.S(expr1)
    f2 = sym.S(expr2)

    df1x1 = sym.diff(f1, x1)
    df1x2 = sym.diff(f1, x2)
    df2x1 = sym.diff(f2, x1)
    df2x2 = sym.diff(f2, x2)

    condition = 1
    k = 0

    while condition > eps:
        J = np.array(
            [[(df1x1.subs([(x1, x1_old), (x2, x2_old)])).evalf(), (df1x2.subs([(x1, x1_old), (x2, x2_old)])).evalf()],
             [(df2x1.subs([(x1, x1_old), (x2, x2_old)])).evalf(), (df2x2.subs([(x1, x1_old), (x2, x2_old)])).evalf()]])

        A1 = np.array(
            [[(f1.subs([(x1, x1_old), (x2, x2_old)])).evalf(), (df1x2.subs([(x1, x1_old), (x2, x2_old)])).evalf()],
             [(f2.subs([(x1, x1_old), (x2, x2_old)])).evalf(), (df2x2.subs([(x1, x1_old), (x2, x2_old)])).evalf()]])

        A2 = np.array(
            [[(df1x1.subs([(x1, x1_old), (x2, x2_old)])).evalf(), (f1.subs([(x1, x1_old), (x2, x2_old)])).evalf()],
             [(df2x1.subs([(x1, x1_old), (x2, x2_old)])).evalf(), (f2.subs([(x1, x1_old), (x2, x2_old)])).evalf()]])

        try:
            x1_new = x1_old - ((A1[0, 0] * A1[1, 1] - A1[0, 1] * A1[1, 0]) / (J[0, 0] * J[1, 1] - J[0, 1] * J[1, 0]))
            x2_new = x2_old - ((A2[0, 0] * A2[1, 1] - A2[0, 1] * A2[1, 0]) / (J[0, 0] * J[1, 1] - J[0, 1] * J[1, 0]))
        except ZeroDivisionError:
            return None, None, 0

        v = np.array([x1_new - x1_old, x2_new - x2_old])
        condition = norm_vector(v)

        x1_old = x1_new
        x2_old = x2_new
        k += 1

    return x1_old, x2_old, k


def check_iter_(expr1, expr2, a1, b1, a2, b2):
    x1 = sym.Symbol('x1')
    x2 = sym.Symbol('x2')

    phi1 = "x1+" + expr1
    phi2 = "x2+" + expr2

    phi1 = sym.S(phi1)
    phi2 = sym.S(phi2)

    dphi1x1 = sym.diff(phi1, x1)
    dphi1x2 = sym.diff(phi1, x2)
    dphi2x1 = sym.diff(phi2, x1)
    dphi2x2 = sym.diff(phi2, x2)

    ca1 = a1
    dx = 0.01
    max1 = 0
    while ca1 < b1:
        ca2 = a2
        while ca2 < b2:
            tmp1 = dphi1x1.subs([(x1, ca1), (x2, ca2)])
            tmp2 = dphi1x2.subs([(x1, ca1), (x2, ca2)])
            max1 = max([tmp1, tmp2, max1], key=abs)
            ca2 += dx
        ca1 += dx

    ca1 = a1

    max2 = 0
    while ca1 < b1:
        ca2 = a2
        while ca2 < b2:
            tmp1 = dphi2x1.subs([(x1, ca1), (x2, ca2)])
            tmp2 = dphi2x2.subs([(x1, ca1), (x2, ca2)])
            max2 = max([tmp1, tmp2, max2], key=abs)
            ca2 += dx
        ca1 += dx

    return True, [1./max1, 1./max2]


def iter_method_systems_(expr1, expr2, q_l, a1, b1, a2, b2, eps):
    x1_old = 0.5*(a1 + b1)
    x2_old = 0.5*(a2 + b2)

    x1 = sym.Symbol('x1')
    x2 = sym.Symbol('x2')
    q1 = q_l[0]
    q2 = q_l[1]

    phi1 = "x1-" + str(q1) + "*(" + str(expr1) + ")"
    phi2 = "x2-" + str(q2) + "*(" + str(expr2) + ")"

    print(phi1)
    print(phi2)

    phi1 = sym.S(phi1)
    phi2 = sym.S(phi2)

    condition1 = 1
    condition2 = 1
    k = 0

    while condition1 > eps or condition2 > eps:
        x1_new = (phi1.subs([(x1, x1_old), (x2, x2_old)])).evalf()
        x2_new = (phi2.subs([(x1, x1_old), (x2, x2_old)])).evalf()
        if abs(x1_new) > 10e10 or abs(x2_new) > 10e10:
            return None, None, 0
        v = np.array([x1_new - x1_old, x2_new - x2_old])
        condition1 = (q1 / (1-q1))*norm_vector(v)
        condition2 = (q2 / (1-q2))*norm_vector(v)

        x1_old = x1_new
        x2_old = x2_new
        k += 1

    return x1_old, x2_old, k
