import pygame
import random
import math
from pygame import mixer

pygame.init()

mixer.pre_init(frequency=44100)

mixer.init(frequency=44100)

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_CH = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_CH = []
enemyY_CH = []
num_of_enemy = 6
# ENEMY
for i in range(num_of_enemy):
    enemyImg.append((pygame.image.load('pacman.png')))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemyX_CH.append(5)
    enemyY_CH.append(40)

# BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletX_CH = 0
bulletY_CH = 10
bullet_state = "ready"

mixer.music.load('background.wav')
mixer.music.play(-1)
backgroundImg = pygame.image.load('background.png')

# SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score():
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (textX, textY))


def PLAYER_POS():
    screen.blit(playerImg, (playerX, playerY))


def ENEMY_POS():
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


def BULLET_FIRE(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, ((x + 10), (y + 16)))


def Collision():
    distance = math.sqrt(math.pow((bulletX - enemyX[i]), 2) + math.pow((bulletY - enemyY[i]), 2))
    if distance < 27:
        return True

def GAME_OVER():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    g_over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(g_over, (200, 280))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_CH = -8
            if event.key == pygame.K_RIGHT:
                playerX_CH = 8
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    mixer.music.load('laser.wav')
                    mixer.music.play()
                   # bullet_shot = mixer.Sound('laser.wav')
                   # bullet_shot.play()

                    BULLET_FIRE(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_CH = 0
            if event.key == pygame.K_RIGHT:
                playerX_CH = 0
    if bullet_state is "fire":
        BULLET_FIRE(bulletX, bulletY)
        bulletY -= bulletY_CH
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

    for i in range(num_of_enemy):
        enemyX[i] += enemyX_CH[i]
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_CH[i] -= 5
            enemyY[i] += enemyY_CH[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_CH[i] += 5
            enemyY[i] += enemyY_CH[i]
        if enemyY[i] >= 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            GAME_OVER()
            break


    playerX += playerX_CH
    if playerX >= 736:
        playerX = 736
    if playerX <= 0:
        playerX = 0
    PLAYER_POS()
    for i in range(num_of_enemy):
        ENEMY_POS()
        if Collision():
            mixer.music.load('explosion.wav')
            mixer.music.play()
            bullet_state = "ready"
            score_value += 1
            bulletY = 480
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)
    show_score()
    pygame.display.update()
