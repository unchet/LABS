import sympy as sym
import numpy as np
from first.Gauss import to_LU, solve_LU
# 0,1.7,3.4,5.1,6.8,8.5
# 0,1.3038,1.8439,2.2583,2.6077,2.9155


def sse(f, x_ar, y_ar):
    x = sym.Symbol('x')
    try:
        f = sym.S(f)
    except ValueError:
        return None
    sum_ = 0
    for i in range(len(x_ar)):
        fx = f.subs(x, x_ar[i])
        sum_ += (fx - y_ar[i])*(fx - y_ar[i])
    return sum_


def mnk(x_ar, y_ar):
    if len(x_ar) != len(y_ar):
        return None, None, None, None
    n = len(x_ar)
    try:
        for i in range(len(x_ar)):
            x_ar[i] = sym.S(x_ar[i])
            y_ar[i] = sym.S(y_ar[i])
    except ValueError:
        return None, None, None, None

    sum_x = sum(x_ar)
    sum_y = sum(y_ar)
    sum_x2 = 0
    sum_x3 = 0
    sum_x4 = 0
    sum_xy = 0
    sum_x2y = 0
    for i in range(len(x_ar)):
        sum_x2 += x_ar[i]*x_ar[i]
        sum_xy += x_ar[i]*y_ar[i]
        sum_x3 += x_ar[i]*x_ar[i]*x_ar[i]
        sum_x4 += x_ar[i]*x_ar[i]*x_ar[i]*x_ar[i]
        sum_x2y += x_ar[i]*x_ar[i]*y_ar[i]

    A = np.matrix([[n, sum_x],
                   [sum_x, sum_x2]])
    v = np.matrix([[sum_y],
                   [sum_xy]])

    LU = to_LU(A, v)
    x = solve_LU(LU[0], v).tolist()

    f1 = str(round(x[0][0], 5)) + '+' + str(round(x[1][0], 5)) + '*x'

    sse1 = sse(f1, x_ar, y_ar)
    if sse1 is None:
        return None, None, None, None

    A = np.matrix([[n, sum_x, sum_x2],
                   [sum_x, sum_x2, sum_x3],
                   [sum_x2, sum_x3, sum_x4]])

    v = np.matrix([[sum_y],
                   [sum_xy],
                   [sum_x2y]])

    LU = to_LU(A, v)
    x = solve_LU(LU[0], v).tolist()

    f2 = str(round(x[0][0], 5)) + '+' + str(round(x[1][0], 5)) + '*x' + '+' + str(round(x[2][0], 5)) + '*x**2'

    sse2 = sse(f2, x_ar, y_ar)
    if sse2 is None:
        return None, None, None, None

    return f1, f2, sse1, sse2
