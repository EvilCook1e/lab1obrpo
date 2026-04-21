import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 400
GROUND = HEIGHT - 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Прыгун")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

dino_x = 80
dino_y = GROUND - 40
dino_width = 30
dino_height = 40
dino_vel_y = 0
is_jumping = False


cactus_x = WIDTH
cactus_width = 20
cactus_height = 30
cactus_speed = 7

score = 0
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                dino_vel_y = -15
    
    if is_jumping:
        dino_vel_y += 1
        dino_y += dino_vel_y
        if dino_y >= GROUND - dino_height:
            dino_y = GROUND - dino_height
            is_jumping = False
    
    cactus_x -= cactus_speed
    if cactus_x < -cactus_width:
        cactus_x = WIDTH
        score += 1
        if score % 5 == 0:
            cactus_speed += 1
    
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    cactus_rect = pygame.Rect(cactus_x, GROUND - cactus_height, cactus_width, cactus_height)
    
    if dino_rect.colliderect(cactus_rect):
        running = False
    
    screen.fill((255, 255, 255))
    

    pygame.draw.rect(screen, (0, 0, 0), (0, GROUND, WIDTH, 3))
    
   
    pygame.draw.rect(screen, (0, 0, 0), (dino_x, dino_y, dino_width, dino_height))
    pygame.draw.circle(screen, (255, 255, 255), (dino_x + 25, dino_y + 10), 3)
    pygame.draw.circle(screen, (0, 0, 0), (dino_x + 25, dino_y + 10), 1)
    

    pygame.draw.rect(screen, (0, 150, 0), (cactus_x, GROUND - cactus_height, cactus_width, cactus_height))
    pygame.draw.rect(screen, (0, 150, 0), (cactus_x + 5, GROUND - cactus_height - 15, 10, 15))
    

    text = font.render(f"Счёт: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    
    pygame.display.update()
    clock.tick(60)


screen.fill((255, 255, 255))
game_over_text = font.render("", True, (255, 0, 0))
score_text = font.render(f"Счёт: {score}", True, (0, 0, 0))
restart_text = font.render("Нажми пробл чтобы играть снова", True, (0, 0, 0))

screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 50))
screen.blit(score_text, (WIDTH//2 - 50, HEIGHT//2))
screen.blit(restart_text, (WIDTH//2 - 130, HEIGHT//2 + 50))
pygame.display.update()


waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting = False
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)

pygame.quit()