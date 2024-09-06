
from OpenGL.GL import *

class Kelp:
    
    def __init__(self,pos,model,rotate_ver,rotate_hor):
        self.position=pos
        self.model=model
        self.rotate_vert=rotate_ver
        self.rotate_hor=rotate_hor
        
    def draw(self):
        glPushMatrix()  
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(self.rotate_vert,0.0,0.0,1.0)
        glRotatef(self.rotate_hor,0.0,1.0,0.0)
        glScale(30.0,30.0,30.0)
        glCallList(self.model)
        glPopMatrix()
        
        