#!/usr/bin/env python3

from re import X
from sre_constants import JUMP
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Camera
import Pyramid


 
class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.objs_pyramide = []
        self.objs_projectile = []
        self.objs_bounding_boxes = []
        self.touch = {}
        self.objs_humain = None

        self.lock_cam = True
        self.pause = False

        # pour faire un saut de 1 metre: (voir jumpforce.py)
        self.jumping_force = 19910
        self.bool_jumping = False
        self.delta_posX = 0.2
        self.gravity = -9.81
        self.weight = 75
        self.accelerationY = self.gravity
        self.velocityY = 0
        # on part du principe qu'on a 60 fps
        self.dt = 1/60

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            if not self.pause:
                GL.glClearColor(0.5, 0.6, 0.9, 1.0)
                for obj in self.objs:
                    GL.glUseProgram(obj.program)
                    if isinstance(obj, Object3D):
                        self.update_camera(obj.program)
                    obj.draw()
                for i in self.objs_pyramide:
                    i.mouvement(self.objs_humain)
                self.update_key()

                self.gravitation()

            else:
                GL.glClearColor(0.2, 0.2, 0.2, 0.5)
                self.text_pause.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()

    def key_callback(self, win, key, scancode, action, mods):
        self.win = win
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

        if key == glfw.KEY_C and action == glfw.PRESS:
            self.lock_cam = not self.lock_cam

        if key == glfw.KEY_P and action == glfw.PRESS:
            self.pause = not self.pause

        else:
            if not self.pause:
                self.touch[key] = action

    def add_object(self, obj):
        self.objs.append(obj)

    def add_object_pyamide(self, obj):
        self.objs_pyramide.append(obj)

    def add_object_projectile(self, obj):
        self.objs_projectile.append(obj)
    
    def add_bounding_box(self, obj):
        self.objs_bounding_boxes.append(obj)
        
    def add_humain(self, obj):
        self.objs_humain =obj

    def set_camera(self, cam):
        self.cam = cam
        glfw.set_cursor_pos_callback(self.window, self.cam.cursor_pos_callback)



    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1):
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1):
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x,
                       rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(
            -self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1):
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)

        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1):
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            self.objs[0].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(
                    self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, self.delta_posX]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(
                    self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, self.delta_posX]))
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
            if not self.bool_jumping:
                self.bool_jumping = True
                self.accelerationY += self.jumping_force/self.weight

        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.02
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.02
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.02
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.02

        if self.lock_cam:
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy()
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            # on peut choisir l'offset lorsque l'on suit l'objet
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 0.75, 2.556])

    def gravitation(self):
        # TODO Faire autre chose que quitter la fct
        self.velocityY += self.accelerationY * self.dt
        # condition a revoir
        X = self.objs[0].transformation.translation.x
        Y = self.objs[0].transformation.translation.y
        Z = self.objs[0].transformation.translation.z

        if self.objs[0].transformation.translation.y + self.velocityY * self.dt < 0.5 and not (X > 25 or X < -25) and not (Z > 25 or Z < -25) and Y > -0.5:
            self.velocityY = 0
            self.bool_jumping = False
        if self.objs[0].transformation.translation.y < -10:
            self.objs[0].transformation.translation.x = 0
            self.objs[0].transformation.translation.y = 0.75
            self.objs[0].transformation.translation.z = 0
        self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, self.velocityY * self.dt, 0]))
        self.accelerationY = self.gravity
