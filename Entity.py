
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

class Entity()   :
    """
    Entity
    Description:
    cree la base de chaque pyramide ou joueur
    """
    def __init__(self,vie,coord,rot,obj,texture,scale,viewer,program3d_id,name) :
        self.coord = coord #position de l'entité au début [x,y,z]
        self.rot = rot #rotation de l'entité
        self.life = vie #vie de l'entité
        self.obj=obj
        self.scale = scale #taille de l'entité
        self.texture =texture
        self.liste_projectile = []
        self.viewer = viewer
        self.program3d_id = program3d_id
        self.name = name
        self.object = None


    def create(self):
        """
        create
        Description:
        cree l entité
        """

        m = Mesh.load_obj(self.obj)
        m.normalize()
        # Taille de la pyramide
        m.apply_matrix(pyrr.matrix44.create_from_scale(self.scale))
        tr = Transformation3D()
        tr.translation.x = self.coord[0]
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = self.coord[2]
        
        tr.rotation_center.x = self.rot[0]
        tr.rotation_center.y = self.rot[1]
        tr.rotation_center.z = self.rot[2]
        texture = glutils.load_texture(self.texture)

        self.object = Object3D(m.load_to_gpu(), m.get_nb_triangles(),
                    self.program3d_id, texture, tr)
        self.viewer.add_object(self.object)
        if self.name == "pyramide":
            self.viewer.add_object_pyamide(self.object)
        if self.name == "projectile" :
            self.viewer.add_object_projectile(self.object)
        if self.name == "humain" :
            self.viewer.add_object_humain(self.object)