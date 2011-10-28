import pygame
from pygame.locals import *
class cursor():
    seleccionado=1
    def __init__(self,x,y):
        self.image = pygame.image.load('imagen/bola.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def actualizar(self,cancha):
        k = pygame.key.get_pressed()
        if k[K_UP]:
            self.seleccionado -= 1
        elif k[K_DOWN]:
            self.seleccionado += 1
        if self.seleccionado<1:
            self.seleccionado=1
        if self.seleccionado>=2:
            self.seleccionado=2
        self.rect.y=self.rect.y+20*self.seleccionado
        cancha.display.blit(self.image, self.rect)

class menu():
    x=0
    y=0
    def __init__(self,x,y):
        self.x=x
        self.y=y
        pass
    def actualizar(self,text):
        text.render("inicio", (0,0,255), (self.x, self.y))
        text.render("calibrar", (0,0,255), (self.x, self.y+25))
        text.render("salir", (0,0,255), (self.x, self.y+50))

