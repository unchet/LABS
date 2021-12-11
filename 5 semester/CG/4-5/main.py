# Ильиных В.М. М8О-301Б-19
# Аппроксимировать заданное тело выпуклым многогранником. Точность аппроксимации задается пользователем.
# Обеспечить возможность вращения и масштабирования многогранника и удаление невидимых линий и поверхностей.
# Реализовать простую модель закраски для случая одного источника света.
# Параметры освещения и отражающие свойства материала задаются пользователем в диалоговом режиме.
# Вариант 11: Прямой усеченный конус

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import threading
from ctypes import *
from widgets import *

stop = False
k = 1
vertex = np.array([-1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1], dtype='float32')
vertex_normal = np.array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1], dtype='float32')
vertex_normal_down = np.array([0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1], dtype='float32')


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
    intens = 0.3
    intens_diff = 1.0

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
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertex)*4, (c_float*len(vertex))(*vertex), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glEnableClientState(GL_VERTEX_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glDisableClientState(GL_VERTEX_ARRAY)


def init_shaders():
    global uniforms
    global locations
    global ambient
    global diffuse

    vert = create_shader(GL_VERTEX_SHADER, """
                varying vec4 vertex_color;
                void main(){
                    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    vertex_color = gl_Color * vec4(0.7, 0.7, 0.7, 1);
                }""")
    fragment = create_shader(GL_FRAGMENT_SHADER, """
                varying vec4 vertex_color;
                void main() {
                    gl_FragColor = vertex_color;
                }""")

    program = glCreateProgram()
    glAttachShader(program, vert)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    glUseProgram(program)


def draw_cone():
    s_axis = float(return_small_axis())
    b_axis = float(return_big_axis())
    h = float(return_height())
    h_slide = float(return_height_slide())
    acc = float(return_accuracy())
    global k
    global h_tmp
    k = max(s_axis, b_axis, h)
    z = h_slide
    circle_pts = []
    circle_pts_tmp = []
    circle_pts_mixed = []
    circle_pts_normal = []
    normal = []
    # init_shaders()

    for i in range(int(acc) + 1):
        angle = 2 * math.pi * (i / acc)
        x_bottom = b_axis * math.cos(angle)
        y_bottom = b_axis * math.sin(angle)

        x_top = s_axis * math.cos(angle)
        y_top = s_axis * math.sin(angle)

        if abs(x_bottom) < 10 ** (-10):
            x_bottom = 0
        if abs(y_bottom) < 10 ** (-10):
            y_bottom = 0
        pt = (x_bottom, y_bottom, z)
        circle_pts_normal.append(pt)
        circle_pts.append(x_top), circle_pts.append(y_top), circle_pts.append(z)
        circle_pts_tmp.append(x_bottom), circle_pts_tmp.append(y_bottom), circle_pts_tmp.append(0)
        circle_pts_mixed.append(x_top), circle_pts_mixed.append(y_top), circle_pts_mixed.append(z)
        circle_pts_mixed.append(x_bottom), circle_pts_mixed.append(y_bottom), circle_pts_mixed.append(0)

    i = 0
    for (x, y, z) in circle_pts_normal:
        x1 = (circle_pts_normal[i][0] + circle_pts_normal[(i + 1) % int(acc)][0]) / 2.0
        y1 = (circle_pts_normal[i][1] + circle_pts_normal[(i + 1) % int(acc)][1]) / 2.0
        length = len_vector(x1, y1)
        normal.append(x1 / length), normal.append(y1 / length), normal.append(0)
        i += 1

    vbo1 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo1)
    glBufferData(GL_ARRAY_BUFFER, len(circle_pts)*4, (c_float*len(circle_pts))(*circle_pts), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    vbo2 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBufferData(GL_ARRAY_BUFFER, len(circle_pts_tmp)*4, (c_float*len(circle_pts_tmp))(*circle_pts_tmp), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    vbo3 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo3)
    glBufferData(GL_ARRAY_BUFFER, len(circle_pts_mixed)*4, (c_float*len(circle_pts_mixed))(*circle_pts_mixed), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glEnableClientState(GL_VERTEX_ARRAY)

    glBindBuffer(GL_ARRAY_BUFFER, vbo1)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glNormalPointer(GL_FLOAT, 0, vertex_normal)
    glColor(1, 0, 0)
    glDrawArrays(GL_TRIANGLE_FAN, 0, int(acc+1))

    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glNormalPointer(GL_FLOAT, 0, vertex_normal_down)
    glColor(0, 0, 1)
    glDrawArrays(GL_TRIANGLE_FAN, 0, int(acc+1))

    glBindBuffer(GL_ARRAY_BUFFER, vbo3)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glNormalPointer(GL_FLOAT, 0, normal)
    glColor(0, 1, 0)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, int((acc+1)*2))

    glDisableClientState(GL_VERTEX_ARRAY)


def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


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

    draw_cone()

    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)

    pygame.display.flip()
    clock.tick(60)
