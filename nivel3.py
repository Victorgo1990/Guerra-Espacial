import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Constantes de configuración
ANCHO, ALTO = 1024, 768
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (200, 0, 0)
ROJO_CLARO = (255, 0, 0)

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Nivel 3 Superado")

# Función para dibujar texto en la pantalla
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, BLANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Función para mostrar la ventana de nivel 3 superado
def mostrar_ventana_nivel3_superado():
    ventana.fill(NEGRO)
    draw_text(ventana, "Felicidades...Has superado todos los niveles!!!", 65, ANCHO / 2, ALTO / 4)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    boton_salir = pygame.Rect(ANCHO / 2 - 100, ALTO / 2, 200, 50)
    if boton_salir.collidepoint(mouse):
        pygame.draw.rect(ventana, ROJO_CLARO, boton_salir)
        if click[0] == 1:
            pygame.quit()
            sys.exit()
    else:
        pygame.draw.rect(ventana, ROJO, boton_salir)

    draw_text(ventana, "Salir", 30, ANCHO / 2, ALTO / 2 + 10)
    pygame.display.flip()

    # Bucle para mantener la ventana emergente hasta que el usuario haga clic en el botón
    ventana_abierta = True
    while ventana_abierta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir.collidepoint(evento.pos):
                    ventana_abierta = False

# Llamada a la función para mostrar la ventana
mostrar_ventana_nivel3_superado()
