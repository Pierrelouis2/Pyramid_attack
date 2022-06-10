
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

    def __init__(self, vie, coord, rot, obj, texture, viewer, name,vao_obj):
        self.coord = coord  # position de l'entité au début [x,y,z]
        self.rot = rot  # rotation de l'entité
        self.life = vie  # vie de l'entité
        self.obj = obj
        self.texture = texture
        self.liste_projectile = []
        self.viewer = viewer
        self.program3d_id = viewer.program3d_id
        self.name = name
        self.object = None
        self.bounding_box= None 
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
            self.object = Object3D(self.vao, self.obj.get_nb_triangles(),self.program3d_id, self.texture, tr)
        else: 
            self.object = Object3D(self.vao, self.obj.get_nb_triangles(),self.program3d_id, self.texture, Transformation3D())

        self.viewer.add_object(self.object)
        if self.name == "pyramid":
            self.viewer.add_object_pyramide(self)
        if self.name == "humain" :
            self.viewer.add_humain(self)

        if self.name != "sol":
            self.bounding_box = BoundingBox(self)


class BoundingBox:
    def __init__(self, entity):
        self.name = "bounding_box"
        self.entity = entity
        self.viewer = entity.viewer
        self.entity_bound = entity
        self.position = entity.object.transformation.translation
        self.coord = entity.coord
        self.obj = entity.viewer.dic_obj[f"cube_{entity.name}"]
        self.texture = entity.viewer.dic_text["cube"]
        self.create()

    def create(self):
        #self.obj.apply_matrix(pyrr.matrix44.create_from_scale(self.scale*2))
        tr = Transformation3D()
        tr.translation.x = self.coord[0]
        tr.translation.y = -np.amin(self.obj.vertices, axis=0)[1]
        tr.translation.z = self.coord[2]
        tr.rotation_center.x = self.entity.rot[0]
        tr.rotation_center.y = self.entity.rot[1]
        tr.rotation_center.z = self.entity.rot[2]
        self.object = Object3D(self.entity.viewer.dic_vao[f"cube_{self.entity.name}"], self.obj.get_nb_triangles(),self.viewer.program3d_id, self.texture, tr)
        self.viewer.add_bounding_box(self.object)

    def intersect(self,position):
        return pyrr.vector3.length(self.position-position) < 1

    def intersectB(self,bounding_box):
        return pyrr.vector3.length(self.position - bounding_box.position) < 1 + bounding_box.position

    def intersectE(self,entity):
        if entity.object.bounding_box.intersectB(self):
            for bounding_box in self.viewer.bounding_boxes:
                if bounding_box.intersectB(self):
                    return True
        return False

