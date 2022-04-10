import numpy as np


def solver(A, number):
    a = A[number, number]
    b = A[number + 1, number + 1]
    c = A[number + 1, number]
    d = A[number, number + 1]
    D = (a - b) ** 2 + 4 * c * d

    if D < 0:
        sqrt_D = np.sqrt(-D)
        real_ = 0.5 * (a + b)
        imag_ = 0.5 * sqrt_D
        x1 = complex(real_, imag_)
        x2 = complex(real_, -imag_)
    else:
        sqrt_D = np.sqrt(D)
        x1 = 0.5 * (a + b + sqrt_D)
        x2 = 0.5 * (a + b - sqrt_D)

    return x1, x2


def norm(v):
    sum_ = 0
    for i in range(len(v)):
        sum_ += v[i, 0] * v[i, 0]
    return np.sqrt(sum_)


def norm_complex(c):
    sum_ = c.real * c.real + c.imag * c.imag
    return np.sqrt(sum_)


def get_lambdas(A):
    L = []
    for i in range(len(A)):
        L.append(A[i, i])
    return L


def check_matrix(A):
    sum_ = 0
    n = 0
    for i in range(1, len(A)):
        n += i
    for j in range(len(A)):
        for i in range(j + 1, len(A)):
            sum_ += abs(A[i, j])

    sum_ /= n
    if sum_ == 0:
        sum_ = 1
    return sum_


def check_elem(A, number):
    sum_ = 0
    n = 1
    for i in range(2, len(A) - number):
        n += 1

    for i in range(number + 1, len(A)):
        sum_ += abs(A[i, number])

    sum_ /= n
    return sum_


def get_Q(H):
    Q = H[0]
    for i in range(1, len(H)):
        Q *= H[i]
    return Q


def to_QR(A):
    n = len(A)
    H = []
    for i in range(n - 1):
        b = np.matrix(np.zeros([n - i, 1]))
        for k in range(i, n):
            b[k - i, 0] = A[k, i]

        v = np.matrix(np.zeros([n, 1]))

        v[i, 0] = b[0, 0] + np.sign(b[0, 0]) * norm(b)

        for k in range(i + 1, n):
            v[k, 0] = b[k - i, 0]
        H_i = np.eye(n) - 2 * (v * np.transpose(v) / (np.transpose(v) * v))
        H.append(H_i)
        A = H_i * A
    Q = get_Q(H)
    return Q, A


def check_for_complex(A, num):
    x1, x2 = solver(A, num)
    if isinstance(x1, complex):
        return True, x1, x2
    return False, None, None


def find_real_eigenvalues(Q, R, epsilon):
    num = 0
    i = 0
    indexes = []
    norma_ = None
    while True:
        A = R * Q
        if check_elem(A, num) <= epsilon:
            indexes.append(num)
            num += 1

        else:
            check, x1, x2 = check_for_complex(A, num)
            if check:
                if norma_ is not None:
                    norma_new = norm_complex(x1)
                    if abs(norma_ - norma_new) <= epsilon:
                        num += 2
                norma_ = norm_complex(x1)

        if num == len(A):
            return indexes, A, i

        i += 1
        Q, R = to_QR(A)


def find_complex_eigenvalues(A, indexes):
    x = []
    i = 0
    while i < len(A):
        if i not in indexes:
            x1, x2 = solver(A, i)
            x.append(x1)
            x.append(x2)
            i += 1
        i += 1

    return x


def solver_QR(Q, R, epsilon):
    lambdas = [0] * len(Q)
    indexes, A, it = find_real_eigenvalues(Q, R, epsilon)

    for i in indexes:
        lambdas[i] = (A[i, i])

    x = find_complex_eigenvalues(A, indexes)

    k = 0
    while k < len(x):
        for i in range(len(lambdas)):
            if i not in indexes:
                lambdas[i] = x[k]
                k += 1

    return lambdas, it

# x^2 -(a+b)x + ab - cd = 0
# D = (a+b)^2 - 4(ab - cd) = (a-b)^2 +4cd
# x = 0.5(a+b +- sqrt(D))
