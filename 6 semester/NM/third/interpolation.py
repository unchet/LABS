import sympy as sym


def lagrange(expr, X, x_ar):
    x = sym.Symbol('x')
    try:
        f = sym.S(expr)
    except ValueError:
        return None, None
    w = ''
    L = sym.S(0)
    L_str = ''
    for xi in x_ar:
        w += "(x-"+xi+")*"
    w = w[:-1]
    try:
        w = sym.S(w)
    except ValueError:
        return None, None
    dw = sym.diff(w, x)

    for xi in x_ar:
        try:
            fi = f.subs(x, xi)
            dwi = dw.subs(x, xi)
        except ValueError:
            return None, None
        fi_dwi = fi / dwi
        x_xi = 'x-'+xi
        coef = (fi_dwi * (w / sym.S(x_xi))).evalf()
        L += coef
        if coef != 0:
            L_str += str(coef) + '\n'

    res = L.subs(x, X)
    return L_str, res.round(5)


def divided_difference(f1, f2, arg1, arg2):
    return (f1 - f2) / (arg1 - arg2)


def newton(expr, X, x_ar):
    x = sym.Symbol('x')
    try:
        f = sym.S(expr)
    except ValueError:
        return None, None

    x_xi = []
    for xi in x_ar:
        x_xi.append('(x-'+xi+')*')
    x_xi[-1] = x_xi[-1][:-1]

    # for i in range(len(x_ar)):
    #     x_ar[i] = float(x_ar[i])

    fi2 = []
    for i in range(len(x_ar)-1):
        try:
            fi2.append([divided_difference((f.subs(x, x_ar[i])).evalf(), (f.subs(x, x_ar[i+1])).evalf(),
                                           sym.S(x_ar[i]), sym.S(x_ar[i+1])), sym.S(x_ar[i]), sym.S(x_ar[i+1])])
        except ValueError:
            return None, None

    fi3 = []
    for i in range(len(fi2)-1):
        try:
            fi3.append([divided_difference(fi2[i][0], fi2[i+1][0], fi2[i][1], fi2[i+1][2]), fi2[i][1], fi2[i+1][2]])
        except ValueError:
            return None, None

    fi4 = []
    for i in range(len(fi3)-1):
        try:
            fi4.append([divided_difference(fi3[i][0], fi3[i+1][0], fi3[i][1], fi3[i+1][2]), fi3[i][1], fi3[i+1][2]])
        except ValueError:
            return None, None

    fi = [fi2, fi3, fi4]
    try:
        P = str(((f.subs(x, x_ar[0])).evalf()).round(5))
        for i in range(len(x_ar)-1):
            P += '+' + ''.join(x_xi[:i+1]) + str((fi[i][0][0]).round(5))
        P = (sym.S(P)).evalf()
        res = (P.subs(x, X)).round(5)
        return P, res
    except ValueError:
        return None, None

