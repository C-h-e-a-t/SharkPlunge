import pygame
from pygame.locals import *
import random



from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

import sys
sys.path.append('..')
from shark import Shark
from gun import Gun
from hud import Health
from hud import Radar
from hud import Dash
from kelp import Kelp
from texture import Model

pygame.init()

screen_disp = pygame.display.Info()
screen_width = screen_disp.current_w/2
screen_height = screen_disp.current_h/2

FOVY=60.0
ZNEAR=1.0
ZFAR=1000.0

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
hitTimer=0
hud_player=[]
nohit=True
sharkPrey=True
sharkPounce=False
sharkDisappear=False
sharkDisappearTimer=0
sharkDeathTimer=0
sharkAlive=True
sharkRound=1
menu_image="resources/menu.bmp"
tutorial_image="resources/tutorial.bmp"
textures=[]
Kelps=[]
player_health=3
damage_timer=0
radarPing=0
radarOn=False
radarPingTimer=7
player_alive=True
deathTimer=0



lastkey = pygame.key.get_pressed()

def initiateKelp():
    kelpModel=Model("kelp.obj",swapyz=True)
    theta=0
    dir=[1,0,0]
    for i in range(36):
        newdir=[0,0,0]
        angle=math.radians(theta)
        newdir[0]=(math.cos(angle)*dir[0])+(math.sin(angle)*dir[2])
        newdir[2]=(-(math.sin(angle))*dir[0])+(math.cos(angle)*dir[2])
        theta=theta+10
        Kelps.append(Kelp([newdir[0]*750,-500,newdir[2]*750],kelpModel.getModel(),random.randrange(-180,180),random.randrange(-5,5)))
        
def drawKelp():
    for i in range(36):
        Kelps[i].draw()
        
        
    
def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    

def Init():
    global screen, radar, player_dash
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
    glFogf(GL_FOG_DENSITY,0)
    glClearColor(0.05, 0.05, 0.120, 1.0)
    Sharks.append(Shark("bob.obj", swapyz=True))
    Sharks[0].generate()
    Guns.append(Gun("arma.obj", swapyz=False))
    Guns.append(Gun("bala.obj", swapyz=False))
    Guns[0].generate()
    Guns[1].generate()
    Texturas(menu_image)
    Texturas(tutorial_image)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    offset=0.95
    for i in range(3):
         hud_player.append(Health(offset))
         offset=offset-0.12
    
    initiateKelp()
    radar=Radar()
    player_dash=Dash()
    
def giro():
    global dir
    newdir=[0,0,0]
    angle=math.radians(theta)
    newdir[0]=(math.cos(angle)*dir[0])+(math.sin(angle)*dir[2])
    newdir[2]=(-(math.sin(angle))*dir[0])+(math.cos(angle)*dir[2])
    dir=newdir
    
def displayHealth():
    y=EYE_Z-CENTER_Z
    x=EYE_X-CENTER_X
    result=math.atan2(y,x)
    degree=-90-math.degrees(result)
    for i in range(player_health):
        hud_player[i].draw([EYE_X,EYE_Z],dir,degree)
        
def displayDash():
    y=EYE_Z-CENTER_Z
    x=EYE_X-CENTER_X
    result=math.atan2(y,x)
    degree=-90-math.degrees(result)
    for i in range(player_health):
        player_dash.draw([EYE_X,EYE_Z],dir,degree,timer)
        

        
def displayRadar():
    if radarOn:
        y=EYE_Z-CENTER_Z
        x=EYE_X-CENTER_X
        result=math.atan2(y,x)
        degree=-90-math.degrees(result)
        shark_x=EYE_X-Sharks[0].getPos()[0]
        shark_y=EYE_Z-Sharks[0].getPos()[1]
        shark_result=math.atan2(shark_y,shark_x)
        shark_degree=-90-math.degrees(shark_result)
        radar.draw([EYE_X,EYE_Z],dir,degree,shark_degree)
        
        

def displayShark():
    global hitTimer, shoot, player_health, damage_timer
    global sharkDeathTimer, sharkAlive, sharkDisappear,sharkDisappearTimer
    if sharkDisappear:
        Sharks[0].moveDown()
    elif sharkAlive==True and radarPing==0:
        Sharks[0].render()
        if sharkPrey:
            Sharks[0].move(EYE_X,EYE_Z)
            Sharks[0].arcTanGet(EYE_X,EYE_Z)
        if sharkPounce:
            Sharks[0].rush()
            if Sharks[0].colition(EYE_X,EYE_Z) and damage_timer==0:
                player_health=player_health-1
                damage_timer=150
                sharkDisappear=True
                sharkDisappearTimer=100
    elif sharkAlive==False:
        Sharks[0].die()
    if hitTimer==0 and shoot==True and damage_timer==0:
        if Sharks[0].bulletColition(Guns[1].getPos()):
            hitTimer=50
            sharkAlive=False
            sharkDeathTimer=300
        

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
    global screen_height, screen_width,screen
    color = [0.05, 0.05, 0.120, 1.0]
    global EYE_X,EYE_Y,EYE_Z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glFogf(GL_FOG_END,1000.0)
    glFogf(GL_FOG_DENSITY,0.008)
    glFogfv(GL_FOG_COLOR,color)
    displayGun()
    displayShark()
    glFogf(GL_FOG_DENSITY,0.002)
    drawKelp()
    pygame.mouse.set_pos = (screen_height/2, screen_width/2)
    displayRadar()
    displayHealth()
    displayDash()
    
def displayMenu():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslatef(460,5,0)
    glRotatef(-90,0.0,0,1)
    glRotatef(180,1.0,0,0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-screen_height/2, 0,  -screen_width/2)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-screen_height/2, 0, screen_width/2)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(screen_height/2, 0, screen_width/2)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(screen_height/2, 0,  -screen_width/2)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    
def displayTutorial():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslatef(460,5,0)
    glRotatef(-90,0.0,0,1)
    glRotatef(180,1.0,0,0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-screen_height/2, 0,  -screen_width/2)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-screen_height/2, 0, screen_width/2)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(screen_height/2, 0, screen_width/2)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(screen_height/2, 0,  -screen_width/2)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    
    
done = False
menu=True
tutorial=False
Init()
while not done:
    
        if menu==False:
            if player_alive:
                keys = pygame.key.get_pressed()
                state = pygame.mouse.get_pressed()
                if lastkey[pygame.K_d] and keys[pygame.K_LSHIFT] and timer==0:
                        timer=200
                        for i in dash:
                            if math.dist([0,0],[EYE_X - dir[2]*i,EYE_Z + dir[0]*i])<600:
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
                        timer=200
                        for i in dash:
                            if math.dist([0,0],[EYE_X + dir[2]*i,EYE_Z - dir[0]*i])<600:
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
                    if math.dist([0,0],[EYE_X + dir[0],EYE_Z + dir[2]])<600:
                        EYE_X = EYE_X + dir[0]
                        EYE_Z = EYE_Z + dir[2]
                        CENTER_X = EYE_X + dir[0]
                        CENTER_Z = EYE_Z + dir[2]
                        glLoadIdentity()
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                if keys[pygame.K_s]:
                    if math.dist([0,0],[EYE_X - dir[0],EYE_Z + EYE_Z - dir[2]])<600:
                        EYE_X = EYE_X - dir[0]
                        EYE_Z = EYE_Z - dir[2]
                        CENTER_X = EYE_X + dir[0]
                        CENTER_Z = EYE_Z + dir[2]
                        glLoadIdentity()
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                if keys[pygame.K_d]:
                    if math.dist([0,0],[EYE_X - dir[2],EYE_Z + dir[0]])<600:
                        EYE_X = EYE_X - dir[2]
                        EYE_Z = EYE_Z + dir[0]
                        CENTER_X = EYE_X + dir[0]
                        CENTER_Z = EYE_Z + dir[2]
                        glLoadIdentity()
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                if keys[pygame.K_a]:
                    if math.dist([0,0],[EYE_X + dir[2],EYE_Z - dir[0]])<600:
                        EYE_X = EYE_X + dir[2]
                        EYE_Z = EYE_Z - dir[0]
                        CENTER_X = EYE_X + dir[0]
                        CENTER_Z = EYE_Z + dir[2]
                        glLoadIdentity()
                        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

                if state[0]:
                    if shoot==False:
                        Guns[1].shoot(EYE_X,EYE_Z,dir)
                        shoot=True
                        shootTimer=150

                if shoot==True:
                    shootTimer=shootTimer-1
                if shootTimer<1:
                    shoot=False 

                if timer>0:
                    timer=timer-1

                if hitTimer>0:
                    hitTimer=hitTimer-1
                if Sharks[0].prey([EYE_X,EYE_Z]) and sharkPrey==False:
                    sharkPrey=True
                    sharkPounce=False
                    Sharks[0].addToMultiplier()
                if Sharks[0].pounce([EYE_X,EYE_Z]) and sharkPounce==False:
                    sharkPrey=False
                    sharkPounce=True
                if damage_timer>0:
                    damage_timer=damage_timer-1

                if sharkDeathTimer>0:
                    sharkDeathTimer=sharkDeathTimer-1
                if sharkAlive==False and sharkDeathTimer==0:
                    sharkRound=sharkRound+1
                    Sharks[0].revive(sharkRound)
                    sharkPrey=True
                    sharkPounce=False
                    sharkAlive=True
                    radarPing=35
                    radarOn=True

                if radarPingTimer>0 and radarPing>0:
                    radarPingTimer=radarPingTimer-1
                if radarPingTimer==0 and radarPing>0:
                    radarPingTimer=7
                    if radarOn:
                        radarOn=False
                    else:
                        radarOn=True

                if radarPing>0:
                    radarPing=radarPing-1

                if sharkDisappearTimer>0:
                    sharkDisappearTimer=sharkDisappearTimer-1

                if sharkDisappearTimer==0 and sharkDisappear:
                    sharkDisappear=False
                    Sharks[0].newAttackPoint()
                    sharkPrey=True
                    sharkPounce=False
                    radarPing=35
                    radarOn=True

                if player_health==0:
                    player_alive=False
                    deathTimer=150



                lastkey=keys

            elif player_alive==False and deathTimer>0:
                EYE_Y=EYE_Y-1
                glLoadIdentity()
                gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                deathTimer=deathTimer-1
            
            
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                    menu = True
                                    EYE_X = 0.0
                                    EYE_Y = 5.0
                                    EYE_Z = 0.0
                                    CENTER_X = 1.0
                                    CENTER_Y = 5.0
                                    CENTER_Z = 0.0
                                    UP_X=0
                                    UP_Y=1
                                    UP_Z=0
                                    dir = [1.0, 0.0, 0.0]
                                    theta = 0
                                    Sharks=[]
                                    Guns=[]
                                    timer = 0
                                    dash=[32,28,23,18,13,8,5,3,2,1]
                                    theta = 0.0
                                    shoot=False
                                    shootTimer=0
                                    sharkMoveTimer=50
                                    hitTimer=0
                                    hud_player=[]
                                    nohit=True
                                    sharkPrey=True
                                    sharkPounce=False
                                    sharkDisappear=False
                                    sharkDisappearTimer=0
                                    sharkDeathTimer=0
                                    sharkAlive=True
                                    sharkRound=1
                                    menu_image="resources/menu.bmp"
                                    textures=[]
                                    Kelps=[]
                                    player_health=3
                                    damage_timer=0
                                    radarPing=0
                                    radarOn=False
                                    radarPingTimer=7
                                    player_alive=True
                                    Init()
                                    glDisable(GL_FOG)
                    elif event.type == MOUSEMOTION:
                        x, y=event.rel
                        if x>0:
                            theta=-1
                            giro()
                            CENTER_X = EYE_X + dir[0]*0.09
                            CENTER_Z = EYE_Z + dir[2]*0.09
                            glLoadIdentity()
                            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
                        elif x<0:
                            theta=1
                            giro()
                            CENTER_X = EYE_X + dir[0]*0.09
                            CENTER_Z = EYE_Z + dir[2]*0.09
                            glLoadIdentity()
                            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
            if player_alive==False and deathTimer==0:
                menu = True
                EYE_X = 0.0
                EYE_Y = 5.0
                EYE_Z = 0.0
                CENTER_X = 1.0
                CENTER_Y = 5.0
                CENTER_Z = 0.0
                UP_X=0
                UP_Y=1
                UP_Z=0
                dir = [1.0, 0.0, 0.0]
                theta = 0
                Sharks=[]
                Guns=[]
                timer = 0
                dash=[32,28,23,18,13,8,5,3,2,1]
                theta = 0.0
                shoot=False
                shootTimer=0
                sharkMoveTimer=50
                hitTimer=0
                hud_player=[]
                nohit=True
                sharkPrey=True
                sharkPounce=False
                sharkDisappear=False
                sharkDisappearTimer=0
                sharkDeathTimer=0
                sharkAlive=True
                sharkRound=1
                menu_image="resources/menu.bmp"
                textures=[]
                Kelps=[]
                player_health=3
                damage_timer=0
                radarPing=0
                radarOn=False
                radarPingTimer=7
                player_alive=True
                Init()
                glDisable(GL_FOG)
            display()
        elif menu and tutorial:
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                    tutorial = False
            displayTutorial()
        elif menu:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                menu=False
                glEnable(GL_FOG)
            if keys[pygame.K_t]:
                tutorial=True
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                    done = True
            displayMenu()

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()