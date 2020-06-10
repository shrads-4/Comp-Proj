import pygame
import math
import random

pygame.init()

score=0

# creating the screen
screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)

# background
background = pygame.image.load('background.png')

XList = [225, 330, 425, 520]

# player
playerImg = pygame.image.load('vampire.png')
playerX = 330
playerY = 550

# obstacle, 225 on 1, 330 on 2,  520 on 4
obstacleImg = pygame.image.load('barrier.png')
obstacleX = XList[random.randrange(0, 3)]
obstacleY = 0


def player(playerX,playerY):
    screen.blit(playerImg, (playerX, playerY))


def obstacle(obstacleX,obstacleY):
    screen.blit(obstacleImg, (obstacleX, obstacleY))

def collide(playerY,obstacleY):
    dist=math.fabs(playerY-obstacleY)
    if dist<20:
        return True
    else:
        return False

def gameOver(score):
    gameFont=pygame.font.Font('freesansbold.ttf',64)
    gameText1=gameFont.render('GAME OVER',True,(255,255,255))
    screen.blit(gameText1,(200,200))
    gameText2=gameFont.render('Score:'+str(score),True,(255,255,255))
    screen.blit(gameText2,(250,300))

# game loop
running = True

while running:

    # background
    screen.blit(background, (0, 0))

    #title and icon
    pygame.display.set_caption("NameOfGame")
    icon = pygame.image.load('vampire.png')
    pygame.display.set_icon(icon)

    #game over
    if collide(playerY,obstacleY):
        gameOver(score)
    #obstacle movement
    else:
        obstacleY+=3

    #keyboard input
    for event in pygame.event.get():
        # action on clicking the x
        if event.type == pygame.QUIT:
            running = False
        #action on pressing arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if XList.index(playerX) != 3:
                    playerX = XList[XList.index(playerX)+1]
            elif event.key == pygame.K_LEFT:
                if XList.index(playerX) != 0:
                    playerX = XList[XList.index(playerX)-1]

    obstacle(obstacleX,obstacleY)
    player(playerX,playerY)
    pygame.display.update()
