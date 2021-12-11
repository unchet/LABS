# Ильиных В.М. М8О-301Б-19
# Аппроксимировать заданное тело выпуклым многогранником. Точность аппроксимации задается пользователем.
# Обеспечить возможность вращения и масштабирования многогранника и удаление невидимых линий и поверхностей.
# Реализовать простую модель закраски для случая одного источника света.
# Параметры освещения и отражающие свойства материала задаются пользователем в диалоговом режиме.
# Вариант 2:Прямой эллиптический цилиндр

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import threading
from widgets import *

stop = False
k = 1
vertex = (-1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1)


# длина вектора
def len_vector(x, y):
    return math.sqrt(x*x + y*y)


def init_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glPushMatrix()

    alpha = int(return_rotating_x())
    betta = int(return_rotating_y())
    gamma = int(return_rotating_z())
    intens = float(return_intensivity())
    intens_diff = float(return_diffuse())

    glRotatef(alpha, 1, 0, 0)
    glRotatef(betta, 0, 1, 0)
    glRotatef(gamma, 0, 0, 1)

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


def draw_cylinder():
    s_axis = float(return_small_axis())
    b_axis = float(return_big_axis())
    h = float(return_height())
    acc = float(return_accuracy())
    global k
    k = max(s_axis, b_axis, h)
    z = h / 2.0
    circle_pts = []

    for i in range(int(acc) + 1):
        angle = 2 * math.pi * (i / acc)
        x = b_axis * math.cos(angle)
        y = s_axis * math.sin(angle)
        if abs(x) < 10 ** (-10):
            x = 0
        if abs(y) < 10 ** (-10):
            y = 0
        pt = (x, y, z)
        circle_pts.append(pt)

    glBegin(GL_TRIANGLE_FAN)
    glColor(1, 0, 0)
    glNormal3f(0, 0, 1)
    for (x, y, z) in circle_pts:
        glVertex3f(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glColor(0, 0, 1)
    glNormal3f(0, 0, -1)
    for (x, y, z) in circle_pts:
        glVertex3f(x, y, -z)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)
    glColor(0, 1, 0)
    i = 0
    for (x, y, z) in circle_pts:
        x1 = (circle_pts[i][0] + circle_pts[(i + 1) % int(acc)][0]) / 2.0
        y1 = (circle_pts[i][1] + circle_pts[(i + 1) % int(acc)][1]) / 2.0
        length = len_vector(x1, y1)
        glNormal3f(x1 / length, y1 / length, 0)
        glVertex3f(x, y, z)
        glVertex3f(x, y, -z)
        i += 1
    glEnd()


t1 = threading.Thread(target=make_window)
t1.start()

pygame.init()
(width, height) = (900, 700)
screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
pygame.display.set_caption('Вадим Ильиных М8О-301Б-19')
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -30)
glEnable(GL_DEPTH_TEST)

glLineWidth(2)
clock = pygame.time.Clock()

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

    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    light_change = int(return_light_change())
    if light_change:
        init_light()

    draw_cylinder()

    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)

    pygame.display.flip()
    clock.tick(60)
