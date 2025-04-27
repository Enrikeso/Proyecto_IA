import pygame
import sys

from Constantes import *
from Fichas import Ficha

pygame.init()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Damas")

# Crear las fichas
fichas = []

def crear_fichas():
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if (fila + columna) % 2 != 0:
                if fila < 3:
                    fichas.append(Ficha(fila, columna, ROJO))
                elif fila > 4:
                    fichas.append(Ficha(fila, columna, GRIS))

def dibujar_tablero(pantalla):
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
            pygame.draw.rect(pantalla, color, (columna * TAM_CUADRO, fila * TAM_CUADRO, TAM_CUADRO, TAM_CUADRO))

crear_fichas()

# Variables para mover fichas
ficha_seleccionada = None
offset_x = 0
offset_y = 0
movimientos_posibles = []
fichas_enemigas_comibles = []

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

                    movimientos_posibles = []
                    fichas_enemigas_comibles = []

                    fila_actual = ficha.y // TAM_CUADRO
                    columna_actual = ficha.x // TAM_CUADRO

                    # Revisar las 4 diagonales
                    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        nueva_fila = fila_actual + dx
                        nueva_columna = columna_actual + dy

                        # Verificar si dentro del tablero
                        if 0 <= nueva_fila < FILAS and 0 <= nueva_columna < COLUMNAS:
                            ocupado = False
                            for otra_ficha in fichas:
                                fila_ficha = otra_ficha.y // TAM_CUADRO
                                columna_ficha = otra_ficha.x // TAM_CUADRO
                                if fila_ficha == nueva_fila and columna_ficha == nueva_columna:
                                    ocupado = True
                                    # Si es enemigo y hay espacio detrás
                                    if otra_ficha.color != ficha.color:
                                        salto_fila = fila_actual + 2*dx
                                        salto_columna = columna_actual + 2*dy
                                        if 0 <= salto_fila < FILAS and 0 <= salto_columna < COLUMNAS:
                                            libre = True
                                            for f in fichas:
                                                if (f.y // TAM_CUADRO, f.x // TAM_CUADRO) == (salto_fila, salto_columna):
                                                    libre = False
                                                    break
                                            if libre:
                                                fichas_enemigas_comibles.append(otra_ficha)
                                    break
                            if not ocupado:
                                movimientos_posibles.append((nueva_fila, nueva_columna))
                    break

        # Detectar soltado
        if evento.type == pygame.MOUSEBUTTONUP:
            if ficha_seleccionada:
                pos = pygame.mouse.get_pos()
                columna = pos[0] // TAM_CUADRO
                fila = pos[1] // TAM_CUADRO

                # Verificar si es un movimiento posible
                if (fila, columna) in movimientos_posibles:
                    ficha_seleccionada.mover(fila, columna)
                else:
                    # Devolver ficha al lugar original si movimiento no válido
                    ficha_seleccionada.x = ficha_seleccionada.columna * TAM_CUADRO + TAM_CUADRO // 2
                    ficha_seleccionada.y = ficha_seleccionada.fila * TAM_CUADRO + TAM_CUADRO // 2

                ficha_seleccionada = None
                movimientos_posibles = []
                fichas_enemigas_comibles = []

        # Detectar arrastre
        if evento.type == pygame.MOUSEMOTION:
            if ficha_seleccionada:
                pos = pygame.mouse.get_pos()
                ficha_seleccionada.x = pos[0] + offset_x
                ficha_seleccionada.y = pos[1] + offset_y

    pantalla.fill(BLANCO)
    dibujar_tablero(pantalla)

    # Dibujar movimientos posibles
    for fila, columna in movimientos_posibles:
        if 0 <= fila < 8 and 0 <= columna < 8:
            x = columna * TAM_CUADRO + TAM_CUADRO // 2
            y = fila * TAM_CUADRO + TAM_CUADRO // 2
            radio = TAM_CUADRO // 2 - 15
            pygame.draw.circle(pantalla, (200, 200, 200), (x, y), radio)

    # Dibujar fichas comibles
    for ficha in fichas_enemigas_comibles:
        pygame.draw.circle(pantalla, (0, 255, 0), (ficha.x, ficha.y), ficha.radio + 5, 5)

    # Dibujar todas las fichas
    for ficha in fichas:
        ficha.dibujar(pantalla)

    pygame.display.flip()