import tkinter as tk
from tkinter import *

first_axis_x = 0
first_axis_y = 0
first_axis_z = 0
first_x = 0
first_y = 0
accuracy = 120
first_z = 0
second_x = 0
second_y = 0
second_z = 0
third_x = 0
third_y = 0
third_z = 0
light_change = 0
rotating_x = 0
rotating_y = 0
rotating_z = 0
parts = 8


def return_parts():
    return int(parts)


def return_accuracy():
    return int(accuracy)


def return_light():
    return light_change


def return_first_axis_x():
    return float(first_axis_x)


def return_first_axis_y():
    return float(first_axis_y)


def return_first_axis_z():
    return float(first_axis_z)


def return_first_x():
    return float(first_x)


def return_first_y():
    return float(first_y)


def return_first_z():
    return float(first_z)


def return_second_x():
    return float(second_x)


def return_second_y():
    return float(second_y)


def return_second_z():
    return float(second_z)


def return_third_x():
    return float(third_x)


def return_third_y():
    return float(third_y)


def return_third_z():
    return float(third_z)


def return_rotating_x():
    return rotating_x


def return_rotating_y():
    return rotating_y


def return_rotating_z():
    return rotating_z


def change_accuracy(value):
    global accuracy
    accuracy = value


def change_first_axis_x(value):
    global first_axis_x
    first_axis_x = value


def change_first_axis_y(value):
    global first_axis_y
    first_axis_y = value


def change_first_axis_z(value):
    global first_axis_z
    first_axis_z = value


def change_first_x(value):
    global first_x
    first_x = value


def change_first_y(value):
    global first_y
    first_y = value


def change_first_z(value):
    global first_z
    first_z = value


def change_second_x(value):
    global second_x
    second_x = value


def change_second_y(value):
    global second_y
    second_y = value


def change_second_z(value):
    global second_z
    second_z = value


def change_third_x(value):
    global third_x
    third_x = value


def light_on():
    global light_change
    light_change = 1


def light_off():
    global light_change
    light_change = 0


def change_third_y(value):
    global third_y
    third_y = value


def change_third_z(value):
    global third_z
    third_z = value


def change_rotating_x(value):
    global rotating_x
    rotating_x = value


def change_rotating_y(value):
    global rotating_y
    rotating_y = value


def change_rotating_z(value):
    global rotating_z
    rotating_z = value


def change_parts(value):
    global parts
    parts = value


def make_window():
    window = tk.Tk()
    window.title("Окно управления")
    window.geometry('400x750')
    count = 0
    var1 = IntVar()

    rad1 = Radiobutton(window, text="Выключить изменение кривой", value=1, variable=var1, command=light_off)
    rad2 = Radiobutton(window, text="Включить изменение кривой", value=2, variable=var1, command=light_on)
    rad1.grid(row=count, column=0)
    rad2.grid(row=count, column=1)
    count += 1

    scale_big_axis = tk.Scale(window, from_=0, to=10, resolution=0.1, orient=HORIZONTAL, command=change_first_axis_x)
    label_big_axis = tk.Label(window, text="first_axis_x")
    label_big_axis.grid(row=count, column=0)
    scale_big_axis.grid(row=count, column=1)
    count += 1

    scale_small_axis = tk.Scale(window, from_=0, to=10, resolution=0.1, orient=HORIZONTAL, command=change_first_axis_y)
    label_small_axis = tk.Label(window, text="first_axis_y")
    label_small_axis.grid(row=count, column=0)
    scale_small_axis.grid(row=count, column=1)
    count += 1

    scale_height = tk.Scale(window, from_=0, to=10, resolution=0.1, orient=HORIZONTAL, command=change_first_axis_z)
    label_height = tk.Label(window, text="first_axis_z")
    label_height.grid(row=count, column=0)
    scale_height.grid(row=count, column=1)
    count += 1

    scale_big_axis = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_first_x)
    label_big_axis = tk.Label(window, text="first_x")
    label_big_axis.grid(row=count, column=0)
    scale_big_axis.grid(row=count, column=1)
    count += 1

    scale_small_axis = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_first_y)
    label_small_axis = tk.Label(window, text="first_y")
    label_small_axis.grid(row=count, column=0)
    scale_small_axis.grid(row=count, column=1)
    count += 1

    scale_height = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_first_z)
    label_height = tk.Label(window, text="first_z")
    label_height.grid(row=count, column=0)
    scale_height.grid(row=count, column=1)
    count += 1

    scale_accuracy = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_second_x)
    label_accuracy = tk.Label(window, text="second_x")
    label_accuracy.grid(row=count, column=0)
    scale_accuracy.grid(row=count, column=1)
    count += 1

    scale_rotating_x = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_second_y)
    label_rotating_x = tk.Label(window, text="second_y")
    label_rotating_x.grid(row=count, column=0)
    scale_rotating_x.grid(row=count, column=1)
    count += 1

    scale_rotating_y = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_second_z)
    label_rotating_y = tk.Label(window, text="second_z")
    label_rotating_y.grid(row=count, column=0)
    scale_rotating_y.grid(row=count, column=1)
    count += 1

    scale_rotating_z = tk.Scale(window, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, command=change_third_x)
    label_rotating_z = tk.Label(window, text="third_x")
    label_rotating_z.grid(row=count, column=0)
    scale_rotating_z.grid(row=count, column=1)
    count += 1

    scale_intensivity = tk.Scale(window, from_=-10, to=10, orient=HORIZONTAL, resolution=0.1, command=change_third_y)
    label_intensivity = tk.Label(window, text="third_y")
    label_intensivity.grid(row=count, column=0)
    scale_intensivity.grid(row=count, column=1)
    count += 1

    scale_diffuse = tk.Scale(window, from_=-10, to=10, orient=HORIZONTAL, resolution=0.1, command=change_third_z)
    label_diffuse = tk.Label(window, text="third_z")
    label_diffuse.grid(row=count, column=0)
    scale_diffuse.grid(row=count, column=1)
    count += 1

    scale_rotating_x = tk.Scale(window, from_=0, to=360, orient=HORIZONTAL, length=150, command=change_rotating_x)
    label_rotating_x = tk.Label(window, text="Вращение света по оси x")
    label_rotating_x.grid(row=count, column=0)
    scale_rotating_x.grid(row=count, column=1)
    count += 1

    scale_rotating_y = tk.Scale(window, from_=0, to=360, orient=HORIZONTAL, length=150, command=change_rotating_y)
    label_rotating_y = tk.Label(window, text="Вращение света по оси y")
    label_rotating_y.grid(row=count, column=0)
    scale_rotating_y.grid(row=count, column=1)
    count += 1

    scale_rotating_z = tk.Scale(window, from_=0, to=360, orient=HORIZONTAL, length=150, command=change_rotating_z)
    label_rotating_z = tk.Label(window, text="Вращение света по оси z")
    label_rotating_z.grid(row=count, column=0)
    scale_rotating_z.grid(row=count, column=1)
    count += 1

    # scale_accuracy = tk.Scale(window, from_=120, to=1000, orient=HORIZONTAL, length=150, command=change_accuracy)
    # label_accuracy = tk.Label(window, text="Точность")
    # label_accuracy.grid(row=count, column=0)
    # scale_accuracy.grid(row=count, column=1)
    # count += 1

    scale_parts = tk.Scale(window, from_=8, to=64, orient=HORIZONTAL, command=change_parts)
    label_parts = tk.Label(window, text="Точность")
    label_parts.grid(row=count, column=0)
    scale_parts.grid(row=count, column=1)
    count += 1

    tk.mainloop()

