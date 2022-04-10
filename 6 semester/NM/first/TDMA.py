import numpy as np


def check_tdma_(A, a, b, c):
    n = len(A)
    for i in range(2, n):
        tmp = A[0][i].get()
        if tmp != 0 and tmp != '':
            return 1
    for i in range(0, n-2):
        tmp = A[n-1][i].get()
        if tmp != 0 and tmp != '':
            return 1
    for i in range(1, n-1):
        for j in range(i+2, n):
            tmp = A[i][j].get()
            if tmp != 0 and tmp != '':
                return 1

    for i in range(0, n):
        if b[i] == 0:
            return 3
        if abs(b[i]) < abs(a[i]) + abs(c[i]):
            return 2

    return 0


def tdma_(a, b, c, v):
    n = len(v)

    x = np.matrix(np.zeros([n, 1]))
    p = np.matrix(np.zeros([n, 1]))
    q = np.matrix(np.zeros([n, 1]))

    p[0] = c[0] / (-b[0])
    q[0] = v[0] / b[0]

    for i in range(1, n-1):
        p[i] = -c[i] / (b[i] + a[i]*p[i-1])
        q[i] = (v[i] - a[i]*q[i-1])/(b[i] + a[i]*p[i-1])

    p[-1] = 0
    q[-1] = (v[-1] - a[-1]*q[-2])/(b[-1] + a[-1]*p[-2])

    x[-1] = q[-1]
    for i in range(n-1, 0, -1):
        x[i-1] = p[i-1] * x[i] + q[i-1]

    D = b[0]
    for i in range(1, n):
        D *= b[i] + a[i]*p[i-1]

    return x, D
