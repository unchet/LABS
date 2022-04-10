import numpy as np


def swap_rows(A, n, m):
    tmp = np.array(np.zeros(A.shape[0]))

    for i in range(A.shape[1]):
        tmp[i] = A[n, i]
    for i in range(A.shape[1]):
        A[n, i] = A[m, i]
    for i in range(A.shape[1]):
        A[m, i] = tmp[i]


def swap_columns(A, n, m):
    tmp = np.array(np.zeros(A.shape[0]))

    for i in range(A.shape[1]):
        tmp[i] = A[i, n]
    for i in range(A.shape[1]):
        A[i, n] = A[i, m]
    for i in range(A.shape[1]):
        A[i, m] = tmp[i]


def to_LU(A, v):
    n = len(A)
    lu_matrix = np.matrix(np.zeros((n, n)))
    P = np.arange(n)
    P_ = np.arange(n)
    n_P = 0

    for k in range(n):
        max_el = A[k, k]
        idx = k
        idx_ = k
        for i in range(k + 1, n):
            if abs(A[i, k]) > abs(max_el):
                max_el = A[i, k]
                idx = P[i]
                idx_ = i

        if k != idx:
            tmp = P[k]
            P[k] = idx
            P[idx_] = tmp
            swap_rows(A, idx_, k)
            swap_rows(v, idx_, k)
            n_P += 1

    for i in range(0, n-1):
        if A[i, i] == 0:
            return None, None, None, 0, False

    for k in range(n):
        for j in range(k, n):
            lu_matrix[k, j] = A[k, j] - lu_matrix[k, :k] * lu_matrix[:k, j]
        for i in range(k + 1, n):
            lu_matrix[i, k] = (A[i, k] - lu_matrix[i, : k] * lu_matrix[: k, k]) / lu_matrix[k, k]

    return lu_matrix, P, P_, n_P, True


def get_L(LU):
    L = LU.copy()
    for i in range(len(L)):
        L[i, i] = 1
        L[i, i + 1:] = 0
    return L


def get_U(LU):
    U = LU.copy()
    for i in range(1, len(U)):
        U[i, :i] = 0
    return U


def solve_LU(LU, v):
    n = len(LU)
    y = np.matrix(np.zeros([n, 1]))

    for i in range(n):
        y[i, 0] = v[i, 0] - LU[i, :i] * y[:i]

    x = np.matrix(np.zeros([n, 1]))
    for i in range(1, x.shape[0] + 1):
        x[-i, 0] = (y[-i] - LU[-i, -i:] * x[-i:, 0]) / LU[-i, -i]

    return x


def inverse_mat(A):
    n = len(A)
    E = np.eye(n)
    e = np.matrix(np.zeros([n, 1]))

    A_inv = np.matrix(np.zeros([n, n]))

    for i in range(n):
        for j in range(n):
            e[j, 0] = E[j, i]
        lu_matrix = to_LU(A, e)
        A_inv[:, i] = solve_LU(lu_matrix[0], e)

    return A_inv
