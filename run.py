import pygame
import math
import random
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

score = 0

# creating the screen
screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)

# background
background = pygame.image.load('background.png')

# button
buttonX = 300
buttonY = 400
color_light = (100, 100, 100)
color_dark = (50, 50, 50)
smallfont = pygame.font.SysFont('Corbel', 15)
returnText = smallfont.render('return to home page', True, (255, 255, 255))

XList = [225, 330, 425, 520]

# player
playerImg = pygame.image.load('vampire.png')
playerX = 330
playerY = 550

# obstacle, 225 on 1, 330 on 2,  520 on 4
imgList = [pygame.image.load('traffic-light.png'), pygame.image.load(
    'barrier.png'), pygame.image.load('traffic-sign.png'), pygame.image.load('vlc.png')]
obstacleY = 0
noOfObstacles = 6
Y_change = 5

X, Y, imgD = {}, {}, {}
for i in range(noOfObstacles):
    img = imgList[random.randint(0, 3)]
    imgD[i] = img
    X[i] = XList[random.randint(0, 3)]
    Y[i] = obstacleY-120*i
#


def player(playerX, playerY):
    screen.blit(playerImg, (playerX, playerY))


def obstacle(imgD, X, Y):
    for i in range(noOfObstacles):
        screen.blit(imgD[i], (X[i], Y[i]))
    #


def collide(playerX, playerY, obstacleX, obstacleY):
    dist = math.fabs(playerY-obstacleY)
    if dist < 30 and playerX == obstacleX:
        return True
    else:
        return False


def gameOver(score):
    gameFont = pygame.font.SysFont('Corbel', 64)
    gameText1 = gameFont.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gameText1, (200, 200))
    gameText2 = gameFont.render('Score:'+str(score), True, (255, 255, 255))
    screen.blit(gameText2, (250, 300))


def overlap(X, Y, i):
    for j in range(noOfObstacles):
        if j != i:
            if X[j] == X[i] and math.fabs(Y[j]-Y[i]) < 80:
                return True
    else:
        return False


def spaced(X, Y, i):
    if overlap(X, Y, i):
        try:
            X[i] = XList[i+1]
        except:
            pass
        Y[i] -= 30
        spaced(X, Y, i)
    else:
        return


def returnButton(mouse):
    if buttonX <= mouse[0] <= buttonX+140 and buttonY <= mouse[1] <= buttonY+40:
        pygame.draw.rect(screen, color_light, [buttonX, buttonY, 140, 40])
        #if event.type==pygame.MOUSEBUTTONDOWN:
            #import homepage.py
    else:
        pygame.draw.rect(screen, color_dark, [buttonX, buttonY, 140, 40])
    screen.blit(returnText, (buttonX+10, buttonY+10))


over = True
c=0
# game loop
running = True
quiz=False

while running:
    c+=1

    # background
    screen.blit(background, (0, 0))

    #title and icon
    pygame.display.set_caption("NameOfGame")
    icon = pygame.image.load('vampire.png')
    pygame.display.set_icon(icon)

    # game over
    for i in range(noOfObstacles):
        if collide(playerX, playerY, X[i], Y[i]):
            if over:
                score=c
            gameOver(score)
            over = False
            Y_change = 0
            for j in range(noOfObstacles):
                Y[j] = playerY

            mouse = pygame.mouse.get_pos()
            returnButton(mouse)

        else:
            if Y[i] >= 640:
                Y[i] = 0
                X[i] = XList[random.randint(0, 3)]

                spaced(X, Y, i)

            else:
                Y[i] += Y_change
    # quiz screen
    if c%1000==0:
        running=False
        quiz=True

    # keyboard input
    for event in pygame.event.get():
        # action on clicking the x
        if event.type == pygame.QUIT:
            running = False
        # action on pressing arrow keys
        if event.type == pygame.KEYDOWN:
            if over:
                if event.key == pygame.K_RIGHT:
                    if XList.index(playerX) != 3:
                        playerX = XList[XList.index(playerX)+1]
                elif event.key == pygame.K_LEFT:
                    if XList.index(playerX) != 0:
                        playerX = XList[XList.index(playerX)-1]

    obstacle(imgD, X, Y)
    player(playerX, playerY)
    pygame.display.update()

while quiz:
    import quizScreen