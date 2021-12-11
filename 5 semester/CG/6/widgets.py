import tkinter as tk
from tkinter import *

radius = 3
height = 5
accuracy = 3
small_axis = 3
big_axis = 3
light_change = 0
rotating_x = 0
rotating_y = 0
rotating_z = 0
intensivity = 0
diffuse = 0


def return_height():
    return height


def return_big_axis():
    return big_axis


def return_small_axis():
    return small_axis


def return_accuracy():
    return accuracy


def return_light_change():
    return light_change


def return_rotating_x():
    return rotating_x


def return_rotating_y():
    return rotating_y


def return_rotating_z():
    return rotating_z


def return_intensivity():
    return intensivity


def return_diffuse():
    return diffuse


def change_big_axis(value):
    global big_axis
    big_axis = value


def change_small_axis(value):
    global small_axis
    small_axis = value


def change_height(value):
    global height
    height = value


def change_accuracy(value):
    global accuracy
    accuracy = value


def change_rotating_x(value):
    global rotating_x
    rotating_x = value


def change_rotating_y(value):
    global rotating_y
    rotating_y = value


def change_rotating_z(value):
    global rotating_z
    rotating_z = value


def light_on():
    global light_change
    light_change = 1


def light_off():
    global light_change
    light_change = 0


def make_window():
    window = tk.Tk()
    window.title("Окно управления")
    window.geometry('450x450')

    var1 = IntVar()

    rad1 = Radiobutton(window, text="Выключить освещение", value=1, variable=var1, command=light_off)
    rad2 = Radiobutton(window, text="Включить освещение", value=2, variable=var1, command=light_on)
    rad1.grid(row=4, column=0)
    rad2.grid(row=4, column=1)

    scale_big_axis = tk.Scale(window, from_=3, to=15, orient=HORIZONTAL, command=change_big_axis)
    label_big_axis = tk.Label(window, text="Первая полуось")
    label_big_axis.grid(row=0, column=0)
    scale_big_axis.grid(row=0, column=1)

    scale_small_axis = tk.Scale(window, from_=3, to=15, orient=HORIZONTAL, command=change_small_axis)
    label_small_axis = tk.Label(window, text="Вторая полуось")
    label_small_axis.grid(row=1, column=0)
    scale_small_axis.grid(row=1, column=1)

    scale_height = tk.Scale(window, from_=5, to=20, orient=HORIZONTAL, command=change_height)
    label_height = tk.Label(window, text="Высота")
    label_height.grid(row=2, column=0)
    scale_height.grid(row=2, column=1)

    scale_accuracy = tk.Scale(window, from_=3, to=100, orient=HORIZONTAL, length=150, command=change_accuracy)
    label_accuracy = tk.Label(window, text="Точность")
    label_accuracy.grid(row=3, column=0)
    scale_accuracy.grid(row=3, column=1)

    scale_rotating_x = tk.Scale(window, from_=0, to=360, orient=HORIZONTAL, length=150, command=change_rotating_x)
    label_rotating_x = tk.Label(window, text="Вращение света по оси x")
    label_rotating_x.grid(row=5, column=0)
    scale_rotating_x.grid(row=5, column=1)

    scale_rotating_y = tk.Scale(window, from_=0, to=360, orient=HORIZONTAL, length=150, command=change_rotating_y)
    label_rotating_y = tk.Label(window, text="Вращение света по оси y")
    label_rotating_y.grid(row=6, column=0)
    scale_rotating_y.grid(row=6, column=1)

    scale_rotating_z = tk.Scale(window, from_=0, to=360, orient=HORIZONTAL, length=150, command=change_rotating_z)
    label_rotating_z = tk.Label(window, text="Вращение света по оси z")
    label_rotating_z.grid(row=7, column=0)
    scale_rotating_z.grid(row=7, column=1)

    tk.mainloop()

