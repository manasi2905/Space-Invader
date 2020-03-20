import math
import random
import pygame

# Intialize the pygame
pygame.init()

# create a screen of width=800 pixels, height=600 pixels
screen = pygame.display.set_mode((800, 600))

# Background music
#pygame.mixer.music.load('Game-Menu.mp3')
#pygame.mixer.music.play()

# Background image
background = pygame.image.load("background.jpg")

# change the caption of the screen
pygame.display.set_caption("Space Invaders")
# change the icon of the screen
icon = pygame.image.load('/home/manasi/PycharmProjects/space_invader/alien.png')
pygame.display.set_icon(icon)

# Player image
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies= 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.2)
    enemyY_change.append(40)

# Bullet image
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
# ready = you can't see the bullet
# fire - bullet is currently moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY =10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    # X+16 = center of spaceship
    # y+10 = a little above spaceship
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # changing background colour
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    # check all the event taking place
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed  check whether its right/left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player
    playerX = playerX + playerX_change
    # setting boundary
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:  # 800-64
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        enemyX[i] = enemyX[i] + enemyX_change[i]
        # setting boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.2
            enemyY[i] = enemyY[i] + enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -1.2
            enemyY[i] = enemyY[i] + enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value = score_value + 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # allows multiple bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # bullet movement
    if bullet_state is "fire":
        fire(bulletX, bulletY)
        bulletY = bulletY - bulletY_change

    player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
