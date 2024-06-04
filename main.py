import pygame
from pygame.locals import *


from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import math

import sys
sys.path.append('..')
from shark import Shark
from gun import Gun

screen_width = 800
screen_height = 800

FOVY=60.0
ZNEAR=1.0
ZFAR=800.0

EYE_X = 0.0
EYE_Y = 5.0
EYE_Z = 0.0
CENTER_X = 1.0
CENTER_Y = 5.0
CENTER_Z = 0.0
UP_X=0
UP_Y=1
UP_Z=0

X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

dir = [1.0, 0.0, 0.0]
theta = 0
Sharks=[]
Guns=[]
timer = 0
dash=[32,28,23,18,13,8,5,3,2,1]
theta = 0.0
shoot=False
shootTimer=0
sharkMove=False
sharkMoveTimer=50
hitTimer=0

pygame.init()


lastkey = pygame.key.get_pressed()


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_FOG)
    glClearColor(0.05, 0.05, 0.120, 1.0)
    Sharks.append(Shark("bob.obj", swapyz=True))
    Sharks[0].generate()
    Guns.append(Gun("arma.obj", swapyz=False))
    Guns.append(Gun("bala.obj", swapyz=False))
    Guns[0].generate()
    Guns[1].generate()
    if bool(glutSetCursor):
        print("exists")
    
    


def giro():
    global dir
    newdir=[0,0,0]
    angle=math.radians(theta)
    newdir[0]=(math.cos(angle)*dir[0])+(math.sin(angle)*dir[2])
    newdir[2]=(-(math.sin(angle))*dir[0])+(math.cos(angle)*dir[2])
    dir=newdir

def displayShark():
    global hitTimer
    global sharkMove
    Sharks[0].render()
    if sharkMove:
        Sharks[0].move(EYE_X,EYE_Z)
        Sharks[0].arcTanGet(EYE_X,EYE_Z)
        #Sharks[0].colition(EYE_X,EYE_Z)
    if hitTimer==0:
        if Sharks[0].bulletColition(Guns[1].getPos()):
            hitTimer=50
        

def displayGun():
    global EYE_X,EYE_Z, CENTER_X, CENTER_Z, dir
    y=EYE_Z-CENTER_Z
    x=EYE_X-CENTER_X
    result=math.atan2(y,x)
    rotate=-90-math.degrees(result)
    Guns[0].render(rotate, dir,EYE_X, EYE_Z)
    if shoot==False:
        Guns[1].render(rotate, dir,EYE_X, EYE_Z)
    else:
        Guns[1].shootMove()
    
def display():
    global shoot
    color = [0.05, 0.05, 0.120, 1.0]
    global EYE_X,EYE_Y,EYE_Z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    displayShark()
    displayGun()
    glFogf(GL_FOG_END,1000.0)
    glFogf(GL_FOG_DENSITY,0.007)
    glFogfv(GL_FOG_COLOR,color)
    glutWarpPointer(screen_width/2,screen_height/2)
                
    
    
done = False
Init()
while not done:
        keys = pygame.key.get_pressed()
        if lastkey[pygame.K_d] and keys[pygame.K_LSHIFT] and timer==0:
                timer=500
                for i in dash:
                        EYE_X = EYE_X - dir[2]*i
                        EYE_Z = EYE_Z + dir[0]*i
                        CENTER_X = EYE_X + dir[0]*i
                        CENTER_Z = EYE_Z + dir[2]*i
                        glLoadIdentity()   
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                        pygame.time.wait(15)
                        display()
                        pygame.display.flip()
                        
        if lastkey[pygame.K_a] and keys[pygame.K_LSHIFT] and timer==0:
                timer=500
                for i in dash:
                        EYE_X = EYE_X + dir[2]*i
                        EYE_Z = EYE_Z - dir[0]*i
                        CENTER_X = EYE_X + dir[0]*i
                        CENTER_Z = EYE_Z + dir[2]*i
                        glLoadIdentity()   
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                        pygame.time.wait(15)
                        display()
                        pygame.display.flip()
                
            
        if keys[pygame.K_w]:
            EYE_X = EYE_X + dir[0]
            EYE_Z = EYE_Z + dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
        if keys[pygame.K_s]:
            EYE_X = EYE_X - dir[0]
            EYE_Z = EYE_Z - dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
        if keys[pygame.K_d]:
            EYE_X = EYE_X - dir[2]
            EYE_Z = EYE_Z + dir[0]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
        if keys[pygame.K_a]:
            EYE_X = EYE_X + dir[2]
            EYE_Z = EYE_Z - dir[0]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
        if keys[pygame.K_p]:
            print("x= ",EYE_X)
            print("z= ",EYE_Z)
            print("look_x= ",CENTER_X)
            print("look_z= ",CENTER_Z)
            print("direction= ",dir)
        if keys[pygame.K_RIGHT]: 
            theta=-1
            giro()
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
        if keys[pygame.K_LEFT]: 
            theta=1
            giro()
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                
        if keys[pygame.K_SPACE]:
            if shoot==False:
                Guns[1].shoot(EYE_X,EYE_Z,dir)
                shoot=True
                shootTimer=150
        if keys[pygame.K_p]:
            if sharkMove and sharkMoveTimer==0:
                sharkMove=False
                sharkMoveTimer=50
            elif sharkMove==False and sharkMoveTimer==0:
                sharkMove=True
                sharkMoveTimer=50
        
        if shoot==True:
            shootTimer=shootTimer-1
        if shootTimer<1:
            shoot=False 
        if sharkMoveTimer>0:
            sharkMoveTimer=sharkMoveTimer-1 
            
        if timer>0:
            timer=timer-1
            
        if hitTimer>0:
            hitTimer=hitTimer-1
                
                
        lastkey=keys

           
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                                done = True
                elif event.type == MOUSEMOTION :
                    x, y=event.rel
                    if x>0:
                        theta=-1
                        giro()
                        CENTER_X = EYE_X + dir[0]
                        CENTER_Z = EYE_Z + dir[2]
                        glLoadIdentity()
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                    elif x<0:
                        theta=1
                        giro()
                        CENTER_X = EYE_X + dir[0]
                        CENTER_Z = EYE_Z + dir[2]
                        glLoadIdentity()
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

        display()

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()