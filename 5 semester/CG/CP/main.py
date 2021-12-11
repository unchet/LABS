# Ильиных Вадим М8О-301Б-19
# Составить и отладить программу, обеспечивающую каркасную визуализацию порции поверхности заданного типа.
# Исходные данные готовятся самостоятельно и вводятся из файла или в панели ввода данных. Должна быть обеспечена
# возможность тестирования программы на различных наборах исходных данных. Программа должна обеспечивать выполнение
# аффинных преобразований для заданной порции поверхности, а также возможность управлять количеством изображаемых
# параметрических линий. Для визуализации параметрических линий поверхности разрешается использовать только функции
# отрисовки отрезков в экранных координатах.
# Вариант 13:
# Поверхность вращения. Образующая – кривая Безье 3D 2-й степени

import numpy as np
import pygame
import threading
from transformations import *
from math import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from scipy.special import comb
from widgets import *

vertex = (-1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1)


def vec_len(x, y, z):
    return sqrt(x*x + y*y + z*z)


with open(str(input("Введите название файла: "))) as file:
    ar2x = float(file.readline())
    ar2y = float(file.readline())
    ar2z = float(file.readline())

    bc1x = float(file.readline())
    bc1y = float(file.readline())
    bc1z = float(file.readline())

    bc2x = float(file.readline())
    bc2y = float(file.readline())
    bc2z = float(file.readline())

    bc3x = float(file.readline())
    bc3y = float(file.readline())
    bc3z = float(file.readline())


def bernstein_poly(i, n, t):
    return comb(n, i) * (t ** i) * (1 - t) ** (n - i)


def bezier_curve(points, nTimes):
    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])
    zPoints = np.array([p[2] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array(
        [bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])

    # вычисляет скалярное произведение двух массивов.
    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)
    zvals = np.dot(zPoints, polynomial_array)

    return xvals, yvals, zvals


def calculate_points():
    check = return_light()
    accuracy = return_accuracy()
    global ar2x, ar2y, ar2z
    global bc1x, bc1y, bc1z
    global bc2x, bc2y, bc2z
    global bc3x, bc3y, bc3z
    if check:
        bc1x = return_first_x(); bc1y = return_first_y(); bc1z = return_first_z()
        bc2x = return_second_x(); bc2y = return_second_y(); bc2z = return_second_z()
        bc3x = return_third_x(); bc3y = return_third_y(); bc3z = return_third_z()

    points = [[bc1x, bc1y, bc1z], [bc2x, bc2y, bc2z], [bc3x, bc3y, bc3z]]

    xvals, yvals, zvals = bezier_curve(points, accuracy)

    if check:
        ar2x = return_first_axis_x(); ar2y = return_first_axis_y(); ar2z = return_first_axis_z()

    length = vec_len(ar2x, ar2y, ar2z)
    if length == 0:
        length = 1
        ar2z = 1

    p2 = [ar2x / length, ar2y / length, ar2z / length]

    num_curves = return_parts()
    radiane = 2*pi / num_curves
    angle = radiane

    xtvals = xvals
    ytvals = yvals
    ztvals = zvals

    while angle <= 2 * pi + 10**-6:
        m1 = rotation_matrix(angle, p2, points[0])
        m2 = rotation_matrix(angle, p2, points[1])
        m3 = rotation_matrix(angle, p2, points[2])

        pp1 = np.dot(points[0], m1[:3,:3].T)
        pp2 = np.dot(points[1], m2[:3,:3].T)
        pp3 = np.dot(points[2], m3[:3,:3].T)

        npoints = [pp1, pp2, pp3]
        xnvals, ynvals, znvals = bezier_curve(npoints, accuracy)
        xtvals = np.append(xtvals, xnvals)
        ytvals = np.append(ytvals, ynvals)
        ztvals = np.append(ztvals, znvals)
        angle += radiane

    vert = []
    vert_lines = []
    vert_gran = []

    for i in range(0, num_curves):
        for j in range(0, 2):
            vert_gran.append(xtvals[i*accuracy + j*accuracy])
            vert_gran.append(ytvals[i*accuracy + j*accuracy])
            vert_gran.append(ztvals[i*accuracy + j*accuracy])

    for i in range(0, num_curves):
        for j in range(0, 2):
            vert_gran.append(xtvals[i*accuracy + j*accuracy + accuracy - 1])
            vert_gran.append(ytvals[i*accuracy + j*accuracy + accuracy - 1])
            vert_gran.append(ztvals[i*accuracy + j*accuracy + accuracy - 1])

    for i in range(0, len(xtvals)):
        vert_lines.append(xtvals[i])
        vert_lines.append(ytvals[i])
        vert_lines.append(ztvals[i])

    for l in range(0, num_curves):
        for i in range(0, accuracy):
            for j in range(0, 2):
                vert.append(xtvals[accuracy*l + i + accuracy*j])
                vert.append(ytvals[accuracy*l + i + accuracy*j])
                vert.append(ztvals[accuracy*l + i + accuracy*j])

    for i in range(0, accuracy):
        for j in range(0, 2):
            vert.append(xtvals[i + accuracy * j])
            vert.append(ytvals[i + accuracy * j])
            vert.append(ztvals[i + accuracy * j])

    return vert, vert_lines, vert_gran


def init_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glPushMatrix()

    alpha = int(return_rotating_x())
    betta = int(return_rotating_y())
    gamma = int(return_rotating_z())
    intens = 0.3
    intens_diff = 1.0
    #
    glRotatef(alpha, 1, 0, 0)
    glRotatef(betta, 0, 1, 0)
    glRotatef(gamma, 0, 0, 1)

    k = 15

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (intens, intens, intens, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (intens_diff, intens_diff, intens_diff, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0.8 * k, 0.3 * k, 0.6 * k, 1))

    glTranslatef(0.8 * k, 0.3 * k, 0.6 * k)

    glScalef(0.3, 0.3, 0.3)
    glColor3f(1, 0, 0)
    draw_light()
    glPopMatrix()


def draw_light():
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertex)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glDisableClientState(GL_VERTEX_ARRAY)


if __name__ == "__main__":
    t1 = threading.Thread(target=make_window)
    t1.start()
    nPoints = 3

    pygame.init()
    (width, height) = (900, 700)
    screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
    pygame.display.set_caption('Вадим Ильиных М8О-301Б-19')
    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -30)
    glLineWidth(2)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                pressed = pygame.mouse.get_pressed(3)
                if pressed[0]:
                    glRotatef(2, event.rel[1], event.rel[0], 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glScalef(1.1, 1.1, 1.1)
                elif event.button == 5:
                    glScalef(0.9, 0.9, 0.9)

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            glRotatef(1, 0, -1, 0)
        if key[pygame.K_RIGHT]:
            glRotatef(1, 0, 1, 0)
        if key[pygame.K_UP]:
            glRotatef(1, -1, 0, 0)
        if key[pygame.K_DOWN]:
            glRotatef(1, 1, 0, 0)
        if key[pygame.K_q]:
            glRotatef(1, 0, 0, -1)
        if key[pygame.K_e]:
            glRotatef(1, 0, 0, 1)
        if key[pygame.K_KP_PLUS] or key[pygame.K_PLUS]:
            glScalef(1.1, 1.1, 1.1)
        if key[pygame.K_MINUS] or key[pygame.K_KP_MINUS]:
            glScalef(0.9, 0.9, 0.9)
        if key[pygame.K_r]:
            glLoadIdentity()
            gluPerspective(45, (width / height), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -40)
            glLineWidth(2)

        vert, vert_lines, vert_gran = calculate_points()

        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        init_light()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vert)
        glColor(0,1,0)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vert)//3)
        glVertexPointer(3, GL_FLOAT, 0, vert_lines)
        glColor(0,0,0,1)
        glDrawArrays(GL_LINE_STRIP, 0, len(vert_lines)//3)
        glVertexPointer(3, GL_FLOAT, 0, vert_gran)
        glColor(0, 0, 0, 1)
        glDrawArrays(GL_LINES, 0, len(vert_gran) // 3)
        glDisableClientState(GL_VERTEX_ARRAY)

        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)

        pygame.display.flip()
        clock = pygame.time.Clock()

