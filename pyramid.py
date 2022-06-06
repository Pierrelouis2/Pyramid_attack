import OpenGL.GL as GL
import pyrr
import numpy as np
import cpe3d as cpe
from Entity import *
import math
import random as rand

class Pyramid(Entity):
    #def __init__(self, vao, nb_triangle, program, texture):
    #    super().__init__(vao, nb_triangle, program, texture)

    def rand_pos(self,rayon):
        teta = rand.randint(0,10)
        x = rayon * math.cos(teta)
        z = rayon * math.sin(teta)
        return [x,0,z]