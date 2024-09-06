import os
import pygame
from OpenGL.GL import *
import math

class Gun:
    generate_on_init = True
    @classmethod
    def loadTexture(cls, imagefile):
        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = cls.loadTexture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        dirname = os.path.dirname(filename)
        self.position=[3,4.2,1.2]
        self.rotate=90.0
        self.dir=[-1,0,0]

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        if self.generate_on_init:
            self.generate()

    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def render(self,degree,dir, player_x, player_z):
        glPushMatrix()
        self.position[0]=player_x+dir[0]*3-dir[2]*1.2
        self.position[2]=player_z+dir[2]*3+dir[0]*1.2
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(degree, 0.0, 1.0, 0.0)
        self.rotate=degree
        glScale(0.3,0.3,0.3)
        glCallList(self.gl_list)
        glPopMatrix()
        
    def shoot(self,player_x, player_z, dir):
        glPushMatrix()
        glTranslatef(player_x+dir[0], self.position[1], player_z+dir[2])
        glRotatef(self.rotate, 0.0, 1.0, 0.0)
        glScale(0.3,0.3,0.3)
        glCallList(self.gl_list)
        self.dir=dir
        self.position[0]=player_x+dir[0]
        self.position[2]=player_z+dir[2]
        glPopMatrix()
    def shootMove(self):
        glPushMatrix()
        glTranslatef(self.position[0]+self.dir[0]*5, self.position[1]-3, self.position[2]+self.dir[2]*5)
        glScale(1.5,1.5,1.5)
        glRotatef(self.rotate, 0.0, 1.0, 0.0)
        glCallList(self.gl_list)
        self.position[0]=self.position[0]+self.dir[0]*5
        self.position[2]=self.position[2]+self.dir[2]*5
        glPopMatrix()
        
    def getPos(self):
        pos=[self.position[0],self.position[2]]
        return pos

    def free(self):
        glDeleteLists([self.gl_list])