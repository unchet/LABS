import tkinter
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb

from pandas import DataFrame
import numexpr as ne
import matplotlib.pyplot as plt
from franges import frange
from sympy import *

from first.TDMA import *
from first.Gauss import *
from first.iter_methods import *
from first.rotation_method import *
from first.qr_method import *

from second.nonlinear_equations import *
from second.nonlinear_systems import *

from third.interpolation import *
from third.spline import *
from third.mnk import *
from third.derivative import *
from third.integrate import *

from fourth.cauchy import *

plt.style.use('ggplot')
small_font = ("Courier New", 12)
font = ("Courier New", 14)
big_font = ("Courier New", 18)
n, n_P, it, D = 0, 0, 0, 0.0
P, P_, L, U, A, A_inv, Q, R = None, None, None, None, None, None, None, None
a, b, c, v, x, y, x_swapped, lambdas, vectors = [], [], [], [], [], [], [], [], []


class Result_cauchy:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('800x500')

        Label(ans, text="x", font=font).place(x=20, y=50)
        Label(ans, text="y", font=font).place(x=220, y=50)
        Label(ans, text="z", font=font).place(x=420, y=50)

        for i in range(len(L)):
            Label(ans, text=round(L[i], 5), font=font).place(x=20, y=90+20*i)
            Label(ans, text=round(A[i], 5), font=font).place(x=220, y=90+20*i)
            Label(ans, text=round(R[i], 5), font=font).place(x=420, y=90+20*i)


class Result_integral:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('800x500')
        Label(ans, text="Шаг = h1 ", font=font).place(x=20, y=60)
        Label(ans, text="Шаг = h2 ", font=font).place(x=20, y=120)
        Label(ans, text="Улучшение ", font=font).place(x=20, y=180)
        Label(ans, text="Точное значение:", font=font).place(x=20, y=240)
        Label(ans, text="Абсолютная\nразность", font=font).place(x=20, y=320)
        Label(ans, text="Метод прямоугольников", font=font).place(x=150, y=20)
        Label(ans, text="Метод трапеций", font=font).place(x=410, y=20)
        Label(ans, text="Метод Симпсона", font=font).place(x=600, y=20)

        Label(ans, text=round(L[0], 8), font=font).place(x=220, y=60)
        Label(ans, text=round(U[0], 8), font=font).place(x=440, y=60)
        Label(ans, text=round(A[0], 8), font=font).place(x=630, y=60)

        Label(ans, text=round(L[1], 8), font=font).place(x=220, y=120)
        Label(ans, text=round(U[1], 8), font=font).place(x=440, y=120)
        Label(ans, text=round(A[1], 8), font=font).place(x=630, y=120)

        Label(ans, text=round(L[2], 8), font=font).place(x=220, y=180)
        Label(ans, text=round(U[2], 8), font=font).place(x=440, y=180)
        Label(ans, text=round(A[2], 8), font=font).place(x=630, y=180)

        Label(ans, text=round(R, 8), font=font).place(x=50, y=270)
        Label(ans, text=round(L[3], 8), font=font).place(x=220, y=330)
        Label(ans, text=round(U[3], 8), font=font).place(x=440, y=330)
        Label(ans, text=round(A[3], 8), font=font).place(x=630, y=330)


class Result_derivative:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('800x300')
        Label(ans, text="Первая производная:", font=font).place(x=20, y=20)
        Label(ans, text=A, font=font).place(x=250, y=20)

        Label(ans, text="Вторая производная:", font=font).place(x=20, y=80)
        Label(ans, text=R, font=font).place(x=250, y=80)


class Result_mnk:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('800x300')
        Label(ans, text="F1 =", font=font).place(x=20, y=20)
        Label(ans, text=L, font=font).place(x=70, y=20)
        Label(ans, text="Ошибка:", font=font).place(x=20, y=60)
        Label(ans, text=A, font=font).place(x=110, y=60)

        Label(ans, text="F2 =", font=font).place(x=20, y=140)
        Label(ans, text=U, font=font).place(x=70, y=140)
        Label(ans, text="Ошибка:", font=font).place(x=20, y=180)
        Label(ans, text=R, font=font).place(x=110, y=180)

        Button(ans, text='График', font=big_font, command=self.show_graphs).place(x=500, y=20)

    def show_graphs(self):
        x = sym.Symbol('x')

        f1 = sym.S(L)
        f2 = sym.S(U)

        plot1, plot2 = sym.plot(f1, f2, show=False)
        x1, y1 = plot1.get_points()
        x2, y2 = plot2.get_points()

        plt.plot(x1, y1, label=str(f1))
        plt.plot(x2, y2, label=str(f2))
        plt.plot(x_swapped, y, 'go', label='Заданные точки из таблицы')
        plt.legend(loc="upper left")
        plt.show()


class Result_spline:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('800x300')
        Label(ans, text="Многочлен:", font=font).place(x=20, y=80)
        Label(ans, text=L, font=small_font).place(x=150, y=80)

        Label(ans, text="Значение =", font=font).place(x=20, y=20)
        Label(ans, text=R, font=font).place(x=170, y=20)


class Result_interpolate_methods:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('800x300')
        Label(ans, text="Многочлен:", font=font).place(x=20, y=80)
        Label(ans, text=L, font=small_font).place(x=150, y=80)

        Label(ans, text="Погрешность =", font=font).place(x=20, y=20)
        Label(ans, text=R, font=font).place(x=170, y=20)


class Result_nonlinear_system:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('400x200')

        Label(ans, text="(x1, x2):", font=font).place(x=20, y=20)
        Label(ans, text=round(x, 8), font=font).place(x=140, y=20)
        Label(ans, text=round(y, 8), font=font).place(x=260, y=20)

        Label(ans, text="Количество итераций: ", font=font).place(x=20, y=80)
        Label(ans, text=it, font=font).place(x=260, y=80)


class Result_nonlinear:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('400x200')

        Label(ans, text="X:", font=font).place(x=20, y=20)
        Label(ans, text=round(x, 8), font=font).place(x=70, y=20)

        Label(ans, text="Количество итераций: ", font=font).place(x=20, y=80)
        Label(ans, text=it, font=font).place(x=260, y=80)


class Result_qr_method:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('600x200')

        Label(ans, text="Количество итераций: ", font=font).place(x=0, y=20)
        Label(ans, text=it, font=font).place(x=240, y=20)

        Label(ans, text="Собственные значения: ", font=font).place(x=0, y=80)
        Label(ans, text=[round_complex(el, 2) for el in lambdas], font=font).place(x=250, y=80)
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
        Label(ans, text=it, font=font).place(x=240, y=20)

        Label(ans, text="Собственные значения: ", font=font).place(x=0, y=80)
        Label(ans, text=[round(el, 2) for el in lambdas], font=font).place(x=250, y=80)
        Button(ans, text="Скопировать СЗ", font=small_font,
               command=lambda: copy_to_buffer(ans, lambdas)).place(x=5, y=105)

        Label(ans, text="Собственные векторы: ", font=font).place(x=0, y=180)
        Label(ans, text=vectors_.round(2).to_string(index=False), font=font).place(x=250, y=160)
        Button(ans, text="Скопировать СВ", font=small_font,
               command=lambda: copy_to_buffer(ans, vectors__.to_string(index=False))).place(x=5, y=205)


class Result_iter_methods:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('1000x350')
        x_ = DataFrame(x)
        x_sw = DataFrame(x_swapped)
        A_ = DataFrame(A)
        v_ = DataFrame(v)

        x_ = x_.rename(columns=lambda r: '')
        x_sw = x_sw.rename(columns=lambda r: '')
        A_ = A_.rename(columns=lambda r: '')
        v_ = v_.rename(columns=lambda r: '')

        Label(ans, text="Матрица после перестановок: ", font=font).place(x=0, y=20)
        Label(ans, text=A_.round(2).to_string(index=False), font=font).place(x=310, y=0)
        Label(ans, text=v_.round(2).to_string(index=False), font=font).place(x=330 + n * 40)
        Button(ans, text="Скопировать A", font=small_font,
               command=lambda: copy_to_buffer(ans, A_.to_string(index=False))).place(x=5, y=45)

        Label(ans, text="Вектор перестановок строк P: ", font=font).place(x=450 + n * 40, y=20)
        Label(ans, text=P, font=font).place(x=760 + n * 40, y=20)
        Button(ans, text="Скопировать P", font=small_font,
               command=lambda: copy_to_buffer(ans, P)).place(x=450 + n * 40, y=45)

        Label(ans, text="Вектор перестановок столбцов P_: ", font=font).place(x=450 + n * 40, y=100)
        Label(ans, text=P_, font=font).place(x=810 + n * 40, y=100)
        Button(ans, text="Скопировать P_", font=small_font,
               command=lambda: copy_to_buffer(ans, P_)).place(x=450 + n * 40, y=125)

        Label(ans, text="Вектор X равен: ", font=font).place(x=0, y=50 + n * 25)
        Label(ans, text=x_.to_string(index=False), font=font).place(x=200, y=30 + n * 25)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_.to_string(index=False))).place(x=5, y=80 + n * 25)

        Label(ans, text="X после перестановок: ", font=font).place(x=0, y=180 + n * 35)
        Label(ans, text=x_sw.to_string(index=False), font=font).place(x=250, y=160 + n * 35)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_sw.to_string(index=False))).place(x=5, y=210 + n * 35)

        Label(ans, text="Количество итераций: ", font=font).place(x=270, y=50 + n * 25)
        Label(ans, text=it, font=font).place(x=500, y=50 + n * 25)


class Result_TDMA:
    def __init__(self):
        super().__init__()
        ans = tkinter.Toplevel()
        ans.wm_title("Результат")
        ans.wm_geometry('600x200')
        x_ = DataFrame(x)
        x_ = x_.rename(columns=lambda r: '')
        Label(ans, text="Вектор X равен: ", font=font).place(x=10, y=50)
        Label(ans, text=x_.round(2).to_string(index=False), font=font).place(x=200, y=30)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_.to_string(index=False))).place(x=15, y=90)

        Label(ans, text="Определитель: ", font=font).place(x=300, y=50)
        Label(ans, text=D, font=font).place(x=480, y=50)
        Button(ans, text="Скопировать определитель", font=small_font,
               command=lambda: copy_to_buffer(ans, D)).place(x=300, y=90)


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

        Label(ans, text="Вектор X равен: ", font=font).place(x=0, y=50 + n * 20)
        Label(ans, text=x_.round(2).to_string(index=False), font=font).place(x=180, y=30 + n * 20)
        Button(ans, text="Скопировать X", font=small_font,
               command=lambda: copy_to_buffer(ans, x_.to_string(index=False))).place(x=5, y=80 + n * 20)

        Label(ans, text="Определитель: ", font=font).place(x=280, y=50 + n * 20)
        Label(ans, text=D, font=font).place(x=430, y=50 + n * 20)
        Button(ans, text="Скопировать определитель", font=small_font,
               command=lambda: copy_to_buffer(ans, D)).place(x=280, y=80 + n * 20)

        Label(ans, text="Матрица L равна: ", font=font).place(x=0, y=80 + n * 40)
        Label(ans, text=L_.round(2).to_string(index=False), font=font).place(x=190, y=60 + n * 40)
        Button(ans, text="Скопировать L", font=small_font,
               command=lambda: copy_to_buffer(ans, L_.to_string(index=False))).place(x=5, y=105 + n * 40)

        Label(ans, text="Матрица U равна: ", font=font).place(x=340 + n * 40, y=80 + n * 40)
        Label(ans, text=U_.round(2).to_string(index=False), font=font).place(x=530 + n * 40, y=60 + n * 40)
        Button(ans, text="Скопировать U", font=small_font,
               command=lambda: copy_to_buffer(ans, U_.to_string(index=False))).place(x=340 + n * 40, y=105 + n * 40)

        Label(ans, text="Матрица после перестановок: ", font=font).place(x=0, y=20)
        Label(ans, text=A_.round(2).to_string(index=False), font=font).place(x=320, y=0)
        Label(ans, text=v_.round(2).to_string(index=False), font=font).place(x=350 + n * 40)
        Button(ans, text="Скопировать A", font=small_font,
               command=lambda: copy_to_buffer(ans, A_.to_string(index=False))).place(x=5, y=45)

        Label(ans, text="Вектор перестановок строк P: ", font=font).place(x=450 + n * 40, y=50 + n * 20)
        Label(ans, text=P, font=font).place(x=760 + n * 40, y=50 + n * 20)
        Button(ans, text="Скопировать P", font=small_font,
               command=lambda: copy_to_buffer(ans, P)).place(x=450 + n * 40, y=80 + n * 20)

        Label(ans, text="Обратная матрица: ", font=font).place(x=450 + n * 40, y=20)
        Label(ans, text=A_inv_.round(2).to_string(index=False), font=font).place(x=670 + n * 40, y=0)
        Button(ans, text="Скопировать матрицу", font=small_font,
               command=lambda: copy_to_buffer(ans, A_inv_.to_string(index=False))).place(x=450 + n * 40, y=45)


class Window:
    def __init__(self):
        super().__init__()
        self.window = tkinter.Tk()
        self.window.title("Численные методы")
        self.window.geometry('1000x450')
        self.window.resizable(0, 0)

        tab_control = ttk.Notebook(self.window)

        self.matrix = []
        self.vector = []

        self.lin_alg = ttk.Frame(tab_control, width=1000, height=650)
        self.lin_alg.pack(fill="both", expand=True)
        tab_control.add(self.lin_alg, text='Линейная алгебра')
        tab_control.place(x=0, y=0)
        Label(self.lin_alg, text="Введите порядок матрицы:", font=font).place(x=5, y=10)
        Label(self.lin_alg, text="Погрешность вычислений:", font=font).place(x=5, y=50)
        self.epsilon = StringVar()
        Entry(self.lin_alg, font=font, width=4, textvariable=self.epsilon).place(x=275, y=50)

        self.n_matrix = StringVar()
        Entry(self.lin_alg, font=font, width=3, textvariable=self.n_matrix).place(x=275, y=10)
        Button(self.lin_alg, text="Ввести", font=font, command=self.change_n_matrix).place(x=320, y=5)

        Button(self.lin_alg, text="Метод прогонки", command=self.tdma, font=big_font).place(x=745, y=2)
        Button(self.lin_alg, text="LU-разложение", command=self.gauss, font=big_font).place(x=530, y=2)
        Button(self.lin_alg, text="Метод Якоби", command=self.jacobi, font=big_font).place(x=745, y=50)
        Button(self.lin_alg, text="Метод Зейделя", command=self.seidel, font=big_font).place(x=530, y=50)
        Button(self.lin_alg, text="Метод вращений", command=self.rotation_method_, font=big_font).place(x=745, y=100)
        Button(self.lin_alg, text="QR-разложение", command=self.qr_method_, font=big_font).place(x=530, y=100)

        self.nonl_eq = ttk.Frame(tab_control, width=800, height=450)
        tab_control.add(self.nonl_eq, text='Нелинейные уравнения')
        self.expression, self.second_expression = StringVar(), StringVar()
        self.iter = StringVar()
        self.a, self.a2 = StringVar(), StringVar()
        self.b, self.b2 = StringVar(), StringVar()
        one_or_system = IntVar()

        Radiobutton(self.nonl_eq, text="Одно уравнение",
                    font=font, value=1, variable=one_or_system, command=self.from_system_to_one).place(x=5, y=20)
        Radiobutton(self.nonl_eq, text="Система уравнений",
                    font=font, value=2, variable=one_or_system, command=self.from_one_to_system).place(x=250, y=20)
        self.label_f, self.label_g = Label(), Label()
        self.entry_f, self.entry_g = Entry(), Entry()
        self.button = Button()

        self.label_ab, self.label_a1, self.label_b1, self.label_a2, self.label_b2 = Label(), Label(), Label(), Label(), Label()
        self.entry_a1, self.entry_b1, self.entry_a2, self.entry_b2 = Entry(), Entry(), Entry(), Entry()

        self.eps = Label()
        self.eps_entry = Entry()

        self.iter_meth, self.newton_meth = Button(), Button()

        self.interpol = ttk.Frame(tab_control, width=1000, height=650)
        self.interpol.pack(fill="both", expand=True)
        tab_control.add(self.interpol, text='Методы приближения')

        Radiobutton(self.interpol, text="Полиномиальная",
                    font=font, value=1, variable=one_or_system, command=self.to_polynomial).place(x=5, y=20)
        Radiobutton(self.interpol, text="Сплайн",
                    font=font, value=2, variable=one_or_system, command=self.to_spline).place(x=250, y=20)
        Radiobutton(self.interpol, text="МНК",
                    font=font, value=3, variable=one_or_system, command=self.to_mnk).place(x=450, y=20)
        Radiobutton(self.interpol, text="Дифференцирование",
                    font=font, value=4, variable=one_or_system, command=self.to_diff).place(x=5, y=60)
        Radiobutton(self.interpol, text="Интегрирование",
                    font=font, value=5, variable=one_or_system, command=self.to_integral).place(x=250, y=60)

        self.ode = ttk.Frame(tab_control, width=1000, height=650)
        self.ode.pack(fill="both", expand=True)
        tab_control.add(self.ode, text='Численные решения ОДУ')

        Label(self.ode, text="Функция:", font=font).place(x=20, y=20)
        Entry(self.ode, font=big_font, width=40, textvariable=self.expression).place(x=150, y=17)
        Label(self.ode, text="y(0)  =", font=font).place(x=20, y=80)
        Entry(self.ode, font=big_font, width=7, textvariable=self.a).place(x=150, y=77)
        Label(self.ode, text="y'(0) =", font=font).place(x=20, y=140)
        Entry(self.ode, font=big_font, width=7, textvariable=self.a2).place(x=150, y=137)
        Label(self.ode, text="x     =", font=font).place(x=20, y=200)
        Entry(self.ode, font=big_font, width=15, textvariable=self.b).place(x=150, y=197)
        Label(self.ode, text="h     =", font=font).place(x=20, y=260)
        Entry(self.ode, font=big_font, width=7, textvariable=self.b2).place(x=150, y=257)

        Button(self.ode, text="Метод Эйлера", font=big_font, command=self.euler_cauchy).place(x=800, y=5)
        Button(self.ode, text="Метод\nРунге-Котта", font=big_font, command=self.runge_kutta_).place(x=800, y=65)
        Button(self.ode, text="Метод\nАдамса", font=big_font, command=self.adams_).place(x=800, y=125)

        self.window.mainloop()

    @staticmethod
    def delete_widgets(*args):
        for i in args:
            i.destroy()

    @staticmethod
    def result_TDMA():
        Result_TDMA()

    @staticmethod
    def result_gauss():
        Result_Gauss()

    @staticmethod
    def result_iter_methods():
        Result_iter_methods()

    @staticmethod
    def result_rotation_method():
        Result_rotation_method()

    @staticmethod
    def result_qr_method():
        Result_qr_method()

    @staticmethod
    def result_nonlinear():
        Result_nonlinear()

    @staticmethod
    def result_nonlinear_system():
        Result_nonlinear_system()

    @staticmethod
    def result_interpolation_methods():
        Result_interpolate_methods()

    @staticmethod
    def result_spline():
        Result_spline()

    @staticmethod
    def result_mnk():
        Result_mnk()

    @staticmethod
    def result_derivative():
        Result_derivative()

    @staticmethod
    def result_integral():
        Result_integral()

    @staticmethod
    def result_cauchy():
        Result_cauchy()

    def to_polynomial(self):
        self.delete_widgets(self.label_f, self.entry_f, self.label_a2, self.entry_a2, self.label_a1, self.entry_a1,
                            self.iter_meth, self.newton_meth, self.label_b1, self.label_b2, self.entry_b1,
                            self.entry_b2)

        self.label_f = Label(self.interpol, text="f(x)=", font=big_font)
        self.label_f.place(x=0, y=110)
        self.entry_f = Entry(self.interpol, font=big_font, width=30, textvariable=self.expression)
        self.entry_f.place(x=80, y=110)

        self.label_a2 = Label(self.interpol, text="X =", font=big_font)
        self.label_a2.place(x=25, y=160)
        self.entry_a2 = Entry(self.interpol, font=big_font, width=5, textvariable=self.a)
        self.entry_a2.place(x=80, y=160)

        self.label_a1 = Label(self.interpol, text="xi =", font=big_font)
        self.label_a1.place(x=0, y=210)
        self.entry_a1 = Entry(self.interpol, font=font, width=35, textvariable=self.second_expression)
        self.entry_a1.place(x=80, y=210)

        self.iter_meth = Button(self.interpol, text="Метод Лагранжа", font=big_font,
                                command=self.interpolation_method_lagrange)
        self.iter_meth.place(x=750, y=5)
        self.newton_meth = Button(self.interpol, text="Метод Ньютона", font=big_font,
                                  command=self.interpolation_method_newton)
        self.newton_meth.place(x=750, y=55)

    def to_spline(self):
        self.delete_widgets(self.label_f, self.entry_f, self.label_a2, self.entry_a2, self.label_a1, self.entry_a1,
                            self.iter_meth, self.newton_meth, self.label_b1, self.label_b2, self.entry_b1,
                            self.entry_b2)
        self.label_a1 = Label(self.interpol, text="xi =", font=big_font)
        self.label_a1.place(x=0, y=110)
        self.entry_a1 = Entry(self.interpol, font=font, width=35, textvariable=self.expression)
        self.entry_a1.place(x=80, y=110)

        self.label_a2 = Label(self.interpol, text="fi =", font=big_font)
        self.label_a2.place(x=0, y=160)
        self.entry_a2 = Entry(self.interpol, font=font, width=35, textvariable=self.second_expression)
        self.entry_a2.place(x=80, y=160)

        self.label_f = Label(self.interpol, text="X =", font=big_font)
        self.label_f.place(x=0, y=210)
        self.entry_f = Entry(self.interpol, font=font, width=5, textvariable=self.a)
        self.entry_f.place(x=80, y=210)

        self.iter_meth = Button(self.interpol, text="Кубический сплайн", font=big_font,
                                command=self.spline)
        self.iter_meth.place(x=730, y=5)

    def to_mnk(self):
        self.delete_widgets(self.label_f, self.entry_f, self.label_a2, self.entry_a2, self.label_a1, self.entry_a1,
                            self.iter_meth, self.newton_meth, self.label_b1, self.label_b2, self.entry_b1,
                            self.entry_b2)
        self.label_a1 = Label(self.interpol, text="xi =", font=big_font)
        self.label_a1.place(x=0, y=110)
        self.entry_a1 = Entry(self.interpol, font=font, width=35, textvariable=self.expression)
        self.entry_a1.place(x=80, y=110)

        self.label_a2 = Label(self.interpol, text="yi =", font=big_font)
        self.label_a2.place(x=0, y=160)
        self.entry_a2 = Entry(self.interpol, font=font, width=35, textvariable=self.second_expression)
        self.entry_a2.place(x=80, y=160)

        self.iter_meth = Button(self.interpol, text="Метод наименьших\nквадратов", font=big_font,
                                command=self.mnk)
        self.iter_meth.place(x=730, y=5)

    def to_diff(self):
        self.delete_widgets(self.label_f, self.entry_f, self.label_a2, self.entry_a2, self.label_a1, self.entry_a1,
                            self.iter_meth, self.newton_meth, self.label_b1, self.label_b2, self.entry_b1, self.entry_b2)
        self.label_a1 = Label(self.interpol, text="xi =", font=big_font)
        self.label_a1.place(x=0, y=110)
        self.entry_a1 = Entry(self.interpol, font=font, width=35, textvariable=self.expression)
        self.entry_a1.place(x=80, y=110)

        self.label_a2 = Label(self.interpol, text="fi =", font=big_font)
        self.label_a2.place(x=0, y=160)
        self.entry_a2 = Entry(self.interpol, font=font, width=35, textvariable=self.second_expression)
        self.entry_a2.place(x=80, y=160)

        self.label_f = Label(self.interpol, text="X =", font=big_font)
        self.label_f.place(x=0, y=210)
        self.entry_f = Entry(self.interpol, font=font, width=5, textvariable=self.a)
        self.entry_f.place(x=80, y=210)

        self.iter_meth = Button(self.interpol, text="Численное\nдифференцирование", font=big_font,
                                command=self.derivative)
        self.iter_meth.place(x=730, y=5)

    def to_integral(self):
        self.delete_widgets(self.label_f, self.entry_f, self.label_a2, self.entry_a2, self.label_a1, self.entry_a1,
                            self.iter_meth, self.newton_meth)
        self.label_f = Label(self.interpol, text="y =", font=big_font)
        self.label_f.place(x=0, y=110)
        self.entry_f = Entry(self.interpol, font=big_font, width=30, textvariable=self.expression)
        self.entry_f.place(x=80, y=110)

        self.label_a2 = Label(self.interpol, text="X0 =", font=big_font)
        self.label_a2.place(x=0, y=160)
        self.entry_a2 = Entry(self.interpol, font=font, width=5, textvariable=self.a)
        self.entry_a2.place(x=80, y=160)

        self.label_a1 = Label(self.interpol, text="Xk =", font=big_font)
        self.label_a1.place(x=0, y=210)
        self.entry_a1 = Entry(self.interpol, font=font, width=5, textvariable=self.second_expression)
        self.entry_a1.place(x=80, y=210)

        self.label_b1 = Label(self.interpol, text="h1 =", font=big_font)
        self.label_b1.place(x=0, y=260)
        self.entry_b1 = Entry(self.interpol, font=font, width=5, textvariable=self.b)
        self.entry_b1.place(x=80, y=260)

        self.label_b2 = Label(self.interpol, text="h2 =", font=big_font)
        self.label_b2.place(x=0, y=310)
        self.entry_b2 = Entry(self.interpol, font=font, width=5, textvariable=self.b2)
        self.entry_b2.place(x=80, y=310)

        self.iter_meth = Button(self.interpol, text="Численное\nинтегрирование", font=big_font,
                                command=self.integrate)
        self.iter_meth.place(x=750, y=5)

    def from_one_to_system(self):
        self.delete_widgets(self.label_f, self.entry_f, self.button, self.entry_a1, self.entry_b1,
                            self.label_a1, self.label_b1, self.label_ab, self.iter_meth, self.newton_meth)

        self.label_f = Label(self.nonl_eq, text="f1(x1,x2) = ", font=big_font)
        self.label_f.place(x=5, y=90)
        self.entry_f = Entry(self.nonl_eq, font=big_font, width=30, textvariable=self.expression)
        self.entry_f.place(x=180, y=91)
        self.label_g = Label(self.nonl_eq, text="f2(x1,x2) = ", font=big_font)
        self.label_g.place(x=5, y=130)
        self.entry_g = Entry(self.nonl_eq, font=big_font, width=30, textvariable=self.second_expression)
        self.entry_g.place(x=180, y=131)
        self.button = Button(self.nonl_eq, text="Ввести", command=self.show_graphs_two_vars, font=font)
        self.button.place(x=5, y=220)

        self.label_ab = Label(self.nonl_eq, text="Начальное приближение:", font=font)
        self.label_ab.place(x=0, y=290)

        self.label_a1 = Label(self.nonl_eq, text="a1 =", font=font)
        self.label_a1.place(x=340, y=260)
        self.entry_a1 = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.a)
        self.entry_a1.place(x=390, y=260)
        self.label_b1 = Label(self.nonl_eq, text="b1 =", font=font)
        self.label_b1.place(x=340, y=290)
        self.entry_b1 = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.b)
        self.entry_b1.place(x=390, y=290)

        self.label_a2 = Label(self.nonl_eq, text="a2 =", font=font)
        self.label_a2.place(x=490, y=260)
        self.entry_a2 = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.a2)
        self.entry_a2.place(x=540, y=260)
        self.label_b2 = Label(self.nonl_eq, text="b2 =", font=font)
        self.label_b2.place(x=490, y=290)
        self.entry_b2 = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.b2)
        self.entry_b2.place(x=540, y=290)

        self.iter_meth = Button(self.nonl_eq, text="Метод простых итераций", font=big_font,
                                command=self.iterations_method_system)
        self.iter_meth.place(x=650, y=20)
        self.newton_meth = Button(self.nonl_eq, text="Метод Ньютона", font=big_font, command=self.newton_method_system)
        self.newton_meth.place(x=650, y=70)

        self.eps = Label(self.nonl_eq, text="ε =", font=font).place(x=340, y=320)
        self.eps_entry = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.epsilon).place(x=390, y=320)

    def from_system_to_one(self):
        self.delete_widgets(self.label_f, self.entry_f, self.label_g, self.entry_g, self.button, self.entry_a1,
                            self.entry_b1, self.label_a1, self.label_b1, self.label_ab, self.entry_a2,
                            self.entry_b2, self.label_b2, self.label_a2, self.iter_meth, self.newton_meth)

        self.label_f = Label(self.nonl_eq, text="f(x) = ", font=big_font)
        self.label_f.place(x=5, y=90)
        self.entry_f = Entry(self.nonl_eq, font=big_font, width=35, textvariable=self.expression)
        self.entry_f.place(x=130, y=91)
        self.button = Button(self.nonl_eq, text="Ввести", command=self.show_graphs, font=font)
        self.button.place(x=5, y=220)

        self.label_ab = Label(self.nonl_eq, text="Начальное приближение:", font=font)
        self.label_ab.place(x=0, y=290)

        self.label_a1 = Label(self.nonl_eq, text="a =", font=font)
        self.label_a1.place(x=340, y=260)
        self.entry_a1 = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.a)
        self.entry_a1.place(x=390, y=260)
        self.label_b1 = Label(self.nonl_eq, text="b =", font=font)
        self.label_b1.place(x=340, y=290)
        self.entry_b1 = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.b)
        self.entry_b1.place(x=390, y=290)

        self.iter_meth = Button(self.nonl_eq, text="Метод простых итераций", font=big_font,
                                command=self.iterations_method)
        self.iter_meth.place(x=650, y=20)
        self.newton_meth = Button(self.nonl_eq, text="Метод Ньютона", font=big_font, command=self.newton_method)
        self.newton_meth.place(x=650, y=70)

        self.eps = Label(self.nonl_eq, text="ε =", font=font).place(x=340, y=320)
        self.eps_entry = Entry(self.nonl_eq, font=small_font, width=8, textvariable=self.epsilon).place(x=390, y=320)

    def get_from_input(self, is_vector_exists=True):
        if not self.n_matrix.get().isdigit():
            show_error("Неверный ввод")
            return
        global A
        A = np.matrix(np.zeros([n, n]))

        for i in range(n):
            for j in range(n):
                el = blank_to_zeros_elem(self.matrix[i][j].get())
                if not is_number(el):
                    show_error("Неверный ввод")
                    return
                A[i, j] = el

        if not is_vector_exists:
            return True

        global v
        v = np.matrix(np.zeros([n, 1]))
        for i in range(n):
            el = blank_to_zeros_elem(self.vector[i].get())
            if not is_number(el):
                show_error("Неверный ввод")
                return
            v[i, 0] = el
        return True

    def change_n_matrix(self):
        global n
        tmp = self.n_matrix.get()
        if not tmp.isdigit():
            show_error("Неверный ввод")
            return
        n = int(tmp)
        if n > 10:
            mb.showinfo("Информация", "Максимальный порядок матрицы - 10\nУстановлено значение 10")
            n = 10

        self.delete_matrix()

        for i in range(0, n):
            tmp_matr = []
            for j in range(0, n):
                entr = Entry(self.lin_alg, width=3, font=font)
                entr.place(x=10 + 36 * j, y=100 + 30 * i)
                tmp_matr.append(entr)
            self.matrix.append(tmp_matr)

        for i in range(0, len(self.vector)):
            self.vector[i].destroy()

        self.vector.clear()

        for i in range(0, n):
            vector = Entry(self.lin_alg, width=3, font=font)
            vector.place(x=30 + 36 * n, y=100 + 30 * i)
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
            if not is_number(tb) or not is_number(tv):
                show_error("Неверный ввод")
                return

            b[i, 0] = tb
            v[i, 0] = tv
            for j in range(i, i + 1):
                if j + 1 == n:
                    break
                ta = blank_to_zeros_elem(self.matrix[i + 1][j].get())
                tc = blank_to_zeros_elem(self.matrix[i][j + 1].get())
                if not is_number(ta) or not is_number(tc):
                    show_error("Неверный ввод")
                    return

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

    def show_graphs_two_vars(self):
        expr = self.expression.get()
        f1 = ""
        for i in expr:
            if i == '^':
                f1 += '**'
                continue
            f1 += i

        expr = self.second_expression.get()
        f2 = ""
        for i in expr:
            if i == '^':
                f2 += '**'
                continue
            f2 += i

        # noinspection PyBroadException
        try:
            x1 = sym.symbols('x1')
            x2 = sym.symbols('x2')

            f1 = sym.S(f1)
            f2 = sym.S(f2)
            plot1 = sym.plot_implicit(sym.Eq(f1, 0), line_color='red', show=False)
            plot2 = sym.plot_implicit(sym.Eq(f2, 0), line_color='green', show=False)
            plot1.append(plot2[0])
            plot1.show()
        except Exception:
            show_error("Неверный ввод")
            return

    def show_graphs(self):
        expr = self.expression.get()
        expression = ""
        for i in expr:
            if i == '^':
                expression += '**'
                continue
            expression += i

        xmin, xmax, dx = -100, 100, 0.01
        x_ = frange(xmin, xmax, dx)
        x = np.arange(xmin, xmax, dx)

        # noinspection PyBroadException
        try:
            y = ne.evaluate(expression)
        except Exception:
            show_error("Функция должна зависеть от переменной x")
            return
        # noinspection PyBroadException
        try:
            plt.plot(list(x_), y, linewidth=1.5)
            plt.axhline(y=0, xmin=xmin, xmax=xmax, color=(0, 1, 0))
            plt.ylim(-10, 10)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.gcf().canvas.manager.set_window_title('График')
            plt.legend(['f(x) = {}'.format(expression)])
            plt.show()
        except Exception:
            show_error("Неверный ввод функции")
            return

    def get_elem_for_nonlinear(self):
        tmp_expression = self.expression.get()
        expression = ""
        for i in tmp_expression:
            if i == '^':
                expression += '**'
                continue
            expression += i

        x = sym.Symbol('x')
        parsed = parse_expr(expression, local_dict={"log2": lambda x: sym.log(x, 2)})
        # noinspection PyBroadException
        try:
            a, b = float(self.a.get()), float(self.b.get())
        except Exception:
            show_error("Неверный ввод")
            return

        eps = self.epsilon.get()
        if eps == '':
            eps = 0.01

        # noinspection PyBroadException
        try:
            eps = float(eps)
        except Exception:
            show_error("Неверный ввод")
            return

        return parsed, a, b, eps

    def iterations_method(self):
        # noinspection PyBroadException
        try:
            expression, a, b, eps = self.get_elem_for_nonlinear()

            check, q, L = check_for_solution(str(expression), a, b)

            if not check:
                show_error("Не выполнены условия теоремы")
                return

            global x, it
            x, it = iteration_method(str(expression), a, b, q, L, eps)
            self.result_nonlinear()
        except Exception:
            show_error("Неверный ввод")

    def newton_method(self):
        # noinspection PyBroadException
        try:
            expression, a, b, eps = self.get_elem_for_nonlinear()
            check, diff_x, c = check_newton(str(expression), a, b)
            if not check:
                show_error("Произошла ошибка, проверьте функцию или отрезок [a, b]")
                return

            global x, it
            x, it = newton_method_(str(expression), diff_x, c, eps)
            self.result_nonlinear()
        except Exception:
            show_error("Неверный ввод")
            return

    def get_elem_for_nonlinear_systems(self):
        tmp_expression1 = self.expression.get()
        tmp_expression2 = self.second_expression.get()
        expression1 = ""
        expression2 = ""
        for i in tmp_expression1:
            if i == '^':
                expression1 += '**'
                continue
            expression1 += i
        for i in tmp_expression2:
            if i == '^':
                expression2 += '**'
                continue
            expression2 += i

        x1 = sym.Symbol('x1')
        x2 = sym.Symbol('x2')
        try:
            parsed1 = parse_expr(expression1, local_dict={"log2": lambda x: sym.log(x, 2)})
            parsed2 = parse_expr(expression2, local_dict={"log2": lambda x: sym.log(x, 2)})
        except Exception:
            show_error("Неверный ввод")
            return
        # noinspection PyBroadException
        try:
            a1, b1, a2, b2 = float(self.a.get()), float(self.b.get()), float(self.a2.get()), float(self.b2.get())
        except Exception:
            show_error("Неверный ввод")
            return

        eps = self.epsilon.get()
        if eps == '':
            eps = 0.01

        # noinspection PyBroadException
        try:
            eps = float(eps)
        except Exception:
            show_error("Неверный ввод")
            return

        return parsed1, parsed2, a1, b1, a2, b2, eps

    def newton_method_system(self):
        expr1, expr2, a1, b1, a2, b2, eps = self.get_elem_for_nonlinear_systems()
        global x, y, it
        x, y, it = newton_method_systems_(str(expr1), str(expr2), a1, b1, a2, b2, eps)
        if x is None:
            show_error("Вырожденная матрица J")
            return
        self.result_nonlinear_system()

    def iterations_method_system(self):
        expr1, expr2, a1, b1, a2, b2, eps = self.get_elem_for_nonlinear_systems()
        check, q = check_iter_(str(expr1), str(expr2), a1, b1, a2, b2)
        if not check:
            show_error("Не выполнено условие теоремы")
            return
        global x, y, it
        x, y, it = iter_method_systems_(str(expr1), str(expr2), q, a1, b1, a2, b2, eps)
        if x is None:
            show_error("Не выполнено условие теоремы")
            return
        self.result_nonlinear_system()

    def get_for_interpolation(self):
        try:
            expr = self.expression.get()
            X_ = float(self.a.get())
            x_ar = self.second_expression.get().split(',')
        except Exception:
            show_error("Неверный ввод")
            return None, None, None
        return expr, X_, x_ar

    def interpolation_method_lagrange(self):
        expr, X_, x_ar = self.get_for_interpolation()
        if expr is None:
            return
        global L, R
        L, R = lagrange(expr, X_, x_ar)
        if L is None:
            show_error("Неверный ввод")
            return
        self.result_interpolation_methods()

    def interpolation_method_newton(self):
        expr, X_, x_ar = self.get_for_interpolation()
        if expr is None:
            return
        global L, R
        L, R = newton(expr, X_, x_ar)
        if L is None:
            show_error("Неверный ввод")
            return
        self.result_interpolation_methods()

    def get_for_spline(self):
        try:
            xi = self.expression.get().split(',')
            fi = self.second_expression.get().split(',')
            X = self.a.get()
        except Exception:
            show_error("Неверный ввод")
            return None, None, None
        return xi, fi, X

    def spline(self):
        xi, fi, X_ = self.get_for_spline()
        if xi is None:
            return
        global L, R
        L, R = spline_interpol(xi, fi, X_)
        if L is None:
            show_error("Неверный ввод")
            return
        self.result_spline()

    def get_for_mnk(self):
        try:
            xi = self.expression.get().split(',')
            fi = self.second_expression.get().split(',')
        except Exception:
            show_error("Неверный ввод")
            return None, None
        return xi, fi

    def mnk(self):
        global x_swapped, y
        x_swapped, y = self.get_for_mnk()
        if x_swapped is None:
            return
        global L, U, A, R
        L, U, A, R = mnk(x_swapped, y)
        if L is None:
            show_error("Неверный ввод")
            return
        self.result_mnk()

    def derivative(self):
        xi, yi, X_ = self.get_for_spline()
        if xi is None:
            return
        global A, R
        A, R = num_derivative(xi, yi, X_)
        if A is None:
            show_error("Неверный ввод")
            return
        self.result_derivative()

    def get_for_integrate(self):
        try:
            expr = self.expression.get()
            X0 = self.a.get()
            Xk = self.second_expression.get()
            h1 = self.b.get()
            h2 = self.b2.get()
        except Exception:
            show_error("Неверный ввод")
            return None, None, None, None, None
        return expr, X0, Xk, h1, h2

    def integrate(self):
        expr, X0, Xk, h1, h2 = self.get_for_integrate()
        if expr is None:
            return
        global L, U, A, R
        L, U, A, R = num_integrate(expr, X0, Xk, h1, h2)
        if L is None:
            show_error("Неверный ввод")
            return
        self.result_integral()

    def euler_cauchy(self):
        expr = self.expression.get()
        y0 = self.a.get()
        z0 = self.a2.get()
        xc = self.b.get().split(',')
        h = self.b2.get()
        global L, A, R
        L, A, R = euler_method(expr, y0, z0, xc[0], xc[1], h)
        self.result_cauchy()

    def runge_kutta_(self):
        expr = self.expression.get()
        y0 = self.a.get()
        z0 = self.a2.get()
        xc = self.b.get().split(',')
        h = self.b2.get()
        global L, A, R
        L, A, R = runge_kutta(expr, y0, z0, xc[0], xc[1], h)
        self.result_cauchy()

    def adams_(self):
        expr = self.expression.get()
        y0 = self.a.get()
        z0 = self.a2.get()
        xc = self.b.get().split(',')
        h = self.b2.get()
        global L, A, R
        L, A, R = adams(expr, y0, z0, xc[0], xc[1], h)
        self.result_cauchy()


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


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
