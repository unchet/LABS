import sympy as sym
from first.TDMA import tdma_


def spline_interpol(x_ar, y_ar, X):
    if len(x_ar) != len(y_ar):
        return None, None
    h = [0]
    try:
        X = sym.S(X)
        for i in range(len(x_ar)):
            x_ar[i] = sym.S((x_ar[i]))
            y_ar[i] = sym.S((y_ar[i]))
    except ValueError:
        return None, None

    it = -1
    try:
        for i in x_ar:
            if X < i:
                break
            it += 1
    except TypeError:
        return None, None

    for i in range(1, len(x_ar)):
        h.append(x_ar[i] - x_ar[i-1])

    a = [0]
    c = []
    for i in range(3, len(x_ar)):
        a.append(h[i-1])
        c.append(h[i])
    c.append(0)
    b = []
    for i in range(2, len(x_ar)):
        b.append(2*(h[i-1]+h[i]))

    v = []
    for i in range(2, len(x_ar)):
        v.append(3*((y_ar[i]-y_ar[i-1])/h[i] - (y_ar[i-1]-y_ar[i-2])/h[i-1]))

    x, D = tdma_(a, b, c, v)
    ci = []
    x = x.tolist()
    for i in x:
        ci.append(i[0])
    ci.insert(0, 0.0)

    ai, bi, di = [], [], []

    for i in range(len(x_ar)-1):
        ai.append(y_ar[i])
    for i in range(1, len(x_ar)-1):
        bi.append((y_ar[i]-y_ar[i-1])/h[i] - (h[i]*(ci[i] + 2*ci[i-1])/3))
        di.append((ci[i]-ci[i-1])/(3*h[i]))

    bi.append((y_ar[-1]-y_ar[-2])/h[-1]-2*(h[-1]*ci[-1])/3)
    di.append((-ci[-1])/(3*h[-1]))

    bcd = [bi, ci, di]

    f = str(ai[it]) + '+'

    for i in range(len(bcd)):
        f += str(round(bcd[i][it], 5)) + '*' + '(x-' + str(round(x_ar[it],5)) + ')**' + str(i+1) + '+'
    f = f[:-1]

    x = sym.Symbol('x')
    try:
        fx = sym.S(f)
        res = fx.subs(x, X)
    except ValueError:
        return None, None

    return f, round(res, 5)
