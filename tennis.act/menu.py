# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
class cursor():
    seleccionado=1
    mantiene_pulsado=0
    yy=0
    def __init__(self,x,y):
        self.image = pygame.image.load('imagen/bola.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.yy=self.rect.y=y
        
    def actualizar(self,cancha):
        #print k
        k=pygame.key.get_pressed()
        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
        if self.seleccionado<=1:
            self.seleccionado=1
        if self.seleccionado>=3:
            self.seleccionado=3
        self.rect[1]=self.yy+(25*self.seleccionado)
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]
        cancha.display.blit(self.image, self.rect)
        return (self.seleccionado)


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

