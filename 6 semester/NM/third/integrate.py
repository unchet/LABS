import sympy as sym


def evaluate(f, X0, Xk, h):
    x = sym.Symbol('x')
    try:
        f = sym.S(f)
    except ValueError:
        return None, None, None
    f_rec = sym.S(0)
    f_tr = f.subs(x, X0) / 2
    f_simp = f.subs(x, X0)
    start = X0
    while start < Xk:
        f_rec += f.subs(x, (start+start+h)/2)
        start += h
    f_rec *= h

    start = X0 + h
    while start < Xk:
        f_tr += f.subs(x, start)
        start += h
    f_tr += f.subs(x, Xk)/2
    f_tr *= h

    it = 1
    start = X0 + h
    while start < Xk:
        if it % 2:
            coef = 4
        else:
            coef = 2
        f_simp += f.subs(x, start) * coef
        it += 1
        start += h

    f_simp += f.subs(x, Xk)
    f_simp *= h/3

    return f_rec, f_tr, f_simp


def boost_acc(f1, f2, k, p):
    return f1 + (f1-f2)/(k**p-1)


def num_integrate(f, X0, Xk, h1, h2):
    try:
        X0, Xk, h1, h2 = sym.S(X0), sym.S(Xk), sym.S(h1), sym.S(h2)
    except ValueError:
        return None, None, None, None
    f_rec1, f_tr1, f_simp1 = evaluate(f, X0, Xk, h1)
    if f_rec1 is None:
        return None, None, None, None
    f_rec2, f_tr2, f_simp2 = evaluate(f, X0, Xk, h2)
    if f_rec2 is None:
        return None, None, None, None

    x = sym.Symbol('x')
    Integral = sym.integrate(f, (x, X0, Xk))

    f_rec = boost_acc(f_rec1, f_rec2, h2/h1, 2)
    f_tr = boost_acc(f_tr1, f_tr2, h2/h1, 2)
    f_simp = boost_acc(f_simp1, f_simp2, h2/h1, 4)

    drec = abs(Integral - f_rec)
    dtr = abs(Integral - f_tr)
    dsimp = abs(Integral - f_simp)

    return [f_rec1, f_rec2, f_rec, drec], [f_tr1, f_tr2, f_tr, dtr], [f_simp1, f_simp2, f_simp, dsimp], Integral
