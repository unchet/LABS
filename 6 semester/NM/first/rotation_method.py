import numpy as np


def check_symmetrical(A):
    n = len(A)
    for i in range(n):
        for j in range(i, n):
            if i != j:
                if A[i, j] != A[j, i]:
                    return False
    return True


def get_lambdas(A):
    n = len(A)
    lambdas = [0]*n
    for i in range(n):
        lambdas[i] = A[i, i]
    return lambdas


def get_vectors(M_list):
    n = len(M_list)
    result_M = M_list[0]
    for i in range(1, n):
        result_M *= M_list[i]
    return result_M


def get_max_elem(A):
    n = len(A)
    max_elem = 0
    i_, j_ = 0, 0
    for i in range(n-1):
        for j in range(i+1, n):
            if abs(A[i, j]) > abs(max_elem):
                max_elem = A[i, j]
                i_, j_ = i, j
    return max_elem, i_, j_


def rotation_method(A, epsilon):
    if not check_symmetrical(A):
        return None, None, 0, False
    n = len(A)
    rotation_matrix_list = []
    it = 0
    while True:
        rotation_matrix = np.matrix(np.zeros([n, n]))
        max_elem, i_, j_ = get_max_elem(A)
        if A[i_, i_] == A[j_, j_]:
            phi = np.arctan(1)
        else:
            phi = 0.5 * np.arctan((2 * A[i_, j_]) / (A[i_, i_] - A[j_, j_]))

        rotation_matrix[i_, j_] = -np.sin(phi)
        rotation_matrix[j_, i_] = np.sin(phi)
        rotation_matrix[i_, i_] = np.cos(phi)
        rotation_matrix[j_, j_] = np.cos(phi)

        for i in range(n):
            if i != i_ and i != j_:
                rotation_matrix[i, i] = 1

        rotation_matrix_list.append(rotation_matrix)
        A = np.transpose(rotation_matrix) * A * rotation_matrix

        sum_ = 0
        for i in range(0, n-1):
            for j in range(i+1, n):
                sum_ += A[i, j] * A[i, j]

        it += 1
        if np.sqrt(sum_) <= epsilon:
            lambdas = get_lambdas(A)
            vectors = get_vectors(rotation_matrix_list)
            return lambdas, vectors, it, True
