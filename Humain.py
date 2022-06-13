import OpenGL.GL as GL
import pyrr
import numpy as np
import cpe3d as cpe
from Entity import *
import arrow
import math
import time
import random as rand


class Humain(Entity):
    def __init__(self, vie, coord, rot, obj, texture, viewer, name,vao_obj, ):
        super().__init__(vie, coord, rot, obj, texture, viewer, name,vao_obj)
        self.delta_posZ = 0.1
        self.delta_posX = 0.1
        self.timer_shoot = 1
        self.time_last_shoot = 0
        self.jumping_force = 19910
        self.weight = 75


    def test(self):
        pass

    def destroy(self):
        #self.viewer.objs.remove(self)
        glfw.set_window_should_close(self.viewer.window, glfw.TRUE)

    def shoot(self) :
        if self.time_last_shoot + self.timer_shoot <= time.time() :
            proj = arrow.Arrow(vie=1, coord=self.object.transformation.translation, rot=[0,0,0], obj=self.viewer.dic_obj["arrow"],texture=self.viewer.dic_text["arrow"], viewer=self.viewer, name="arrow",vao_obj=self.viewer.dic_vao["arrow"])
            proj.create()
            proj.size = pyrr.Vector3([0.15, 0.15, 0.25])
            proj.object.transformation.translation.y += self.object.transformation.translation.y +0.1
            proj.object.transformation.rotation_euler[pyrr.euler.index().yaw] = self.object.transformation.rotation_euler[pyrr.euler.index().yaw]
            proj.object.transformation.rotation_euler[pyrr.euler.index().roll] = -self.viewer.cam.transformation.rotation_euler[pyrr.euler.index().roll]
            self.viewer.objs_projectile.append(proj)
            self.time_last_shoot = time.time()

    def update_line(self):
        self.line.object.transformation.translation = self.object.transformation.translation + 0.1
        self.line.object.transformation.rotation_euler[pyrr.euler.index().yaw] = self.object.transformation.rotation_euler[pyrr.euler.index().yaw]
        self.line.object.transformation.rotation_euler[pyrr.euler.index().roll] = -self.viewer.cam.transformation.rotation_euler[pyrr.euler.index().roll]

    def collision(self):
        for bonus in self.viewer.objs_bonus:
            if self.bounding_box.intersectBB(bonus.bounding_box):
                self.bonus()

    def bonus(self):
        self.viewer.objs_bounding_boxes.remove(self.bounding_box)
        self.viewer.objs_bonus.remove(self)
        self.viewer.objs.remove(self)
        bonus = rand.randint(0,3)
        if bonus == 0:
            self.delta_posX +=0.1
        if bonus == 1:
            self.delta_posY +=0.1
        if bonus == 2:
            self.timer_shoot -= 0.1
        if bonus == 3:
            self.jumping_force += 1000