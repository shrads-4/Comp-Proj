import pygame
import math
import random

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

#
X,Y,imgD={},{},{}
for i in range(noOfObstacles):
    img=imgList[random.randint(0,3)]
    imgD[i]=img
    X[i]=XList[random.randint(0,3)]
    Y[i]=obstacleY-125*i
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
    '''if collide(playerX, playerY, obstacleX, obstacleY):
        gameOver(score)
    '''
    for i in range(noOfObstacles):
        if collide(playerX,playerY,X[i],Y[i]):
            gameOver(score)
        else:
            if Y[i]>=640:
                Y[i]=0
                X[i]=XList[random.randint(0,3)]
                
                spaced=True
                while spaced:
                    for j in range(noOfObstacles):
                        if X[i]==X[j] and math.fabs(Y[i]-Y[j])<=80:
                           X[i]=XList[random.randrange(0,3)]
                           j=0
                    else:
                        spaced=False               
            else:
                Y[i]+=5
    '''
    # obstacle movement
    else:
        if obstacleY >= 640:
            obstacleY = 0
            obstacleX = XList[random.randrange(0, 3)]
        obstacleY += 5
    '''
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
