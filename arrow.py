from Entity import Entity, BoundingBox
import pyrr

class Arrow(Entity) :
    def mov_arrow(self) :
        self.object.transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.object.transformation.rotation_euler), pyrr.Vector3([0.4, 0.0, 0.0]))
        self.move_BB()

    # def move_BB(self):
    #     self.bounding_box.object.transformation.translation = self.object.transformation.translation
    
    def destroy(self):
        self.viewer.objs_bounding_boxes.remove(self.bounding_box)
        self.viewer.objs_projectile.remove(self)
        self.viewer.objs.remove(self)