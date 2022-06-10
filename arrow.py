from Entity import Entity, BoundingBox
import pyrr

class Arrow(Entity) :

    def mov_arrow(self) :
        self.object.transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.object.transformation.rotation_euler), pyrr.Vector3([0.05, 0.0, 0.0]))

    def move_BB(self):
        self.bounding_box.object.transformation.translation.x = self.object.transformation.translation.x
        self.bounding_box.object.transformation.translation.z = self.object.transformation.translation.z