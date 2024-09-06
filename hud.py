from OpenGL.GL import *



class Health:
    
    def __init__(self,offset):
        
        self.Position=[0,5.5,0]
        self.offset=offset
        
    def draw(self,player,dir,degree):
        self.Position[0]=player[0]+dir[0]*1.1+dir[2]*self.offset
        self.Position[2]=player[1]+dir[2]*1.1-dir[0]*self.offset
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(90,1.0,0,0)
        glRotatef(degree,0.0,0,-1.0)
        glRotatef(180, 0.0, 1.0, 0.0)
        glScaled(0.1,0.1,0.1)
        glEnable(GL_COLOR_MATERIAL)
        glColor(0.239,0.049,0.049)
        glBegin(GL_POLYGON)
        glVertex3f(0.0, 0.0, 0.3)
        glVertex3f(0.2, 0.0, 0.5)
        glVertex3f(0.4, 0.0, 0.5)
        glVertex3f(0.5, 0.0, 0.4)
        glVertex3f(0.5, 0.0, 0.1)
        glVertex3f(0.0, 0.0, -0.5)
        glVertex3f(-0.5, 0.0, 0.1)
        glVertex3f(-0.5, 0.0, 0.4)
        glVertex3f(-0.4, 0.0, 0.5)
        glVertex3f(-0.2, 0.0, 0.5)
        glEnd()
        glDisable(GL_COLOR_MATERIAL)
        glPopMatrix()
        
class Dash:
    def __init__(self):
        
        self.Position=[0,5.494,0]
        
    def draw(self,player,dir,degree,dash):
        self.Position[0]=player[0]+dir[0]*1.1001-dir[2]*0.75
        self.Position[2]=player[1]+dir[2]*1.1001+dir[0]*0.75
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(90,1.0,0,0)
        glRotatef(degree,0.0,0,-1.0)
        glRotatef(-90, 0.0, 1.0, 0.0)
        glScaled(0.5,0.5,0.5)
        glEnable(GL_COLOR_MATERIAL)
        glColor(0,0,0)
        glBegin(GL_QUADS)
        glVertex3f(0.1, 0.0, 0.5)
        glVertex3f(-0.1, 0.0, 0.5)
        glVertex3f(-0.1, 0.0, -0.5)
        glVertex3f(0.1, 0.0, -0.5)
        glEnd()
        glPopMatrix()
        self.Position[0]=player[0]+dir[0]*1.1-dir[2]*0.75
        self.Position[2]=player[1]+dir[2]*1.1+dir[0]*0.75
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(90,1.0,0,0)
        glRotatef(degree,0.0,0,-1.0)
        glRotatef(-90, 0.0, 1.0, 0.0)
        glScaled(0.5,0.5,0.5)
        glEnable(GL_COLOR_MATERIAL)
        glColor(1,1,1)
        glBegin(GL_QUADS)
        glVertex3f(0.1, 0.0, 0.5-(dash*0.005))
        glVertex3f(-0.1, 0.0, 0.5-(dash*0.005))
        glVertex3f(-0.1, 0.0, -0.5)
        glVertex3f(0.1, 0.0, -0.5)
        glEnd()
        glDisable(GL_COLOR_MATERIAL)
        glPopMatrix()

class Radar:
    def __init__(self):
        self.Position=[0,4.6,0]
        
    def draw(self,player,dir,degree, sharkdegree):
        self.Position[0]=player[0]+dir[0]*1.1+dir[2]*0.87
        self.Position[2]=player[1]+dir[2]*1.1-dir[0]*0.87
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(90,1.0,0,0)
        glRotatef(degree,0.0,0,-1.0)
        glRotatef(degree-sharkdegree-180,0.0,1.0,0.0)
        glScaled(0.25,0.25,0.25)
        glEnable(GL_COLOR_MATERIAL)
        glColor(0.3,1,1)
        glBegin(GL_POLYGON)
        glVertex3f(0.0, 0.0, 0.5)
        glVertex3f(0.2, 0.0, 0.2)
        glVertex3f(0.1, 0.0, 0.2)
        glVertex3f(0.0, 0.0, -0.5)
        glVertex3f(-0.1, 0.0, 0.2)
        glVertex3f(-0.2, 0.0, 0.2)
        glEnd()
        glDisable(GL_COLOR_MATERIAL)
        glPopMatrix()