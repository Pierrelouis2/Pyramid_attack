
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
        self.bounding_boxe= None 
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
            self.viewer.add_object_projectile(self.object)
        if self.name == "humain" :
            self.viewer.add_humain(self)
        
        self.bounding_boxes = BoundingBox(self)


class BoundingBox:
    def __init__(self, entity):
        self.name = "bounding_box"
        self.viewer = entity.viewer
        self.entity_bound = entity
        self.position = entity.object.transformation.translation
        self.coord = entity.coord
        self.obj = entity.dict_obj["cube"]
        self.texture = entity.dict_text["cube"]

    def create(self):
        self.obj.apply_matrix(pyrr.matrix44.create_from_scale(self.scale))
        tr = Transformation3D()
        tr = Transformation3D()
        tr.translation.x = self.coord[0]
        tr.translation.y = -np.amin(self.obj.vertices, axis=0)[1]
        tr.translation.z = self.coord[2]
        tr.rotation_center.x = self.rot[0]
        tr.rotation_center.y = self.rot[1]
        tr.rotation_center.z = self.rot[2]
        self.object3D = Object3D(self.obj, self.obj.get_nb_triangles(),self.viewer.program3d_id, self.texture, tr)
        self.viewer.add_bounding_box(self.object3D)

    def intersect(self,position):
        return pyrr.vector3.length(self.position-position) < self.size

    def intersectB(self,bounding_box):
        return pyrr.vector3.length(self.position - bounding_box.position) < self.size+ bounding_box.position

    def intersectE(self,entity):
        if not entity.general_bounding_box == None:
            if entity.general_bounding_box.intersectB(self):
                for bounding_box in entity.bounding_boxes:
                    if not bounding_box == None:
                        if bounding_box.intersectB(self):
                            return True
        return False

    def adapt(self,transformation):
        self.position = transformation.translation + pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(transformation.rotation_euler), self.offset)
        self.ent.object.transformation.translation = self.position

    def draw(self):
        self.ent.render()
