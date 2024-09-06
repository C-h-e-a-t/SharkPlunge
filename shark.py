
import os
import pygame
from OpenGL.GL import *
import math
import random

class Shark:
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
        self.position=[800,0,0]
        self.rotate=90.0
        self.dir=[-1,0,0]
        self.multiplier=1
        self.dir_predictor=[0,0,0]

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
        
    def arcTanGet(self,player_x,player_y):
        y=self.position[2]-player_y
        x=self.position[0]-player_x
        result=math.atan2(y,x)
        self.rotate=90-math.degrees(result)
        
    def move(self,player_x,player_y):
        y=self.position[2]-player_y
        x=self.position[0]-player_x
        result=math.atan2(y,x)
        check=90-math.degrees(result)
        if check!=self.rotate:
            newdir=[0,0,0]
            angle=math.radians(check-self.rotate)
            newdir[0]=(math.cos(angle)*self.dir[0])+(math.sin(angle)*self.dir[2])
            newdir[2]=(-(math.sin(angle))*self.dir[0])+(math.cos(angle)*self.dir[2])
            self.dir=newdir
        self.position[0]=self.position[0]+self.dir[0]*self.multiplier
        self.position[2]=self.position[2]+self.dir[2]*self.multiplier
        
    def rush(self):
        self.position[0]=self.position[0]+self.dir[0]*3*self.multiplier
        self.position[2]=self.position[2]+self.dir[2]*3*self.multiplier
        
    def prey(self,player):
        if math.dist(player,[self.position[0],self.position[2]])>850:
            return True
        
    def pounce(self,player):
        if math.dist(player,[self.position[0],self.position[2]])<300:
            return True
        
    def getPos(self):
        value=[self.position[0],self.position[2]]
        return value
    
    def die(self):
        glPushMatrix() 
        self.position[1]=self.position[1]-1 
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(self.rotate, 0.0, 0.0, 1.0)
        glRotatef(90, 0.0, 1.0, 0.0)
        glScale(10.0,10.0,10.0)
        glCallList(self.gl_list)
        glPopMatrix()
    
    def colition(self,player_x,player_y):
        if abs(player_x-self.position[0])<20 and abs(player_y-self.position[2])<20:
            return True
        

    def render(self):
        
        glPushMatrix()  
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(self.rotate, 0.0, 0.0, 1.0)
        glScale(10.0,10.0,10.0)
        glCallList(self.gl_list)
        glPopMatrix()
    
    def bulletColition(self, bullet_pos):
        place=[self.position[0]-self.dir[0]*7,self.position[2]-self.dir[2]*7]
        for i in range(8):
            if math.dist(bullet_pos,place)<10:
                return True
            place=[place[0]-self.dir[0]*15,place[1]-self.dir[2]*15]
            
    def revive(self, round):
        angle=math.radians(random.randrange(-180,180))
        self.position=[1,0,0]
        new_x=(math.cos(angle)*self.position[0])+(math.sin(angle)*self.position[2])
        new_y=(-(math.sin(angle))*self.position[0])+(math.cos(angle)*self.position[2])
        self.position[0]=new_x*855
        self.position[2]=new_y*855
        self.multiplier=round/2+1
    
    def addToMultiplier(self):
        self.multiplier=self.multiplier+0.25
        
    def newAttackPoint(self):
        angle=math.radians(random.randrange(-180,180))
        self.position=[1,0,0]
        new_x=(math.cos(angle)*self.position[0])+(math.sin(angle)*self.position[2])
        new_y=(-(math.sin(angle))*self.position[0])+(math.cos(angle)*self.position[2])
        self.position[0]=new_x*855
        self.position[2]=new_y*855
    
    def moveDown(self):
        self.position[0]=self.position[0]+self.dir[0]*3*self.multiplier
        self.position[2]=self.position[2]+self.dir[2]*3*self.multiplier
        self.position[1]=self.position[1]-4*self.multiplier
        glPushMatrix()  
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(self.rotate, 0.0, 0.0, 1.0)
        glRotatef(30, -1.0, 0.0, 0.0)
        glScale(10.0,10.0,10.0)
        glCallList(self.gl_list)
        glPopMatrix()
        

    def free(self):
        glDeleteLists([self.gl_list])
        
    

