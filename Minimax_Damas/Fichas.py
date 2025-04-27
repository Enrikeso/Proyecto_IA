import pygame
from Constantes import TAM_CUADRO

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

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)

    def mover(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.actualizar_pos()