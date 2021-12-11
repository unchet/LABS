import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from coordinates import *


def cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv((1, 1, 1))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0, 0, 0))
            glVertex3fv(vertices[vertex])
    glEnd()

def actions_with_cube():
    pygame.init()
    display = (800, 600)
    pygame.display.set_caption('Вадим Ильиных М8О-301Б-19')
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glLineWidth(2)

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
        if key[pygame.K_r]:
            glLoadIdentity()
            gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -10)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    actions_with_cube()