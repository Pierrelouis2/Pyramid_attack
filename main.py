from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import random as rand
import Pyramid
from Entity import Entity, BoundingBox
import Humain
import math
import glfw
import pyrr

def main():
    viewer = ViewerGL()

    # Cam
    # cam = Camera(viewer,mouseX_middle = glfw.get_window_size(viewer.window)[0],mouseY_middle = glfw.get_window_size(viewer.window)[1])
    cam = Camera(viewer)
    viewer.set_camera(cam)
    viewer.cam.transformation.translation.y = 0.75
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    viewer.program3d_id = glutils.create_program_from_file('vert/shader.vert', 'frag/shader.frag')
    viewer.programGUI_id = glutils.create_program_from_file('vert/gui.vert', 'frag/gui.frag')

    dic_text = {}
    dic_obj = {}
    dic_vao = {}

    #------------------------ Chargements des textures + objs ----------------------------

    dic_text["pyramid"] = glutils.load_texture("Textures/architecture.jpg")
    dic_text["sol"] = glutils.load_texture("Textures/TextureSand.jpeg")
    dic_text["humain"] = glutils.load_texture("Textures/multicolor.png")
    dic_text["cube"] = glutils.load_texture("Textures/cube.png")
    
    dic_obj["pyramid"] = Mesh.load_obj("Textures/pyramid.obj")
    dic_obj["pyramid"].normalize()
    dic_obj["pyramid"].apply_matrix(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25, 1]))
    dic_obj["humain"] = Mesh.load_obj("Textures/homme.obj")
    dic_obj["humain"].normalize()
    dic_obj["humain"].apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
    #bounding_box
    dic_obj["cube_pyramid"] = Mesh.load_obj("Textures/cube.obj")
    dic_obj["cube_pyramid"].normalize()
    dic_obj["cube_pyramid"].apply_matrix(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25, 1]))
    dic_obj["cube_humain"] = Mesh.load_obj("Textures/cube.obj")
    dic_obj["cube_humain"].normalize()
    dic_obj["cube_humain"].apply_matrix(pyrr.matrix44.create_from_scale([0.2, 0.5, 0.2, 1]))
    dic_obj["cube_arrow"] = Mesh.load_obj("Textures/cube.obj")
    dic_obj["cube_arrow"].normalize()
    dic_obj["cube_arrow"].apply_matrix(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25, 1]))

    viewer.dic_obj = dic_obj
    viewer.dic_text = dic_text

    #chargement sol
    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1],[p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    dic_obj["sol"] = m

    dic_vao["humain"] = dic_obj["humain"].load_to_gpu()
    dic_vao["pyramid"] = dic_obj["pyramid"].load_to_gpu()
    dic_vao["sol"] = dic_obj["sol"].load_to_gpu()
    dic_vao["cube_pyramid"] = dic_obj["cube_pyramid"].load_to_gpu()
    dic_vao["cube_humain"] = dic_obj["cube_humain"].load_to_gpu()
    dic_vao["cube_arrow"] = dic_obj["cube_arrow"].load_to_gpu()

    viewer.dic_vao = dic_vao

    #------------------------Fin Chargements des textures + objs ---------------------------

    # humain
    humain = Humain.Humain(vie=1, coord=[0, 0, 0], rot=[0, 0, 0], obj=dic_obj["humain"],
                           texture=dic_text["humain"], viewer=viewer, name="humain",vao_obj=dic_vao["humain"])
    humain.create()
    humain.bounding_box = BoundingBox(humain)
    humain.bounding_box.create()

    # Spawn Pyramide
    nbr_pyramide = 10
    lst_pyramide = []
    rayon = 10
    for i in range(nbr_pyramide):
        teta = rand.randint(0, 10)
        pyramide = Pyramid.Pyramid(vie=1, coord=[rayon * math.cos(teta), 0, rayon * math.sin(teta)], rot=[0, 0, 0], obj=dic_obj["pyramid"],
                                   texture=dic_text["pyramid"], viewer=viewer, name="pyramid",vao_obj = dic_vao["pyramid"])
        lst_pyramide.append(pyramide)
        pyramide.create()
        pyramide.create_BB()

    # Sol
    sol  = Entity(vie=1, coord=[0,0,0], rot=[0,0,0], obj=dic_obj["sol"],texture=dic_text["sol"],viewer=viewer,vao_obj = dic_vao["sol"],name="sol")
    sol.create()

    # Text Pause
    vao_obj = Text.initalize_geometry()
    texture = glutils.load_texture('Textures/fontB2.png')
    text_pause = Text('Pause', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao_obj, 2, viewer.programGUI_id, texture)
    viewer.text_pause = text_pause


    viewer.run()


if __name__ == '__main__':
    main()
