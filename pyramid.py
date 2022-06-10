import OpenGL.GL as GL
import pyrr
import numpy as np
import cpe3d as cpe

class Pyramid(object):
    def __init__(self, vao, nb_triangle, program, texture):
        super().__init__(vao, nb_triangle, program, texture)

    def spawn(self):
        self.proba = 0.1 
        
