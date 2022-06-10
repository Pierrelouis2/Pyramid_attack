
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr


class Entity():
    """
    Entity
    Description:
    cree la base de chaque pyramide ou joueur
    """

    def __init__(self, vie, coord, rot, obj, texture, viewer, program3d_id, name,vao_obj):
        self.coord = coord  # position de l'entité au début [x,y,z]
        self.rot = rot  # rotation de l'entité
        self.life = vie  # vie de l'entité
        self.obj = obj
        self.texture = texture
        self.liste_projectile = []
        self.viewer = viewer
        self.program3d_id = program3d_id
        self.name = name
        self.object = None
        self.vao = vao_obj

    def create(self):
        """
        create
        Description:
        cree l entité
        """
       

        if self.name != "sol" :

            
            tr = Transformation3D()
            tr.translation.x = self.coord[0]
            tr.translation.y = -np.amin(self.obj.vertices, axis=0)[1]
            tr.translation.z = self.coord[2]

            tr.rotation_center.x = self.rot[0]
            tr.rotation_center.y = self.rot[1]
            tr.rotation_center.z = self.rot[2]


            self.object = Object3D(self.vao, self.obj.get_nb_triangles(),
                                self.program3d_id, self.texture, tr)
        
        if self.name == "sol" : 
            self.object = Object3D(self.vao, self.obj.get_nb_triangles(),
                            self.program3d_id, self.texture, Transformation3D())

        self.viewer.add_object(self.object)
        if self.name == "pyramide":
            self.viewer.add_object_pyamide(self)
        if self.name == "projectile":
            self.viewer.add_object_projectile(self)
        if self.name == "humain" :
            self.viewer.add_humain(self)
