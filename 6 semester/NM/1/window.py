import tkinter
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from pandas import DataFrame

from TDMA import *
from Gauss import *
from iter_methods import *
from rotation_method import *
from qr_method import *

small_font = ("Courier New", 9)
font = ("Courier New", 11)
big_font = ("Courier New", 14)
digital = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
n, n_P, it = 0, 0, 0
is_tdma = False
P, P_, L, U, A, A_inv, Q, R = None, None, None, None, None, None, None, None
D = 0.0
a, b, c, v, x, x_swapped, lambdas, vectors = [], [], [], [], [], [], [], []


class Result_qr_method:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('600x200')

        Label(ans, text="Количество итераций: ", font=font).place(x=0, y=20)
        Label(ans, text=it, font=font).place(x=200, y=20)

        Label(ans, text="Собственные значения: ", font=font).place(x=0, y=80)
        Label(ans, text=[round_complex(el, 2) for el in lambdas], font=font).place(x=220, y=80)
        Button(ans, text="Скопировать СЗ", font=small_font,
               command=lambda: copy_to_buffer(ans, lambdas)).place(x=5, y=105)


class Result_rotation_method:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('600x300')

        vectors_ = DataFrame(vectors)
        vectors__ = vectors_.rename(columns=lambda r: '')

        Label(ans, text="Количество итераций: ", font=font).place(x=0, y=20)
        Label(ans, text=it, font=font).place(x=200, y=20)

        Label(ans, text="Собственные значения: ", font=font).place(x=0, y=80)
        Label(ans, text=[round(el, 2) for el in lambdas], font=font).place(x=250, y=80)
        Button(ans, text="Скопировать СЗ", font=small_font,
               command=lambda: copy_to_buffer(ans, lambdas)).place(x=5, y=105)

        Label(ans, text="Собственные векторы: ", font=font).place(x=0, y=150)
        Label(ans, text=vectors_.round(2).to_string(index=False), font=font).place(x=250, y=130)
        Button(ans, text="Скопировать СВ", font=small_font,
               command=lambda: copy_to_buffer(ans, vectors__.to_string(index=False))).place(x=5, y=175)


class Result_iter_methods:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('1000x300')
        x_ = DataFrame(x)
        x_sw = DataFrame(x_swapped)
        A_ = DataFrame(A)
        v_ = DataFrame(v)

        x_ = x_.rename(columns=lambda r: '')
        x_sw = x_sw.rename(columns=lambda r: '')
        A_ = A_.rename(columns=lambda r: '')
        v_ = v_.rename(columns=lambda r: '')

        Label(ans, text="Матрица после перестановок: ", font=font).place(x=0, y=20)
        Label(ans, text=A_.round(2).to_string(index=False), font=font).place(x=250, y=0)
        Label(ans, text=v_.round(2).to_string(index=False), font=font).place(x=300 + n * 40)
        Button(ans, text="Скопировать A", font=small_font,
               command=lambda: copy_to_buffer(ans, A_.to_string(index=False))).place(x=5, y=45)

        Label(ans, text="Вектор перестановок строк P: ", font=font).place(x=380 + n * 40, y=20)
        Label(ans, text=P, font=font).place(x=640 + n * 40, y=20)
        Button(ans, text="Скопировать P", font=small_font,
               command=lambda: copy_to_buffer(ans, P)).place(x=380 + n * 40, y=45)

        Label(ans, text="Вектор перестановок столбцов P_: ", font=font).place(x=380 + n * 40, y=100)
        Label(ans, text=P_, font=font).place(x=670 + n * 40, y=100)
        Button(ans, text="Скопировать P_", font=small_font,
               command=lambda: copy_to_buffer(ans, P_)).place(x=380 + n * 40, y=125)

        Label(ans, text="Вектор X равен: ", font=font).place(x=0, y=50 + n * 15)
        Label(ans, text=x_.to_string(index=False), font=font).place(x=150, y=30 + n * 15)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_.to_string(index=False))).place(x=5, y=80 + n * 15)

        Label(ans, text="X после перестановок: ", font=font).place(x=0, y=150 + n * 15)
        Label(ans, text=x_sw.to_string(index=False), font=font).place(x=200, y=130 + n * 15)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_sw.to_string(index=False))).place(x=5, y=180 + n * 15)

        Label(ans, text="Количество итераций: ", font=font).place(x=250, y=50 + n * 15)
        Label(ans, text=it, font=font).place(x=450, y=50 + n * 15)


class Result_TDMA:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('500x200')
        x_ = DataFrame(x)
        x_ = x_.rename(columns=lambda r: '')
        Label(ans, text="Вектор X равен: ", font=font).place(x=10, y=50)
        Label(ans, text=x_.round(2).to_string(index=False), font=font).place(x=150, y=30)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_.to_string(index=False))).place(x=15, y=80)

        Label(ans, text="Определитель: ", font=font).place(x=250, y=50)
        Label(ans, text=D, font=font).place(x=380, y=50)
        Button(ans, text="Скопировать определитель", font=small_font,
               command=lambda: copy_to_buffer(ans, D)).place(x=250, y=80)


class Result_Gauss:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('1000x350')
        x_ = DataFrame(x)
        L_ = DataFrame(L)
        U_ = DataFrame(U)
        A_ = DataFrame(A)
        A_inv_ = DataFrame(A_inv)
        v_ = DataFrame(v)

        x_ = x_.rename(columns=lambda r: '')
        L_ = L_.rename(columns=lambda r: '')
        U_ = U_.rename(columns=lambda r: '')
        A_ = A_.rename(columns=lambda r: '')
        A_inv_ = A_inv_.rename(columns=lambda r: '')
        v_ = v_.rename(columns=lambda r: '')

        Label(ans, text="Вектор X равен: ", font=font).place(x=0, y=50 + n * 15)
        Label(ans, text=x_.round(2).to_string(index=False), font=font).place(x=150, y=30 + n * 15)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_.to_string(index=False))).place(x=5, y=80 + n * 15)

        Label(ans, text="Определитель: ", font=font).place(x=250, y=50 + n * 15)
        Label(ans, text=D, font=font).place(x=380, y=50 + n * 15)
        Button(ans, text="Скопировать определитель", font=small_font,
               command=lambda: copy_to_buffer(ans, D)).place(x=250, y=80 + n * 15)

        Label(ans, text="Матрица L равна: ", font=font).place(x=0, y=80 + n * 35)
        Label(ans, text=L_.round(2).to_string(index=False), font=font).place(x=160, y=60 + n * 35)
        Button(ans, text="Скопировать L", font=small_font,
               command=lambda: copy_to_buffer(ans, L_.to_string(index=False))).place(x=5, y=105 + n * 35)

        Label(ans, text="Матрица U равна: ", font=font).place(x=340 + n * 35, y=80 + n * 35)
        Label(ans, text=U_.round(2).to_string(index=False), font=font).place(x=500 + n * 35, y=60 + n * 35)
        Button(ans, text="Скопировать U", font=small_font,
               command=lambda: copy_to_buffer(ans, U_.to_string(index=False))).place(x=340 + n * 35, y=105 + n * 35)

        Label(ans, text="Матрица после перестановок: ", font=font).place(x=0, y=20)
        Label(ans, text=A_.round(2).to_string(index=False), font=font).place(x=250, y=0)
        Label(ans, text=v_.round(2).to_string(index=False), font=font).place(x=300 + n * 40)
        Button(ans, text="Скопировать A", font=small_font,
               command=lambda: copy_to_buffer(ans, A_.to_string(index=False))).place(x=5, y=45)

        Label(ans, text="Вектор перестановок строк P: ", font=font).place(x=380 + n * 40, y=50 + n * 15)
        Label(ans, text=P, font=font).place(x=640 + n * 40, y=50 + n * 15)
        Button(ans, text="Скопировать P", font=small_font,
               command=lambda: copy_to_buffer(ans, P)).place(x=380 + n * 40, y=80 + n * 15)

        Label(ans, text="Обратная матрица: ", font=font).place(x=380 + n * 40, y=20)
        Label(ans, text=A_inv_.round(2).to_string(index=False), font=font).place(x=550 + n * 40, y=0)
        Button(ans, text="Скопировать матрицу", font=small_font,
               command=lambda: copy_to_buffer(ans, A_inv_.to_string(index=False))).place(x=380 + n * 40, y=45)


class Window:
    def __init__(self):
        super().__init__()
        self.window = tkinter.Tk()
        self.window.title("Численные методы")
        self.window.geometry('800x450')
        self.window.resizable(0, 0)

        tab_control = ttk.Notebook(self.window)

        self.matrix = []
        self.vector = []

        self.lin_alg = ttk.Frame(tab_control, width=800, height=450)
        self.lin_alg.pack(fill="both", expand=True)
        tab_control.add(self.lin_alg, text='Линейная алгебра')
        tab_control.place(x=0, y=0)
        Label(self.lin_alg, text="Введите порядок матрицы:", font=font).place(x=5, y=10)
        Label(self.lin_alg, text="Погрешность вычислений:", font=font).place(x=5, y=50)
        self.epsilon = StringVar()
        Entry(self.lin_alg, font=font, width=4, textvariable=self.epsilon).place(x=235, y=50)

        self.n_matrix = StringVar()
        Entry(self.lin_alg, font=font, width=3, textvariable=self.n_matrix).place(x=235, y=10)
        Button(self.lin_alg, text="Ввести", font=font, command=self.change_n_matrix).place(x=275, y=7)

        Button(self.lin_alg, text="TDMA", command=self.tdma, font=big_font).place(x=390, y=2)
        Button(self.lin_alg, text="LU-разложение", command=self.gauss, font=big_font).place(x=465, y=2)
        Button(self.lin_alg, text="Метод Якоби", command=self.jacobi, font=big_font).place(x=640, y=2)
        Button(self.lin_alg, text="Метод Зейделя", command=self.seidel, font=big_font).place(x=390, y=50)
        Button(self.lin_alg, text="Метод вращений", command=self.rotation_method_, font=big_font).place(x=565, y=50)
        Button(self.lin_alg, text="QR-разложение", command=self.qr_method_, font=big_font).place(x=390, y=100)

        nonl_eq = ttk.Frame(tab_control)
        tab_control.add(nonl_eq, text='Нелинейные уравнения')
        tab_control.place(x=0, y=0)

        self.window.mainloop()

    def result_TDMA(self):
        Result_TDMA()

    def result_gauss(self):
        Result_Gauss()

    def result_iter_methods(self):
        Result_iter_methods()

    def result_rotation_method(self):
        Result_rotation_method()

    def result_qr_method(self):
        Result_qr_method()

    def get_from_input(self, is_vector_exists=True):
        if not self.n_matrix.get().isdigit():
            show_error("Неверный ввод")
            return
        global A
        A = np.matrix(np.zeros([n, n]))

        for i in range(n):
            for j in range(n):
                el = blank_to_zeros_elem(self.matrix[i][j].get())
                A[i, j] = el

        if not is_vector_exists:
            return True

        global v
        v = np.matrix(np.zeros([n, 1]))
        for i in range(n):
            el = blank_to_zeros_elem(self.vector[i].get())
            v[i, 0] = el
        return True

    def change_n_matrix(self):
        global n
        tmp = self.n_matrix.get()
        if not tmp.isdigit():
            show_error("Неверный ввод")
            return
        n = int(tmp)
        self.delete_matrix()

        for i in range(0, n):
            tmp_matr = []
            for j in range(0, n):
                entr = Entry(self.lin_alg, width=3, font=font)
                entr.place(x=10 + 30 * j, y=100 + 30 * i)
                tmp_matr.append(entr)
            self.matrix.append(tmp_matr)

        for i in range(0, len(self.vector)):
            self.vector[i].destroy()

        self.vector.clear()

        for i in range(0, n):
            vector = Entry(self.lin_alg, width=3, font=font)
            vector.place(x=30 + 30 * n, y=100 + 30 * i)
            self.vector.append(vector)

    def get_abcv(self):
        if not self.n_matrix.get().isdigit():
            show_error("Неверный ввод")
            return False
        global a, b, c, v
        a = np.matrix(np.zeros([n, 1]))
        b = np.matrix(np.zeros([n, 1]))
        c = np.matrix(np.zeros([n, 1]))
        v = np.matrix(np.zeros([n, 1]))

        for i in range(0, n):
            tb = blank_to_zeros_elem(self.matrix[i][i].get())
            tv = blank_to_zeros_elem(self.vector[i].get())

            b[i, 0] = tb
            v[i, 0] = tv
            for j in range(i, i + 1):
                if j + 1 == n:
                    break
                ta = blank_to_zeros_elem(self.matrix[i + 1][j].get())
                tc = blank_to_zeros_elem(self.matrix[i][j + 1].get())
                a[i + 1, 0] = ta
                c[i, 0] = tc
        return True

    def delete_matrix(self):
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix)):
                self.matrix[i][j].destroy()

        self.matrix.clear()

    def tdma(self):
        global x, D
        check = self.get_abcv()
        if not check:
            return

        check = check_tdma_(self.matrix, a, b, c)
        if check == 1:
            show_error("Матрица не трехдиагональная")
            return
        elif check == 2:
            show_error("Матрица неустойчива")
            return
        elif check == 3:
            show_error("Нулевые элементы на главной диагонали")
            return

        x, D = tdma_(a, b, c, v)
        self.result_TDMA()

    def gauss(self):
        global P, P_, n_P, L, U, x, A, v, D, A_inv
        check = self.get_from_input()
        if not check:
            return

        r_A = np.linalg.matrix_rank(A)
        r_Av = np.linalg.matrix_rank(np.concatenate([A, v], axis=1))

        if r_A < r_Av:
            show_error("Система несовместна")
            return
        elif r_A < n:
            show_error("У системы бесконечно много решений")
            return

        lu_matrix, P, P_, n_P, check = to_LU(A, v)
        if not check:
            show_error("Нули на главной диагонали")
            return

        L = get_L(lu_matrix)
        U = get_U(lu_matrix)
        x = solve_LU(lu_matrix, v)
        A_inv = inverse_mat(A)
        D = determinant_gauss(U)
        self.result_gauss()

    def jacobi(self):
        global x, x_swapped, A, v, it, P, P_, n_P
        check = self.get_from_input()
        if not check:
            return
        epsilon = self.epsilon.get()
        if epsilon == '':
            epsilon = 0.01
        x_swapped, it, P, P_, n_P, check = jacobi_(A, v, float(epsilon))
        if check == 1:
            show_error("Нули на главной диагонали")
            return
        elif check == 2:
            show_error("Не выполнено достаточное условие")
            return

        x = swap_x(x_swapped, P_)
        self.result_iter_methods()

    def seidel(self):
        global x, x_swapped, A, v, it, P, P_, n_P
        check = self.get_from_input()
        if not check:
            return
        epsilon = self.epsilon.get()
        if epsilon == '':
            epsilon = 0.01
        x_swapped, it, P, P_, n_P, check = seidel_(A, v, float(epsilon))
        if check == 1:
            show_error("Нули на главной диагонали")
            return
        elif check == 2:
            show_error("Не выполнено достаточное условие")
            return
        x = swap_x(x_swapped, P_)
        self.result_iter_methods()

    def rotation_method_(self):
        global lambdas, vectors, it
        check = self.get_from_input(False)
        if not check:
            return
        epsilon = self.epsilon.get()
        if epsilon == '':
            epsilon = 0.01
        lambdas, vectors, it, check = rotation_method(A, float(epsilon))
        if not check:
            show_error("Матрица несимметрична")
            return
        self.result_rotation_method()

    def qr_method_(self):
        check = self.get_from_input(False)
        if not check:
            return
        if A[0, 0] == 0:
            show_error("Матрица не сходится")
            return
        global Q, R, lambdas, it
        epsilon = self.epsilon.get()
        if epsilon == '':
            epsilon = 0.01
        Q, R = to_QR(A)
        lambdas, it = solver_QR(Q, R, float(epsilon))
        self.result_qr_method()


def show_error(msg):
    mb.showerror("Ошибка", msg)


def blank_to_zeros_elem(el):
    if el == '':
        el = '0'
    return el


def determinant_gauss(M):
    global D
    D = 1
    for i in range(0, n):
        D *= M[i, i]
    if n_P % 2 != 0:
        D *= -1
    return round(D, 2)


def blank_to_zeros(m):
    for i in range(0, len(m)):
        if m[i] == '':
            m[i] = '0'


def copy_to_buffer(wind, x_):
    wind.clipboard_clear()
    wind.clipboard_append(x_)


def swap_x(x_sw, P_col):
    x_ = np.matrix(np.zeros([n, 1]))
    for i in range(n):
        k = P_col[i]
        x_[i, 0] = x_sw[k, 0]
    return x_


def round_complex(C, num):
    if not isinstance(C, complex):
        return round(C, num)
    return complex(round(C.real, num), round(C.imag, num))
