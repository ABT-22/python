import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong en Pygame")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de las paletas y la pelota
paddle_width, paddle_height = 15, 100
ball_size = 15

player1 = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
player2 = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)

# Velocidades
paddle_speed = 6
ball_speed_x, ball_speed_y = 5, 5

# Marcador
score1, score2 = 0, 0
font = pygame.font.Font(None, 36)

# Reloj para controlar FPS
clock = pygame.time.Clock()

running = True
game_over = False

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        # Movimiento de jugadores
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= paddle_speed
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += paddle_speed
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= paddle_speed
        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += paddle_speed
        
        # Movimiento de la pelota
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        
        # Rebote en la parte superior e inferior
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        
        # Colisión con las paletas
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1
        
        # Reiniciar pelota si sale de la pantalla y actualizar marcador
        if ball.left <= 0:
            score2 += 1
            ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_speed_x *= -1  # Cambiar dirección después de reiniciar
        if ball.right >= WIDTH:
            score1 += 1
            ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_speed_x *= -1  # Cambiar dirección después de reiniciar
        
        # Verificar si alguien ha ganado
        if score1 == 5 or score2 == 5:
            game_over = True
    
    # Dibujar los elementos en pantalla
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Dibujar marcador
    if game_over:
        if score1 == 5:
            win_text = font.render("WINNER", True, WHITE)
            lose_text = font.render("LOSER", True, WHITE)
            screen.blit(win_text, (WIDTH // 4 - win_text.get_width() // 2, HEIGHT // 2))
            screen.blit(lose_text, (3 * WIDTH // 4 - lose_text.get_width() // 2, HEIGHT // 2))
        else:
            win_text = font.render("WINNER", True, WHITE)
            lose_text = font.render("LOSER", True, WHITE)
            screen.blit(lose_text, (WIDTH // 4 - lose_text.get_width() // 2, HEIGHT // 2))
            screen.blit(win_text, (3 * WIDTH // 4 - win_text.get_width() // 2, HEIGHT // 2))
    else:
        score_text = font.render(f"{score1} - {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
