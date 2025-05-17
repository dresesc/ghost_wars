import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ghost Wars")

# Ruta base
BASE_PATH = os.path.dirname(__file__)

IMAGES_PATH = os.path.join(BASE_PATH, "assets", "imagenes")
SOUNDS_PATH = os.path.join(BASE_PATH, "assets", "sounds")
FONTS_PATH = os.path.join(BASE_PATH, "assets", "fonts")

# Imágenes
player_image = pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, "player.png")), (120, 120))
bullet_image = pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, "bullet.png")), (50, 50))
enemy_image = pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, "enemy.gif")), (80, 80))
background_image = pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, "background.png")), (width, height))

# Jugador
player_rect = player_image.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
player_speed = 15

# Bala
bullet_speed = 10
bullets = []

# Enemigos
enemy_speed = 3
enemies = []

# Texto
font = pygame.font.Font(os.path.join(FONTS_PATH, "retrotech.ttf"), 25)
big_font = pygame.font.Font(os.path.join(FONTS_PATH, "retrotech.ttf"), 100)
score = 0

# Reloj
clock = pygame.time.Clock()
keys_pressed = {'left': False, 'right': False}

# Estados del juego
MENU = 'menu'
RUNNING = 'running'
PAUSED = 'paused'
GAME_OVER = 'game_over'
state = MENU

# Botón de pausa
pause_button_rect = pygame.Rect(width - 50, 10, 30, 30)

# Música del juego
pygame.mixer.music.load(os.path.join(SOUNDS_PATH, "musica_fondo.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Sonidos del juego
sonido_disparo = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "disparo.wav"))
sonido_disparo.set_volume(0.2)

sonido_perdiste = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "game_over.mp3"))
sonido_perdiste.set_volume(0.2)

def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (1,23,28,255), rect)
    pygame.draw.rect(screen, (1,23,28,255), rect, 2)
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect

while True:
    screen.blit(background_image, (0, 0))

    if state == MENU:
        title = big_font.render("Ghost Wars", True, (255, 255, 255))
        screen.blit(title, (width//2 - title.get_width()//2, 100))
        play_button = draw_button("Jugar", 275, 300, 150, 60)
        quit_button = draw_button("Salir", 275, 400, 150, 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    state = RUNNING
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    elif state == RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keys_pressed['left'] = True
                elif event.key == pygame.K_RIGHT:
                    keys_pressed['right'] = True
                elif event.key == pygame.K_SPACE:
                    bullet_rect = bullet_image.get_rect()
                    sonido_disparo.play()

                    bullet = {
                        'rect': pygame.Rect(
                            player_rect.x + player_rect.width // 2 - bullet_rect.width // 2,
                            player_rect.y,
                            bullet_rect.width,
                            bullet_rect.height
                        ),
                        'image': bullet_image
                    }
                    bullets.append(bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys_pressed['left'] = False
                elif event.key == pygame.K_RIGHT:
                    keys_pressed['right'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.pause()  
                    state = PAUSED

        # Movimiento del jugador
        if keys_pressed['left'] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys_pressed['right'] and player_rect.right < width:
            player_rect.x += player_speed

        # Movimiento de balas
        for bullet in bullets:
            bullet['rect'].y -= bullet_speed
    

        # Generación de enemigos
        if random.randint(0, 100) < 2:
            enemy_rect = enemy_image.get_rect()
            enemy_rect.x = random.randint(0, width - enemy_rect.width)
            enemies.append(enemy_rect.copy())

        # Movimiento de enemigos
        for enemy in enemies:
            enemy.y += enemy_speed

        # Colisiones
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                if enemy.colliderect(bullet['rect']):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    score += 1

        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                pygame.mixer.music.stop() 
                state = GAME_OVER
                sonido_perdiste.play()

        # Dibujar objetos
        screen.blit(player_image, player_rect)
        for bullet in bullets:
            screen.blit(bullet['image'], bullet['rect'].topleft)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)

        # Contador
        score_text = font.render(f'Puntos : {score}', True, (255, 255, 255))
        score_rect = pygame.Rect(10, 10, score_text.get_width() + 30, score_text.get_height() + 16)
        pygame.draw.rect(screen, (1, 23, 28, 255), score_rect) 
        pygame.draw.rect(screen, (1, 23, 28, 255), score_rect, 2) 
        screen.blit(score_text, (score_rect.x + 15, score_rect.y + 8))

        # Botón de pausa
        pygame.draw.rect(screen, (1, 23, 28, 255), pause_button_rect)  
        pygame.draw.rect(screen, (255, 255, 255), (pause_button_rect.x + 6, pause_button_rect.y + 5, 5, 20))  
        pygame.draw.rect(screen, (255, 255, 255), (pause_button_rect.x + 17, pause_button_rect.y + 5, 5, 20)) 

        pygame.display.flip()
        clock.tick(60)

    elif state == PAUSED:
        # Pantalla de pausa
        pause_label = big_font.render("PAUSA", True, (255, 255, 255))
        screen.blit(pause_label, (width//2 - pause_label.get_width()//2, 220))

        # Botones en la pantalla de pausa
        resume_button = draw_button("Play", 275, 320, 150, 50)
        reset_button = draw_button("Reiniciar", 275, 390, 150, 50)
        menu_button = draw_button("Menu", 275, 460, 150, 50)
        quit_button = draw_button("Salir", 275, 530, 150, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    pygame.mixer.music.unpause() 
                    state = RUNNING
                elif reset_button.collidepoint(event.pos):
                    # Reinicia el juego
                    score = 0
                    bullets.clear()
                    enemies.clear()
                    player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
                    keys_pressed = {'left': False, 'right': False}
                    pygame.mixer.music.play(-1) 
                    state = RUNNING
                elif menu_button.collidepoint(event.pos):
                    # Reinicia para volver al menú
                    score = 0
                    bullets.clear()
                    enemies.clear()
                    player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
                    keys_pressed = {'left': False, 'right': False}
                    pygame.mixer.music.play(-1) 
                    state = MENU
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    elif state == GAME_OVER:
        # Pantalla de "Perdiste"
        lose_label = big_font.render("PERDISTE", True, (255, 0, 0))
        screen.blit(lose_label, (width//2 - lose_label.get_width()//2, 180))

        play_again_button = draw_button("Jugar de nuevo", 225, 350, 250, 60)
        menu_button = draw_button("Menu", 275, 430, 150, 50)
        quit_button = draw_button("Salir", 275, 500, 150, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    # Reinicia el juego
                    score = 0
                    bullets.clear()
                    enemies.clear()
                    player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
                    keys_pressed = {'left': False, 'right': False}
                    pygame.mixer.music.play(-1) 
                    state = RUNNING
                elif menu_button.collidepoint(event.pos):
                    # Reinicia para volver al menú
                    score = 0
                    bullets.clear()
                    enemies.clear()
                    player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
                    keys_pressed = {'left': False, 'right': False}
                    pygame.mixer.music.play(-1) 
                    state = MENU
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
