import OpenGL.GL as GL
import pyrr
import numpy as np
import cpe3d as cpe
from Entity import *
import math
import random as rand


class Humain(Entity):
    def test(self):
        pass

    def move_BB(self):
        self.bounding_box.object.transformation.translation.x = self.object.transformation.translation.x
        self.bounding_box.object.transformation.translation.z = self.object.transformation.translation.z
        self.bounding_box.object.transformation.rotation_euler[pyrr.euler.index().roll]= self.object.transformation.rotation_euler[pyrr.euler.index().roll]
        self.bounding_box.object.transformation.rotation_euler[pyrr.euler.index().yaw]= self.object.transformation.rotation_euler[pyrr.euler.index().yaw]
