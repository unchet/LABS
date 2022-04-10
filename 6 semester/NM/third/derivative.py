import sympy as sym


def num_derivative(x_ar, y_ar, X):
    if len(x_ar) != len(y_ar):
        return None, None
    try:
        X = sym.S(X)
        for i in range(len(x_ar)):
            x_ar[i] = sym.S(x_ar[i])
            y_ar[i] = sym.S(y_ar[i])
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

    left = (y_ar[it]-y_ar[it-1])/(x_ar[it]-x_ar[it-1])
    right = (y_ar[it+1]-y_ar[it])/(x_ar[it+1]-x_ar[it])

    dyx = left + ((right - left)/(x_ar[it+1]-x_ar[it-1])) * (2*X-x_ar[it-1]-x_ar[it])
    dyx2 = 2*((right-left)/(x_ar[it+1]-x_ar[it-1]))

    return dyx, dyx2
