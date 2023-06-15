import pygame
import random
import math
from pygame import mixer
#Istalei o Pygame
pygame.init()

#criar a tela
screen = pygame.display.set_mode((800, 600))

#fundo
background = pygame.image.load("background.png")

# Musica de fundo
mixer.music.load("background.wav")
mixer.music.play(-1)

#Título e Ícone
pygame.display.set_caption("Invasores Do Espaço")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Jogadores
playerImg = pygame.image.load("player.png")
playerX = 370 
playerY = 480
playerX_change = 0

# Inimigo
enemyImg = list()
enemyX = list()
enemyY = list()
enemyX_change = list()
enemyY_change = list()
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bala

# Pronto - Você não pode ver o marcador na tela
# Fogo - A bala está se movendo no momento

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = str("ready")

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 25)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font("freesansbold.ttf", 54)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER  " + str(score_value), True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))



def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bullerY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bullerY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Loop de jogo
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Imagem de Fundo
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # se a tecla for pressionada, verifique se está à direita ou à esquerda
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is str("ready"):
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Verificando os limites da nave espacial para que ela não saia dos limites
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # movimento inimigo
    for i in range(num_of_enemies):
        # Game Over

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = str("ready")
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = str("ready")

    if bullet_state is str("fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()