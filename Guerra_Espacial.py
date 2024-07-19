import pygame
import random
import sys
import os
import config  # Importa el módulo de configuración


# Inicialización de Pygame
pygame.init()

# Inicialización del mezclador de sonido
pygame.mixer.init()


# Constantes de configuración
ANCHO, ALTO = 1024, 768
BARRA_LATERAL_ANCHO = 180
FPS = 30
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERDE_CLARO = (0, 255, 0)
ROJO = (200, 0, 0)
ROJO_CLARO = (255, 0, 0)



# Constante para el evento de cambio de visibilidad de estrellas
CAMBIAR_VISIBILIDAD_ESTRELLAS_EVENTO = pygame.USEREVENT + 1

# Configura el temporizador para que genere el evento cada 1 segundo
pygame.time.set_timer(CAMBIAR_VISIBILIDAD_ESTRELLAS_EVENTO, 1000)

# Definir la cantidad de estrellas
CANTIDAD_ESTRELLAS = 100

# Función para crear el fondo estrellado
def crear_fondo_estrellado():
    estrellas = []
    for _ in range(CANTIDAD_ESTRELLAS):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        estrellas.append((x, y))
    return estrellas

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO + BARRA_LATERAL_ANCHO, ALTO))
pygame.display.set_caption("Guerra Espacial")

# Cargar y redimensionar imágenes
def cargar_imagen_redimensionada(ruta, ancho, alto):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (ancho, alto))

jugador_img = cargar_imagen_redimensionada("jugador.png", 50, 50)
enemigo_img = cargar_imagen_redimensionada("enemigo.png", 40, 40)
bala_img = cargar_imagen_redimensionada("bala.png", 20, 40)
explosion_img = cargar_imagen_redimensionada("explosion.png", 50, 50)

# Cargar sonidos
sonido_eliminacion = pygame.mixer.Sound("D:\\Users\\Victor Gimenez\\Desktop\\ING INFORMATICA\\5° Año\\Optativa\\Trabajo práctico_pygame\\sounds\\sfx\\brick-bump.ogg")
sonido_disparo = pygame.mixer.Sound("D:\\Users\\Victor Gimenez\\Desktop\\ING INFORMATICA\\5° Año\\Optativa\\Trabajo práctico_pygame\\sounds\\sfx\\brick-bump.ogg")
sonido_muerte = pygame.mixer.Sound("D:\\Users\\Victor Gimenez\\Desktop\\ING INFORMATICA\\5° Año\\Optativa\\Trabajo práctico_pygame\\sounds\\sfx\\death.wav")



# Clases
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jugador_img
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.vel_x = 10
        self.vel_y = 10
        self.vidas = 3

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel_x
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel_x
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.vel_y
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.vel_y

        if pygame.sprite.spritecollideany(self, enemigos):
            self.vidas -= 1
            if self.vidas > 0:
                self.reaparecer()
            else:
                sonido_muerte.play()
                return False
        return True

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_sprites.add(bala)
        balas.add(bala)
        sonido_disparo.play()

    def reaparecer(self):
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemigo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.vel_y = random.randint(1, 4)

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.vel_y = random.randint(1, 4)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bala_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vel_y = -10

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= 9:
                self.kill()

def crear_grupos():
    global todas_las_sprites, enemigos, balas, explosiones, jugador
    todas_las_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    explosiones = pygame.sprite.Group()

    jugador = Jugador()
    todas_las_sprites.add(jugador)

def crear_enemigos(numero):
    for _ in range(numero):
        enemigo = Enemigo()
        todas_las_sprites.add(enemigo)
        enemigos.add(enemigo)

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, BLANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def pantalla_pausa():
    en_pausa = True
    while en_pausa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_c:
                    en_pausa = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    quit()

        ventana.fill(NEGRO)
        draw_text(ventana, "Pausado", 115, ANCHO / 2, ALTO / 4)
        draw_text(ventana, "Presiona C para continuar o Q para salir", 35, ANCHO / 2, ALTO / 2)
        pygame.display.flip()
        reloj.tick(5)

def pantalla_game_over():
    ventana.fill(NEGRO)
    draw_text(ventana, "GAME OVER", 115, ANCHO / 2, ALTO / 4)
    draw_text(ventana, "Presiona R para reiniciar o Q para salir", 35, ANCHO / 2, ALTO / 2)
    pygame.display.flip()
    reloj.tick(5)

    game_over = True
    while game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    return False


def mostrar_ventana_advertencia():
    reloj = pygame.time.Clock()
    advertencia = True
    font = pygame.font.SysFont(None, 50)

    while advertencia:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Permitir salir con Escape
                    pygame.quit()
                    quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if boton_aceptar.collidepoint(mouse):
                    advertencia = False

        ventana.fill(NEGRO)
        draw_text(ventana, "Es necesario que introduzca su nombre para jugar", 50, ANCHO / 2, ALTO / 2 - 50)

        # Botón Aceptar
        boton_aceptar = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 + 10, 200, 50)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if boton_aceptar.collidepoint(mouse):
            pygame.draw.rect(ventana, VERDE_CLARO, boton_aceptar)
            if click[0] == 1:
                advertencia = False
        else:
            pygame.draw.rect(ventana, VERDE, boton_aceptar)

        draw_text(ventana, "Aceptar", 30, ANCHO / 2, ALTO / 2 + 25)

        pygame.display.flip()
        reloj.tick(15)

def pantalla_inicio():
    global nombre_usuario
    config.nombre_usuario = ""  # Usa la variable de configuración
    reloj = pygame.time.Clock()
    intro = True
    font = pygame.font.SysFont(None, 50)
    color_fondo_texto = (0, 0, 255)  # Azul

    pygame.mixer.music.load("sounds/castle1.mid")
    pygame.mixer.music.play(-1)

    while intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Verifica si el campo de nombre no está vacío antes de iniciar el juego
                    if nombre_usuario:
                        intro = False
                    else:
                        mostrar_ventana_advertencia()
                if evento.key == pygame.K_BACKSPACE:
                    config.nombre_usuario = config.nombre_usuario[:-1]
                elif evento.key == pygame.K_ESCAPE:  # Opcional: permitir salir con Escape
                    pygame.quit()
                    quit()
            if evento.type == pygame.KEYUP:
                if evento.key >= pygame.K_a and evento.key <= pygame.K_z or evento.key >= pygame.K_0 and evento.key <= pygame.K_9:
                    config.nombre_usuario += evento.unicode

        ventana.fill(NEGRO)
        draw_text(ventana, "Bienvenido Soldado, ¿Listo para la misión?", 65, ANCHO / 2, ALTO / 4)

        draw_text(ventana, "Ingrese su nombre:", 40,  ANCHO / 2, ALTO / 2.1 - 30)
       # Fondo azul para el área de entrada de texto
        entrada_rect = pygame.Rect(ANCHO / 2 - 150, ALTO / 2 - 20, 300, 40)  # Define el rectángulo para el área de texto
        pygame.draw.rect(ventana, color_fondo_texto, entrada_rect)  # Dibuja el fondo azul

        entrada_texto = font.render(config.nombre_usuario, True, BLANCO)
        ventana.blit(entrada_texto, (ANCHO / 2 - entrada_texto.get_width() / 2, ALTO / 2 - 20))

        boton_inicio = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 + 50, 200, 50)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if boton_inicio.collidepoint(mouse):
            pygame.draw.rect(ventana, VERDE_CLARO, boton_inicio)
            if click[0] == 1:
                if config.nombre_usuario:
                    sonido_seleccion = pygame.mixer.Sound("D:\\Users\\Victor Gimenez\\Desktop\\ING INFORMATICA\\5° Año\\Optativa\\Trabajo práctico_pygame\\sounds\\sfx\\coin.ogg")
                    sonido_seleccion.play()
                    intro = False
                else:
                    mostrar_ventana_advertencia()
        else:
            pygame.draw.rect(ventana, VERDE, boton_inicio)

        

        draw_text(ventana, "Iniciar Juego", 30, ANCHO / 2, ALTO / 2 + 60)

        pygame.display.flip()
        reloj.tick(15)

def pantalla_pausa():
    en_pausa = True
    while en_pausa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_c:
                    en_pausa = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    quit()

        ventana.fill(NEGRO)
        draw_text(ventana, "Pausado", 115, ANCHO / 2, ALTO / 4)
        draw_text(ventana, "Presiona C para continuar o Q para salir", 35, ANCHO / 2, ALTO / 2)
        pygame.display.flip()
        reloj.tick(5)

def pantalla_game_over():
    ventana.fill(NEGRO)
    draw_text(ventana, "GAME OVER", 115, ANCHO / 2, ALTO / 4)
    draw_text(ventana, "Presiona R para reiniciar o Q para salir", 35, ANCHO / 2, ALTO / 2)
    pygame.display.flip()
    reloj.tick(5)

    game_over = True
    while game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    return False

def mostrar_ventana_nivel_superado():
    ventana.fill(NEGRO)
    draw_text(ventana, "Felicidades!!! Primer Nivel Superado!!!", 65, ANCHO / 2, ALTO / 4)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    boton_segundo_nivel = pygame.Rect(ANCHO / 2 - 100, ALTO / 2, 200, 50)
    if boton_segundo_nivel.collidepoint(mouse):
        pygame.draw.rect(ventana, VERDE_CLARO, boton_segundo_nivel)
        if click[0] == 1:
             # Ejecutar el archivo nivel2.py
            os.system('python nivel2.py')
            return False  # Para terminar el bucle del primer nivel
    else:
        pygame.draw.rect(ventana, VERDE, boton_segundo_nivel)

    draw_text(ventana, "Segundo nivel", 30, ANCHO / 2, ALTO / 2 + 10)
    pygame.display.flip()

    # Bucle para mantener la ventana emergente hasta que el usuario haga clic en el botón
    ventana_abierta = True
    while ventana_abierta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_segundo_nivel.collidepoint(evento.pos):
                    ventana_abierta = False


def reiniciar_juego():
    global corriendo, puntuacion, fondo_estrellas
    crear_grupos()
    crear_enemigos(8)
    fondo_estrellas = crear_fondo_estrellado()
    puntuacion = 0
    return True

# Pantalla de inicio
pantalla_inicio()

# Variables del juego
corriendo = True
puntuacion = 0
reloj = pygame.time.Clock()

# Crear grupos y enemigos iniciales
crear_grupos()
crear_enemigos(8)

# Crear fondo estrellado
fondo_estrellas = crear_fondo_estrellado()

def dibujar_botones_laterales():
    boton_pausa = pygame.Rect(ANCHO + BARRA_LATERAL_ANCHO // 1.5 - 100, ALTO / 2 + 50, 150, 50)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if boton_pausa.collidepoint(mouse):
        pygame.draw.rect(ventana, VERDE_CLARO, boton_pausa)
        if click[0] == 1:
            pantalla_pausa()
    else:
        pygame.draw.rect(ventana, VERDE, boton_pausa)

    draw_text(ventana, "Pausar", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, ALTO / 2 + 65)

    # Botón de Salir
    boton_salir = pygame.Rect(ANCHO + BARRA_LATERAL_ANCHO // 1.5 - 100, ALTO / 2 + 120, 150, 50)

    if boton_salir.collidepoint(mouse):
        pygame.draw.rect(ventana, ROJO_CLARO, boton_salir)
        if click[0] == 1:
            pygame.quit()
            sys.exit()

    else:
        pygame.draw.rect(ventana, ROJO, boton_salir)

    draw_text(ventana, "Salir", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, ALTO / 2 + 135)


    # Mostrar nombre del usuario
    draw_text(ventana, f"Usuario: {config.nombre_usuario}", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, ALTO / 2 - 30)

# Cargar la música de fondo
pygame.mixer.music.load("sounds\\background_music.mp3")
pygame.mixer.music.play(-1) # Reproducir en bucle
# Bucle principal del juego
while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jugador.disparar()
            if evento.key == pygame.K_p:
                pantalla_pausa()
            if evento.key == pygame.K_r:
                corriendo = reiniciar_juego()
        if evento.type == CAMBIAR_VISIBILIDAD_ESTRELLAS_EVENTO:
            fondo_estrellas = crear_fondo_estrellado()

    if not jugador.update():
        if pantalla_game_over():
            corriendo = reiniciar_juego()
        else:
            corriendo = False

    todas_las_sprites.update()

    colisiones = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones:
        puntuacion += 10
        explosion = Explosion(colision.rect.center)
        todas_las_sprites.add(explosion)
        explosiones.add(explosion)
        sonido_eliminacion.play()
        enemigo = Enemigo()
        todas_las_sprites.add(enemigo)
        enemigos.add(enemigo)

    if puntuacion >= 100:
        if mostrar_ventana_nivel_superado():
            # Aquí puedes almacenar un # o realizar otra acción
          corriendo = False

    ventana.fill(NEGRO)
    for estrella in fondo_estrellas:
        ventana.fill(BLANCO, (estrella[0], estrella[1], 2, 2))
    todas_las_sprites.draw(ventana)

    AZUL = (0, 0, 255)

    pygame.draw.rect(ventana, AZUL, (ANCHO, 0, BARRA_LATERAL_ANCHO, ALTO))

    draw_text(ventana, "Guerra Espacial", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, 20)
    draw_text(ventana, "Nivel 1", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, 60)
    draw_text(ventana, f"Puntuación: {puntuacion}", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, 90)
    draw_text(ventana, f"Vidas: {jugador.vidas}", 30, ANCHO + BARRA_LATERAL_ANCHO // 2, 120)

    dibujar_botones_laterales()

    pygame.display.flip()
    reloj.tick(FPS)

    

pygame.quit()
sys.exit()
