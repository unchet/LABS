import sympy as sym


def check_for_solution(expr, a, b):
    x = sym.Symbol('x')
    diff_x = sym.diff(expr, x)

    f = sym.S(expr)
    if f.subs(x, a) * f.subs(x, b) > 0:
        return False, None, None

    dx = 0.01
    c = a
    max_diff = 0

    while c <= b:
        eval_ = diff_x.subs(x, c)
        if abs(eval_) > abs(max_diff):
            max_diff = eval_
        c += dx

    L = 1. / max_diff.evalf()

    phi_x = "1-" + str(L) + "*(" + str(diff_x) + ")"
    phi_x = sym.S(phi_x)
    c = a
    max_diff = 0
    while c <= b:
        eval_ = abs(phi_x.subs(x, c))
        if eval_ >= 1:
            return False, None, None
        if eval_ > max_diff:
            max_diff = eval_
        c += dx

    return True, max_diff.evalf(), L


def check_newton(expr, a, b):
    x = sym.Symbol('x')
    diff_x = sym.diff(expr, x)
    diff_x2 = sym.diff(diff_x, x)

    f = sym.S(expr)
    if f.subs(x, a) * f.subs(x, b) > 0:
        return False, None

    dx = 0.01
    c = a
    eval_tmp_dx1 = diff_x.subs(x, c)
    eval_tmp_dx2 = diff_x2.subs(x, c)
    while c <= b:
        c += dx
        eval_ = diff_x.subs(x, c)
        if eval_ * eval_tmp_dx1 < 0:
            return False, None
        eval_tmp_dx1 = eval_
        eval_ = diff_x2.subs(x, c)
        if eval_ * eval_tmp_dx2 < 0:
            return False, None

    c = b
    while c >= a:
        if f.subs(x, c) * diff_x2.subs(x, c) > 0:
            return True, diff_x, c
    return False, None


def iteration_method(expr, a, b, q, L, eps):
    x_ = 0.5 * (a+b)
    x = sym.Symbol('x')

    phi_x = "x-" + str(L) + "*(" + str(expr) + ")"
    phi_x = sym.S(phi_x)
    k = 0

    condition = 1
    while condition > eps:
        k += 1
        x_k = phi_x.subs(x, x_)
        condition = abs(q/(1-q))*abs(x_k.evalf() - x_)
        x_ = x_k.evalf()

    return x_, k


def newton_method_(expr, diff_expr, x0, eps):
    x = sym.Symbol('x')
    f = sym.S(expr)
    df = sym.S(diff_expr)
    condition = f.subs(x, x0) / df.subs(x, x0)

    k = 0
    while condition > eps:
        x_ = (x0 - condition).evalf()
        condition = (f.subs(x, x_) / df.subs(x, x_)).evalf()
        x0 = x_
        k += 1

    return x0, k
