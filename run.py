import pygame
import math
import random
import sys

pygame.init()

score = 0

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
imgList = [pygame.image.load('traffic-light.png'), pygame.image.load(
    'barrier.png'), pygame.image.load('traffic-sign.png'), pygame.image.load('vlc.png')]
obstacleImg = imgList[random.randint(0, 3)]
#obstacleX = XList[random.randrange(0, 3)]
obstacleY = 0
noOfObstacles=7
Y_change=5

#
X,Y,imgD={},{},{}
for i in range(noOfObstacles):
    img=imgList[random.randint(0,3)]
    imgD[i]=img
    X[i]=XList[random.randint(0,3)]
    Y[i]=obstacleY-120*i
#

def player(playerX, playerY):
    screen.blit(playerImg, (playerX, playerY))


def obstacle(imgD,X,Y):
    #screen.blit(obstacleImg, (obstacleX, obstacleY));param:obstacleImg,obstacleX,obstacleY
    #
    for i in range(noOfObstacles):
        screen.blit(imgD[i],(X[i],Y[i]))
    #


def collide(playerX, playerY, obstacleX, obstacleY):
    dist = math.fabs(playerY-obstacleY)
    if dist < 30 and playerX == obstacleX:
        return True
    else:
        return False


def gameOver(score):
    gameFont = pygame.font.Font('freesansbold.ttf', 64)
    gameText1 = gameFont.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gameText1, (200, 200))
    gameText2 = gameFont.render('Score:'+str(score), True, (255, 255, 255))
    screen.blit(gameText2, (250, 300))
    
def overlap(X,Y,i):
    for j in range(noOfObstacles):
        if j!=i:
            if X[j]==X[i] and math.fabs(Y[j]-Y[i])<80:
                return True    
    else:
        return False

def spaced(X,Y,i):
    if overlap(X,Y,i):
        try:
            X[i]=XList[i+1]
        except:
            pass
        Y[i]-=30
        spaced(X,Y,i)
    else:
        return

# game loop
running = True

while running:
    
    # background
    screen.blit(background, (0, 0))

    #title and icon
    pygame.display.set_caption("NameOfGame")
    icon = pygame.image.load('vampire.png')
    pygame.display.set_icon(icon)

    # game over
   
    for i in range(noOfObstacles):
        if collide(playerX,playerY,X[i],Y[i]):
            gameOver(score)
            Y_change=0
            for j in range(noOfObstacles):
                Y[j]=playerY
        else:
            if Y[i]>=640:
                Y[i]=0
                X[i]=XList[random.randint(0,3)]                
                
                spaced(X,Y,i)

            else:
                Y[i]+=Y_change
    
    # keyboard input
    for event in pygame.event.get():
        # action on clicking the x
        if event.type == pygame.QUIT:
            running = False
        # action on pressing arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if XList.index(playerX) != 3:
                    playerX = XList[XList.index(playerX)+1]
            elif event.key == pygame.K_LEFT:
                if XList.index(playerX) != 0:
                    playerX = XList[XList.index(playerX)-1]

    obstacle(imgD,X,Y)
    player(playerX, playerY)
    pygame.display.update()
