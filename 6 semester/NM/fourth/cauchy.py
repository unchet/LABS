import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
from third.integrate import boost_acc


def euler_method(f, lc1, lc2, lx, rx, h):
    lc1 = sym.S(lc1)
    lc2 = sym.S(lc2)
    lx = sym.S(lx)
    rx = sym.S(rx)
    h = sym.S(h)
    x, y, y1, y2, z, z1 = sym.symbols('x y y1 y2 z z1')
    parse = parse_expr(f, local_dict={"y2": z1, "y1": z})

    f = sym.S(parse)
    f = sym.S(sym.solve(f, z1)[0])

    xi, yi, zi = [], [], []
    xi.append(lx)
    yi.append(lc1)
    zi.append(lc2)

    for i in range((rx - lx) // h + 1):
        xi.append(round(xi[-1] + h, 5))
        yi.append(round(yi[-1] + h * zi[-1], 5))
        zi.append(round(zi[-1] + h * f.subs([(x, xi[-2]), (y, yi[-2]), (z, zi[-1])]), 5))

    return xi, yi, zi


def runge_kutta(f, lc1, lc2, lx, rx, h):
    lc1 = sym.S(lc1)
    lc2 = sym.S(lc2)
    lx = sym.S(lx)
    rx = sym.S(rx)
    h = sym.S(h)
    x, y, y1, y2, z, z1 = sym.symbols('x y y1 y2 z z1')
    parse = parse_expr(f, local_dict={"y2": z1, "y1": z})

    f = sym.S(parse)
    f = sym.S(sym.solve(f, z1)[0])

    xi, yi, zi = [], [], []
    xi.append(lx)

    for i in range((rx - lx) // h + 1):
        xi.append(xi[-1] + h)

    yi.append(lc1)
    zi.append(lc2)
    # y2-4*x*y1+(4*x**2-2)*y

    for j in range(len(xi) - 1):
        Ky, Kz = [], []
        Ky.append(zi[j])
        Kz.append(f.subs([(x, xi[j]), (y, yi[j]), (z, zi[j])]))
        for i in range(2):
            Ky.append(zi[j] + (h / 2) * Kz[i])
            Kz.append(f.subs([(x, xi[j] + h / 2), (y, yi[j] + (h / 2) * Ky[i]), (z, zi[j] + (h / 2) * Kz[i])]))
        Ky.append(zi[j] + h * Kz[-1])
        Kz.append(f.subs([(x, xi[j] + h), (y, yi[j] + h * Ky[-2]), (z, zi[j] + h * Kz[-1])]))
        yi.append(yi[j] + (h / 6) * (Ky[0] + 2 * Ky[1] + 2 * Ky[2] + Ky[3]))
        zi.append(zi[j] + (h / 6) * (Kz[0] + 2 * Kz[1] + 2 * Kz[2] + Kz[3]))

    return xi[1:], yi[1:], zi[1:]


def adams(expr, lc1, lc2, lx, rx, h):
    xi, yi, zi = runge_kutta(expr, lc1, lc2, lx, rx, h)
    n = len(xi)
    xi, yi, zi = xi[:4], yi[:4], zi[:4]

    h = sym.S(h)
    x, y, y1, y2, z, z1 = sym.symbols('x y y1 y2 z z1')
    parse = parse_expr(expr, local_dict={"y2": z1, "y1": z})

    f = sym.S(parse)
    f = sym.S(sym.solve(f, z1)[0])

    for i in range(3, n - 1):
        zi.append(zi[i] + h * (55 * f.subs([(x, xi[i]), (y, yi[i]), (z, zi[i])]) -
                               59 * f.subs([(x, xi[i-1]), (y, yi[i-1]), (z, zi[i-1])]) +
                               37 * f.subs([(x, xi[i-2]), (y, yi[i-2]), (z, zi[i-2])]) -
                               9 * f.subs([(x, xi[i-3]), (y, yi[i-3]), (z, zi[i-3])]))/24)

        yi.append(yi[i] + h * (55 * zi[i] - 59 * zi[i-1] + 37 * zi[i-2] - 9 * zi[i-3])/24)
        xi.append(xi[i]+h)

    return xi, yi, zi


# def runge_romberg(f1, f2, h1, h2):

