from first.Gauss import swap_rows, swap_columns
import numpy as np


def norm_matrix(A):
    n = len(A)
    sum_ = 0
    for i in range(n):
        for j in range(n):
            sum_ += A[i, j] * A[i, j]
    return np.sqrt(sum_)


def check_diagonal(A):
    n = len(A)
    for i in range(0, n):
        sum_ = 0
        for j in range(0, n):
            if i != j:
                sum_ += abs(A[i, j])
        if abs(A[i, i]) <= sum_:
            return False
    return True


def norma(a, b):
    n = len(a)
    a_ = np.array(np.zeros(n))
    b_ = np.array(np.zeros(n))
    for i in range(0, n):
        a_[i] = a[i][0]
        b_[i] = b[i][0]
    return np.sqrt(np.dot(b_-a_, b_-a_))


def iter_methods(A, v):
    n = len(v)
    b = np.matrix(np.zeros([n, 1]))
    a = np.matrix(np.zeros([n, n]))

    P = np.arange(n)
    P_ = np.arange(n)
    n_P = 0

    for k in range(n):
        idx = k
        idx_ = k
        if A[k, k] == 0:
            for i in range(0, n):
                if A[i, k] != 0 and A[k, i] != 0:
                    idx = P[i]
                    idx_ = i
                    break

        if k != idx:
            tmp = P[k]
            P[k] = idx
            P[idx_] = tmp
            swap_rows(A, idx_, k)
            swap_rows(v, idx_, k)
            n_P += 1

    for k in range(0, n):
        max_el = A[k, k]
        idx = k
        idx_ = k
        for i in range(0, n):
            if abs(A[k, i]) > abs(max_el) and A[i, k] != 0:
                if A[k, i] - max_el > A[i, i] - A[i, k]:
                    max_el = A[k, i]
                    idx = P_[i]
                    idx_ = i

        if k != idx:
            tmp = P_[k]
            P_[k] = idx
            P_[idx_] = tmp
            swap_columns(A, idx_, k)
            n_P += 1

    for i in range(0, n):
        if A[i, i] == 0:
            return None, 0, None, None, 0, 1

    # if not check_diagonal(A):
    #     return None, None, None, None, 0, 2

    for i in range(0, n):
        for j in range(0, n):
            b[i] = v[i] / A[i, i]
            if i != j:
                a[i, j] = -A[i, j] / A[i, i]
            else:
                a[i, j] = 0

    if norm_matrix(a) > 1:
        return None, None, None, None, 0, 2

    return a, b, P, P_, n_P, 0


def jacobi_(A, v, epsilon):
    a, b, P, P_, n_P, check = iter_methods(A, v)
    if check == 1:
        return None, 0, None, None, 0, 1
    elif check == 2:
        return None, 0, None, None, 0, 2

    x = np.copy(b)
    print("X0", x)
    i = 1
    while True:
        x1 = b + a * x
        print("X", i, x1)
        norm = norma(x, x1)
        n_a = norm_matrix(a)
        if n_a == 1:
            coef = 1
        else:
            coef = n_a / (1.0 - n_a)
        if coef * abs(norm) <= epsilon:
            return x1, i, P, P_, n_P, 0
        i += 1
        x = x1


def seidel_(A, v, epsilon=0.01):
    a, b, P, P_, n_P, check = iter_methods(A, v)
    if check == 1:
        return None, 0, None, None, 0, 1
    elif check == 2:
        return None, 0, None, None, 0, 2

    B = a.copy()
    n = len(a)
    for i in range(n):
        B[i, i] = 0
        B[i, i + 1:] = 0

    B_1 = np.linalg.inv(np.eye(n) - B)
    C = a.copy()
    for i in range(1, n):
        C[i, :i] = 0

    x = np.copy(b)
    print("X0", x)
    i = 1

    while True:
        x1 = B_1 * C * x + B_1 * b
        print("X", i, x1)
        norm = norma(x, x1)
        n_a = norm_matrix(a)
        if n_a == 1:
            coef = 1
        else:
            coef = n_a / (1.0 - n_a)
        if coef * abs(norm) <= epsilon:
            return x1, i, P, P_, n_P, 0
        i += 1
        x = x1
