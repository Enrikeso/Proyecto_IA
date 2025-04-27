import pygame
import sys

import Constantes as co
import Fichas as fich

pygame.init()

pantalla = pygame.display.set_mode((co.ANCHO_VENTANA, co.ALTO_VENTANA))
pygame.display.set_caption("Juego de Damas")

# Crear las fichas
fichas = []

def crear_fichas():
    for fila in range(co.FILAS):
        for columna in range(co.COLUMNAS):
            if (fila + columna) % 2 != 0:
                if fila < 3:
                    fichas.append(fich.Ficha(fila, columna, co.ROJO))
                elif fila > 4:
                    fichas.append(fich.Ficha(fila, columna, co.GRIS))

def dibujar_tablero(pantalla):
    for fila in range(co.FILAS):
        for columna in range(co.COLUMNAS):
            color = co.BLANCO if (fila + columna) % 2 == 0 else co.NEGRO
            pygame.draw.rect(pantalla, color, (columna * co.TAM_CUADRO, fila * co.TAM_CUADRO, co.TAM_CUADRO, co.TAM_CUADRO))

crear_fichas()

# Variables para mover fichas
ficha_seleccionada = None
offset_x = 0
offset_y = 0

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar click
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for ficha in fichas:
                distancia = ((pos[0] - ficha.x) ** 2 + (pos[1] - ficha.y) ** 2) ** 0.5
                if distancia < ficha.radio:
                    ficha_seleccionada = ficha
                    offset_x = ficha.x - pos[0]
                    offset_y = ficha.y - pos[1]
                    break

        # Detectar soltado
        if evento.type == pygame.MOUSEBUTTONUP:
            if ficha_seleccionada:
                pos = pygame.mouse.get_pos()
                columna = pos[0] // co.TAM_CUADRO
                fila = pos[1] // co.TAM_CUADRO
                ficha_seleccionada.mover(fila, columna)
                ficha_seleccionada = None

        # Detectar arrastre
        if evento.type == pygame.MOUSEMOTION:
            if ficha_seleccionada:
                pos = pygame.mouse.get_pos()
                ficha_seleccionada.x = pos[0] + offset_x
                ficha_seleccionada.y = pos[1] + offset_y

    pantalla.fill(co.BLANCO)
    dibujar_tablero(pantalla)

    for ficha in fichas:
        ficha.dibujar(pantalla)

    pygame.display.flip()