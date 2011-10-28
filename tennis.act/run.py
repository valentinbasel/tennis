
# -*- coding: utf-8 -*-
"""Skeleton project file mainloop for new OLPCGames users"""
import olpcgames, logging #pygame 
from olpcgames import pausescreen
import os
import sys
from pygame.locals import *

sys.path.insert(0, "lib")
import pygame
import pygame.camera
import random

from menu import *
pygame.init()
pygame.camera.init()
FONDO=(198,233,185)
LINEA=(255,255,255)
log = logging.getLogger( 'icaro run' )
log.setLevel( logging.DEBUG )
size = width, height = 840, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
class reloj(pygame.sprite.Sprite):
    def __init__(self):
        self.unidad=1
        self.tiempo=str(abs(pygame.time.get_ticks()/1000))

    def update(self):
        text.render(self.tiempo, (0,0,255), (640, 40))        
        self.tiempo=str(abs(pygame.time.get_ticks()/1000))
class Text:
    def __init__(self, FontName = None, FontSize = 30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
 
    def render(self,  text, color, pos):
        #text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            cancha.display.blit(self.font.render(i, 1, color), (x, y))
            y += self.size 
class fondo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        size = width, height = 840, 480        
        self.display = pygame.display.set_mode(size)
        self.largo,self.alto=self.display.get_size() 
    def lineas(self):
        pygame.draw.line(cancha.display,LINEA,(20,40),(600,40),3)
        pygame.draw.line(cancha.display,LINEA,(20,240),(600,240),3)
        pygame.draw.line(cancha.display,LINEA,(20,440),(600,440),3)
        pygame.draw.line(cancha.display,LINEA,(20,40),(20,440),3)
        pygame.draw.line(cancha.display,LINEA,(600,40),(600,440),3) 
        #marcador
        pygame.draw.line(cancha.display,LINEA,(630,90),(690,90),3)
        pygame.draw.line(cancha.display,LINEA,(630,125),(690,125),3)
        pygame.draw.line(cancha.display,LINEA,(630,90),(630,125),3)
        pygame.draw.line(cancha.display,LINEA,(690,90),(690,125),3)
class Capture(object):
    ccolor=(0,0,0,0)
    def __init__(self):
        self.size = (800, 600 )
        self.display = pygame.display.set_mode(self.size, 0)
        self.clist = pygame.camera.list_cameras()
        self.cam = pygame.camera.Camera(self.clist[0], self.size,'RGB')
        self.cam.start()
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)
        self.thresholded = pygame.surface.Surface(self.size, 0, self.display)

    def get(self):
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)
            self.snapshot = pygame.transform.flip(self.snapshot,True,False)
        mask = pygame.mask.from_threshold(self.snapshot, self.ccolor, (30,30,30))

        connected = mask.connected_component()
        if mask.count() > 100:
            coord = mask.centroid()
            persona.posicion(coord[0],coord[1])
            
        else:
             coord = (0,0)
        #pygame.display.flip()
        return coord

    def calibrate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.snapshot = pygame.transform.flip(self.cam.get_image(),True,False)
        self.display.blit(self.snapshot, (0,0))
        self.crect = pygame.draw.rect(self.display, (255, 0, 0), (mouse_x , mouse_y  ,10, 10), 4)
        self.ccolor = pygame.transform.average_color(self.snapshot, self.crect)
        self.display.fill(self.ccolor, (0,0,50,50))

        pygame.display.flip()
    def mostrar(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.snapshot = pygame.transform.flip(self.cam.get_image(self.snapshot),True,False)
        self.display.blit(self.snapshot, (0,0))
        self.crect = pygame.draw.rect(cancha.display, (0,0, 0, 255), (305 , 5  ,70, 70), 4)
        self.ccolor = pygame.transform.average_color(self.snapshot, self.crect)
        #self.display.fill(self.ccolor, (100,0,50,50))
        pygame.display.flip()
    def umbral(self):
        cancha.display.fill(self.ccolor, (640,200,50,50))        
class personaje(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagen/azul_de.png")
        self.rect = self.imagen.get_rect()
        self.rect[0]=100
        self.rect[1]=500
    def update(self):
        
        cancha.display.blit(self.imagen,(self.rect))        
        if (self.rect[0]<=320):
            self.imagen = pygame.image.load("imagen/azul_iz.png")
            velocidad=-12
            if (self.rect[1]>300):
                velocidad=-6
        if (self.rect[0]>=320):
            self.imagen = pygame.image.load("imagen/azul_de.png")
            velocidad=12
            if (self.rect[1]<300):
                velocidad=6
        if (self.rect.colliderect(pelota.rect)):
            pelota.velocidad_y=-6
            pelota.velocidad_x=velocidad
    def posicion(self,x,y):
        self.rect[0]=x
        self.rect[1]=y
        if (self.rect[1]<=240):
            self.rect[1]=239
class personaje_2(pygame.sprite.Sprite):
    azar=0
    azar2=0
    x=0
    y=0
    contador=0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagen/rojo_de.png")
        self.rect = self.imagen.get_rect()
        self.rect[0]=100
        self.rect[1]=50
        self.y=self.rect[1]
    def update(self):
        #self.rect[1]=self.y
        cancha.display.blit(self.imagen,(self.rect))
        #
        
        if (self.rect[0]<=320):
            self.imagen = pygame.image.load("imagen/rojo_iz.png")
            velocidad=-12
            if (self.rect[1]>300):
                velocidad=-6
        if (self.rect[0]>=320):
            self.imagen = pygame.image.load("imagen/rojo_de.png")
            velocidad=12
            if (self.rect[1]<300):
                velocidad=6
        if (self.rect.colliderect(pelota.rect)):
            pelota.velocidad_y=6
            pelota.velocidad_x=velocidad
        self.inteligencia()
    def inteligencia(self):
        #self.rect[0]=self.rect[0]-pelota.velocidad_x
        if self.rect[0]<pelota.rect[0]:
            self.rect[0]=self.rect[0]+6
        if self.rect[0]>pelota.rect[0]:
            self.rect[0]=self.rect[0]-6
        if (self.contador==50):
            self.azar=random.randint(1, 200)
            self.contador=0
        else:
            self.contador=self.contador+1
        if(self.azar<=110):
            avance=1
        else: 
            avance =-1
        self.rect[1]+=avance
        if self.rect[1]>=400:
            avance=avance*-1
        if self.rect[1]<=20:
            avance=avance*-1
#        if pelota.velocidad_y<0 and pelota.rect[1]>100:
#                           
#            if (self.contador==50):
#                self.azar=random.randint(1, 200)
#                self.contador=0
#            else:
#                self.contador=self.contador+1
#            if(self.azar<=110):
#                self.rect[1]=self.rect[1]-1  
#                if (self.rect[1]<=20):
#                    self.rect[1]=29
#                    
#            if(self.azar>=150):
#                self.rect[1]=self.rect[1]+1
#                if (self.rect[1]>=210):
#                    self.rect[1]=109

class cajas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagen/box1.png")
        self.rect = self.imagen.get_rect()
        self.x=self.rect[0]=300
        self.y=self.rect[1]=0
   
    def update(self):
        cancha.display.blit(self.imagen,(self.rect))
        text.render("ponga el objecto ", (0,0,255), (300, 120))
        text.render("del color deseado", (0,0,255), (300, 140))
        text.render("en este recuadro", (0,0,255), (300, 160))
class bola(pygame.sprite.Sprite):
    marcador="0 - 0"
    x=0
    y=0
    velocidad_x=6
    velocidad_y=9
    valor=0
    valor2=0
    def __init__(self,xx,yy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagen/bola.png")
        self.rect = self.imagen.get_rect()
        self.x=self.rect[0]=xx
        self.y=self.rect[1]=yy
   
    def update(self):
        self.x=self.x+self.velocidad_x*-1
        self.y=self.y+self.velocidad_y
        self.rect[0]=self.x
        self.rect[1]=self.y


        if (self.rect[0]<=0):
            self.velocidad_x=self.velocidad_x*-1
        if (self.rect[0]>=600):
            self.velocidad_x=self.velocidad_x*-1
        if (self.rect[1]>=460):
            self.x=150
            self.y=100
            persona2.rect[0]=150
            persona2.rect[1]=40
            self.valor=self.valor+1
            self.marcador= str(self.valor) +  " - " + str(self.valor2)
            #self.velocidad_y=self.velocidad_y*-1
        if (self.rect[1]<=40):
            self.x=150
            self.y=100
            self.velocidad_y=9
            persona2.rect[0]=150
            persona2.rect[1]=40
            self.valor2=self.valor2+1
            self.marcador= str(self.valor) +  " - " + str(self.valor2)
        cancha.display.blit(self.imagen,(self.rect))

cronometro=reloj()                  
c = Capture()
c.calibrate()
persona=personaje()
persona2=personaje_2()
pelota=bola(100,150)
clock = pygame.time.Clock()
cancha=fondo()
text = Text()
caja1=cajas()
quit = False
cur=cursor(100,15)
men=menu(140,40)
def menu_principal():
    seleccion=True
    while seleccion==True:
        for event in pygame.event.get():
           pass 

        cancha.display.fill(FONDO)
        valor=cur.actualizar(cancha)
        men.actualizar(text)
        if pygame.key.get_pressed()[pygame.K_RETURN]:

            if valor==1:
                juego()
            if valor==2:
                calibracion()
            if valor==3:
                sys.exit()
        pygame.display.update()


def  calibracion():
    calibrado=False

    while calibrado==False:
        clock.tick(40)
        for event in pygame.event.get():    #get user input
            #if event.type == pygame.QUIT:    #if user clicks the close X

            if event.type == MOUSEBUTTONDOWN:
                calibrado = True
                c.calibrate()
        cancha.display.fill(FONDO)
        c.mostrar()
        c.umbral()
        caja1.update()
        pygame.display.update()
        
def juego():


    partido=1
    while partido<=3:
        pelota.valor=0
        pelota.valor2=0
        pelota.marcador="0 - 0"
        cancha.display.fill(FONDO)
        cancha.lineas()
        text.render("set "+str(partido), (0,255,0), (300, 220))
        pygame.display.flip()
        pygame.time.delay(1000)
        ganador=game()
        print partido
        if ganador==1:
            partido +=1
        if partido ==3:
            pelota.valor=0
            pelota.valor2=0
            pelota.marcador="0 - 0"
            cancha.display.fill(FONDO)
            cancha.lineas()
            text.render("perdiste!!!", (255,0,0), (300, 220))
            pygame.display.flip()
            pygame.time.delay(1000)
            return 0
    

        
def game():
    running = True
    while running:
        screen.fill( (0,0,0))
        milliseconds = clock.tick(40) # maximum number of frames per second
        
        # Event-management loop with support for pausing after X seconds (20 here)
        #events = pausescreen.get_events()
        # Now the main event-processing loop
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
        cancha.display.fill(FONDO)
        c.get()
        #c.umbral()
        persona.update()
        persona2.update()
        pelota.update()
        cancha.lineas()
        text.render(pelota.marcador, (0,0,255), (640, 100))
        #cronometro.update()
        if pelota.valor==7:
            return 1
        pygame.display.flip()
def main():
    """The mainloop which is specified in the activity.py file
    
    "main" is the assumed function name
    """
    if olpcgames.ACTIVITY:
        size = olpcgames.ACTIVITY.game_size
    menu_principal()



            

if __name__ == "__main__":
    logging.basicConfig()
    main()
