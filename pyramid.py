
import Entity
import math

class Pyramid(Entity.Entity):
    #def __init__(self, vao, nb_triangle, program, texture):
    #    super().__init__(vao, nb_triangle, program, texture)
    def mouvement(self,humain) :
        
        vect =[humain.object.transformation.translation.x - self.object.transformation.translation.x,0,humain.object.transformation.translation.z  - self.object.transformation.translation.z]
        norm = math.sqrt(vect[0]*vect[0] + vect[2]*vect[2])
        vect_norm = [i/norm for i in vect]
        mov = [i*0.005 for i in vect_norm]
        self.object.transformation.translation.x += mov[0]
        self.object.transformation.translation.z += mov[2]
