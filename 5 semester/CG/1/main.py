# x = a*sin(t), y = b*cos(t)
import numpy as np
import pylab
from matplotlib.widgets import Slider


def add_plot(a, b, t):
    x = a * np.sin(t)
    y = b * np.cos(t)
    graph_axes.plot(x, y, label='x = a * sin(t)\ny = b * cos(t)')
    graph_axes.legend(loc='upper right')
    graph_axes.grid()
    graph_axes.axis('equal')
    pylab.draw()


if __name__ == "__main__":
    def update_graphic():
        global slider_a
        global slider_b
        global graph_axes

        a = slider_a.val
        b = slider_b.val
        t = np.arange(0, slider_t.val, 0.01)
        graph_axes.clear()
        add_plot(a, b, t)


    def on_change_value(value):
        update_graphic()

    fig, graph_axes = pylab.subplots()

    fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)

    axes_slider_a = pylab.axes([0.05, 0.25, 0.85, 0.04])
    slider_a = Slider(axes_slider_a,
                      label='a',
                      valmin=0,
                      valmax=10,
                      valinit=1,
                      valfmt='%1.2f')
    slider_a.on_changed(on_change_value)

    axes_slider_b = pylab.axes([0.05, 0.17, 0.85, 0.04])
    slider_b = Slider(axes_slider_b,
                      label='b',
                      valmin=0,
                      valmax=10,
                      valinit=1,
                      valfmt='%1.2f')
    slider_b.on_changed(on_change_value)

    axes_slider_t = pylab.axes([0.05, 0.09, 0.85, 0.04])
    slider_t = Slider(axes_slider_t,
                      label='t',
                      valmin=0,
                      valmax=2*np.pi,
                      valinit=2*np.pi,
                      valfmt='%1.2f')
    slider_t.on_changed(on_change_value)

    update_graphic()

    pylab.show()
