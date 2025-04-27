import pygame
from Constantes import *

class Ficha:
    def __init__(self, fila, columna, color):
        self.fila = fila
        self.columna = columna
        self.color = color
        self.radio = TAM_CUADRO // 2 - 5
        self.x = 0
        self.y = 0
        self.actualizar_pos()

    def actualizar_pos(self):
        self.x = self.columna * TAM_CUADRO + TAM_CUADRO // 2
        self.y = self.fila * TAM_CUADRO + TAM_CUADRO // 2

    def dibujar(self, pantalla, color_resaltado=None):
            pygame.draw.circle(pantalla, GRIS, (self.x, self.y), self.radio + 3)
            pygame.draw.circle(pantalla, NEGRO, (self.x, self.y), self.radio + 2)
            color_final = color_resaltado if color_resaltado else self.color
            pygame.draw.circle(pantalla, color_final, (self.x, self.y), self.radio)

    def mover(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.x = columna * TAM_CUADRO + TAM_CUADRO // 2
        self.y = fila * TAM_CUADRO + TAM_CUADRO // 2