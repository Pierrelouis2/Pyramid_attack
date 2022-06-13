from Entity import Entity, BoundingBox
import pyrr, math 

class Arrow(Entity) :
    def mov_arrow(self) :
        self.speed = self.viewer.objs_humain.v_proj
        self.object.transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.object.transformation.rotation_euler), pyrr.Vector3([0.0, 0.0, self.speed]))
        self.bounding_box.move_BB()
        out_x = -25 <self.object.transformation.translation.x < 25
        out_z = -25 <self.object.transformation.translation.z < 25
        if not out_x or not out_z :
            self.destroy()
    
    def destroy(self):
        self.viewer.objs_bounding_boxes.remove(self.bounding_box)
        self.viewer.objs_projectile.remove(self)
        self.viewer.objs.remove(self)