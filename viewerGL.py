#!/usr/bin/env python3

from re import X
from sre_constants import JUMP
import OpenGL.GL as GL
import OpenGL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Camera
import Pyramid
import arrow
import math
import time
 
class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'Pyramid Attack', None, None)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)
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
        self.bool_draw_bounding_boxes = False

        self.timer_shoot = 1
        self.time_last_shoot = 0
        self.timer_BB = 0.4
        self.time_last_BB = 0

        # pour faire un saut de 1 metre: (voir jumpforce.py)
        self.jumping_force = 19910
        self.bool_jumping = False
        self.delta_posZ = 0.1
        self.delta_posX = 0.1
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

                # affichage des objets
                for obj in self.objs:
                    GL.glUseProgram(obj.object.program)
                    if isinstance(obj.object, Object3D):
                        self.update_camera(obj.object.program)
                    obj.object.draw()
                self.text_life.draw()
                self.objs_humain.move_BB()
                
                # mouvement des prohectiles
                for proj in self.objs_projectile :
                    proj.mov_arrow()
                # mouvement des pyramides + collisions
                for pyramid in self.objs_pyramide:
                    pyramid.mouvement(self.objs_humain)
                    pyramid.collision()

                # gestion des BoundingBox
                if self.bool_draw_bounding_boxes:
                    for bb in self.objs_bounding_boxes:
                        bb.object.draw()

                self.update_key()
                self.gravitation()
                self.update_line()

            else:
                GL.glClearColor(0.2, 0.2, 0.2, 0.5)
                self.text_pause.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
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

    def add_object_pyramide(self, obj):
        self.objs_pyramide.append(obj)

    def add_bounding_box(self, obj):
        self.objs_bounding_boxes.append(obj)

    def add_humain(self, obj):
        self.objs_humain = obj

    def set_camera(self, cam):
        self.cam = cam
        glfw.set_cursor_pos_callback(self.window, self.cam.cursor_pos_callback)



    def update_camera(self, prog):
        GL.glUseProgram(prog)
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1):
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        if (loc == -1):
            print("Pas de variable uniforme : rotation_center_view")
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)
        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1):
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1):
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        #mouvement joueur
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0:
            self.objs_humain.object.transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs_humain.object.transformation.rotation_euler), pyrr.Vector3([0, 0, self.delta_posZ]))
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
            self.objs_humain.object.transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs_humain.object.transformation.rotation_euler), pyrr.Vector3([0, 0, self.delta_posZ]))
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0:
            self.objs_humain.object.transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs_humain.object.transformation.rotation_euler), pyrr.Vector3([self.delta_posX, 0, 0]))
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0:
            self.objs_humain.object.transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs_humain.object.transformation.rotation_euler), pyrr.Vector3([self.delta_posX, 0, 0]))
        #jumping
        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
            if not self.bool_jumping:
                self.bool_jumping = True
                self.accelerationY += self.jumping_force/self.weight
        #affichage BoundingBox
        if glfw.KEY_B in self.touch and self.touch[glfw.KEY_B] > 0:
            if self.time_last_BB + self.timer_BB <= time.time():
                self.bool_draw_bounding_boxes = not self.bool_draw_bounding_boxes
                self.time_last_BB = time.time()
        #Rotation camera 3P
        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.02
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.02
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.02
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.02
        # choix 1P ou 3P
        if self.lock_cam:
            self.cam.transformation.rotation_center = self.objs_humain.object.transformation.translation + self.objs_humain.object.transformation.rotation_center
            # on peut choisir l'offset lorsque l'on suit l'objet
            self.cam.transformation.translation = self.objs_humain.object.transformation.translation + pyrr.Vector3([0, 0.75, 2.556])
        # Shoot
        if glfw.KEY_X in self.touch and self.touch[glfw.KEY_X]> 0 :
            self.shoot()

        state = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT);
        if (state == glfw.PRESS) :
            self.shoot()

    def gravitation(self):
        self.velocityY += self.accelerationY * self.dt
        X = self.objs_humain.object.transformation.translation.x
        Y = self.objs_humain.object.transformation.translation.y
        Z = self.objs_humain.object.transformation.translation.z
        if self.objs_humain.object.transformation.translation.y + self.velocityY * self.dt < 0.5 and not (X > 25 or X < -25) and not (Z > 25 or Z < -25) and Y > -0.5:
            self.velocityY = 0
            self.bool_jumping = False
        if self.objs_humain.object.transformation.translation.y < -10:
            self.objs_humain.object.transformation.translation.x = 0
            self.objs_humain.object.transformation.translation.y = 0.75
            self.objs_humain.object.transformation.translation.z = 0
        self.objs_humain.object.transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs_humain.object.transformation.rotation_euler), pyrr.Vector3([0, self.velocityY * self.dt, 0]))
        self.accelerationY = self.gravity


    def shoot(self) :
        if self.time_last_shoot + self.timer_shoot <= time.time() :
            proj = arrow.Arrow(vie=1, coord=self.objs_humain.object.transformation.translation, rot=[0,0,0], obj=self.dic_obj["arrow"],texture=self.dic_text["arrow"], viewer=self, name="arrow",vao_obj=self.dic_vao["arrow"])
            proj.create()
            proj.size = pyrr.Vector3([0.15, 0.15, 0.25])
            proj.object.transformation.translation.y += self.objs_humain.object.transformation.translation.y +0.1
            proj.object.transformation.rotation_euler[pyrr.euler.index().yaw] = self.objs_humain.object.transformation.rotation_euler[pyrr.euler.index().yaw]
            proj.object.transformation.rotation_euler[pyrr.euler.index().roll] = -self.cam.transformation.rotation_euler[pyrr.euler.index().roll]
            self.objs_projectile.append(proj)
            self.time_last_shoot = time.time()

    def update_line(self):
        self.line.object.transformation.translation = self.objs_humain.object.transformation.translation + 0.1
        self.line.object.transformation.rotation_euler[pyrr.euler.index().yaw] = self.objs_humain.object.transformation.rotation_euler[pyrr.euler.index().yaw]
        self.line.object.transformation.rotation_euler[pyrr.euler.index().roll] = -self.cam.transformation.rotation_euler[pyrr.euler.index().roll]
