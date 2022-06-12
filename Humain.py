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

    def destroy(self):
        #self.viewer.objs.remove(self)
        glfw.set_window_should_close(self.viewer.window, glfw.TRUE)