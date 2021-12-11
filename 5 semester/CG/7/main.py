# Ильиных В.М. М8О-301Б-19
# Написать программу, строящую полиномиальную кривую по заданным точкам.
# Обеспечить возможность изменения позиции точек и, при необходимости,
# значений касательных векторов и натяжения
# Вариант 12. B-сплайн. n =  6, k =  4. Узловой вектор равномерный.

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as si
from matplotlib.widgets import Slider

points = [[3, 0], [1, 1], [2, 2], [10, 3], [10, 4], [8, 5]]
points = np.array(points)
x = points[:, 0]  # x = { 5, 7, 2, 10, 10, 8}
t = points[:, 1]  # t = { 0, 1, 2, 3, 4, 5}
axcolor = 'white'


def interpol():
    global x
    global t
    ipl_t = np.linspace(min(t), max(t), 100)
    x_tup = si.splrep(t, x, k=4)
    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]
    x_i = si.splev(ipl_t, x_list)
    return [ipl_t, x_i]


def update0(val):
    global x
    global cords
    amp = samp0.val
    x[0] = amp
    cords = interpol()
    l.set_ydata(cords[1])
    a.set_ydata(x)


def update1(val):
    global x
    global cords
    amp = samp1.val
    x[1] = amp
    cords = interpol()
    l.set_ydata(cords[1])
    a.set_ydata(x)


def update2(val):
    global x
    global cords
    amp = samp2.val
    x[2] = amp
    cords = interpol()
    l.set_ydata(cords[1])
    a.set_ydata(x)


def update3(val):
    global x
    global cords
    amp = samp3.val
    x[3] = amp
    cords = interpol()
    l.set_ydata(cords[1])
    a.set_ydata(x)


def update4(val):
    global x
    global cords
    amp = samp4.val
    x[4] = amp
    cords = interpol()
    l.set_ydata(cords[1])
    a.set_ydata(x)


def update5(val):
    global x
    global cords
    amp = samp5.val
    x[5] = amp
    cords = interpol()
    l.set_ydata(cords[1])
    a.set_ydata(x)


fig = plt.figure()
ax = fig.add_subplot(211)
a, = plt.plot(t, x, '-og')
cords = interpol()
l, = plt.plot(cords[0], cords[1], 'r')
plt.xlim([min(t), max(t)])
plt.ylim([0, 11])
plt.gcf().canvas.manager.set_window_title("Ильиных В.М. М8О-301Б-19")
plt.title('B - Сплайн, n = 6, k = 4')

axamp0 = plt.axes([0.25, 0.30, 0.65, 0.03], facecolor=axcolor)
axamp1 = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
axamp2 = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
axamp3 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axamp4 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axamp5 = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

samp0 = Slider(axamp0, 'dot 0', 0.1, 10.0, valinit=points[0][0])
samp1 = Slider(axamp1, 'dot 1', 0.1, 10.0, valinit=points[1][0])
samp2 = Slider(axamp2, 'dot 2', 0.1, 10.0, valinit=points[2][0])
samp3 = Slider(axamp3, 'dot 3', 0.1, 10.0, valinit=points[3][0])
samp4 = Slider(axamp4, 'dot 4', 0.1, 10.0, valinit=points[4][0])
samp5 = Slider(axamp5, 'dot 5', 0.1, 10.0, valinit=points[5][0])

samp0.on_changed(update0)
samp1.on_changed(update1)
samp2.on_changed(update2)
samp3.on_changed(update3)
samp4.on_changed(update4)
samp5.on_changed(update5)

plt.show()
