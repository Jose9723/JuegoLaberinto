import pygame
import sys

ANCHO, ALTO = 650, 800
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VERDE_OSCURO = (0, 200, 0)
ROJO_OSCURO = (200, 0, 0)
FPS = 30

LABERINTO = [
    "00000000000000000000",
    "011111111111111111010",
    "010000010100000000010",
    "011111010101111101110",
    "010100010101000100010",
    "010101000001010111110",
    "010101111011010101010",
    "010100010000010001010",
    "010101011111011111010",
    "010111000010000000010",
    "010000011010111111110",
    "011111010000000000010",
    "010000010111110111110",
    "010111110101010101010",
    "010000000001010101010",
    "010111111101010001010",
    "010100000001011101010",
    "010101111111000001010",
    "010100000100011101010",
    "010111110101010111010",
    "010100000101000000010",
    "010101110101111111110",
    "010101010000000010010",
    "111111011111101011010",
    "100000000000001000010",
    "111111111111111111110"
]

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Laberinto")
reloj = pygame.time.Clock()

TAMANO_CELDA = 30

imagen_jugador = pygame.transform.scale(pygame.image.load("jugador.webp"), (TAMANO_CELDA, TAMANO_CELDA))
imagen_pared = pygame.transform.scale(pygame.image.load("pared.jpg"), (TAMANO_CELDA, TAMANO_CELDA))
imagen_camino = pygame.transform.scale(pygame.image.load("camino.jpeg"), (TAMANO_CELDA, TAMANO_CELDA))
imagen_meta = pygame.transform.scale(pygame.image.load("meta.jpg"), (TAMANO_CELDA, TAMANO_CELDA))
imagen_obstaculo = pygame.transform.scale(pygame.image.load("fantasma.webp"), (TAMANO_CELDA, TAMANO_CELDA))

OBSTACULOS = [
    {'pos': (16, 2), 'dir': (0, 1)},  
    {'pos': (11, 10), 'dir': (0, 1)}, 
    {'pos': (8, 14), 'dir': (0, 1)},  
    {'pos': (9, 5), 'dir': (0, 1)}, 
    {'pos': (6, 24), 'dir': (0, 1)},   
    {'pos': (2, 10), 'dir': (1, 0)}   
]

VELOCIDAD_OBSTACULO = 1

def dibujar_laberinto():
    for y, fila in enumerate(LABERINTO):
        for x, celda in enumerate(fila):
            rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            if celda == '1':
                pantalla.blit(imagen_pared, rect.topleft)
            else:
                pantalla.blit(imagen_camino, rect.topleft)

def dibujar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        x, y = obstaculo['pos']
        rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
        pantalla.blit(imagen_obstaculo, rect.topleft)

def mover_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        x, y = obstaculo['pos']
        dx, dy = obstaculo['dir']
        
        nuevo_x = x + dx * VELOCIDAD_OBSTACULO
        nuevo_y = y + dy * VELOCIDAD_OBSTACULO
        
        nuevo_x = int(round(nuevo_x))
        nuevo_y = int(round(nuevo_y))
        
        if (0 <= nuevo_x < len(LABERINTO[0]) and 0 <= nuevo_y < len(LABERINTO) and 
            LABERINTO[nuevo_y][nuevo_x] == '0'):
            obstaculo['pos'] = (nuevo_x, nuevo_y)
        else:
            if dx != 0:
                obstaculo['dir'] = (-dx, dy)
            else:
                obstaculo['dir'] = (dx, -dy)

def dibujar_texto(texto, tamano_fuente, color, posicion):
    fuente = pygame.font.Font(None, tamano_fuente)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=posicion)
    pantalla.blit(superficie_texto, rect_texto)

def dibujar_boton(texto, rect, color, color_hover, accion=None):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(pantalla, color_hover, rect)
        if click[0] == 1 and accion:
            accion()
    else:
        pygame.draw.rect(pantalla, color, rect)
    
    dibujar_texto(texto, 40, NEGRO, rect.center)

def manejar_fin_juego(resultado):
    global fin_juego
    global resultado_fin_juego
    fin_juego = True
    resultado_fin_juego = resultado

def principal():
    global fin_juego
    global resultado_fin_juego
    fin_juego = False
    resultado_fin_juego = ""

    jugador_x, jugador_y = 1, 24
    rect_jugador = pygame.Rect(jugador_x * TAMANO_CELDA, jugador_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
    meta_x, meta_y = 18, 1
    rect_meta = pygame.Rect(meta_x * TAMANO_CELDA, meta_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not fin_juego:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and LABERINTO[jugador_y][jugador_x - 1] == '0':
                jugador_x -= 1
            if teclas[pygame.K_RIGHT] and LABERINTO[jugador_y][jugador_x + 1] == '0':
                jugador_x += 1
            if teclas[pygame.K_UP] and LABERINTO[jugador_y - 1][jugador_x] == '0':
                jugador_y -= 1
            if teclas[pygame.K_DOWN] and LABERINTO[jugador_y + 1][jugador_x] == '0':
                jugador_y += 1

            rect_jugador.topleft = (jugador_x * TAMANO_CELDA, jugador_y * TAMANO_CELDA)

            mover_obstaculos(OBSTACULOS)

            if (jugador_x, jugador_y) in [obstaculo['pos'] for obstaculo in OBSTACULOS]:
                manejar_fin_juego("¡Derrota!")

            if jugador_x == meta_x and jugador_y == meta_y:
                manejar_fin_juego("¡Victoria!")

        pantalla.fill(BLANCO)
        dibujar_laberinto()
        dibujar_obstaculos(OBSTACULOS)
        pantalla.blit(imagen_jugador, rect_jugador.topleft)
        pantalla.blit(imagen_meta, rect_meta.topleft)

        if fin_juego:
            dibujar_texto(resultado_fin_juego, 80, BLANCO, (ANCHO // 2, ALTO // 2 - 100))
            ancho_boton, alto_boton = 250, 50
            boton_x = ANCHO // 2 - ancho_boton // 2
            boton_y = ALTO // 2 + 50
            rect_boton = pygame.Rect(boton_x, boton_y, ancho_boton, alto_boton)
            
            def reiniciar():
                principal()
            
            def salir_juego():
                pygame.quit()
                sys.exit()
            
            dibujar_boton('Intentar de nuevo', rect_boton, VERDE, VERDE_OSCURO, reiniciar)
            
            boton_y += alto_boton + 10
            rect_boton = pygame.Rect(boton_x, boton_y, ancho_boton, alto_boton)
            dibujar_boton('Salir', rect_boton, ROJO, ROJO_OSCURO, salir_juego)
        
        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    principal()
