import pygame
import math
import random
import os
import time
import quizScreen

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

def run():
    # creating the screen
    runScreen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)

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
    obstacleY = 0
    noOfObstacles = 6
    Y_change = 5

    X, Y, imgD = {}, {}, {}


    def obsDicts(noOfObstacles, imgList, XList, obstacleY, X, Y, imgD):
        for i in range(noOfObstacles):
            img = imgList[random.randint(0, 3)]
            imgD[i] = img
            X[i] = XList[random.randint(0, 3)]
            Y[i] = obstacleY-120*i

    def showlevel(level, runScreen):
        start_time = time.time()
        levelfont = pygame.font.SysFont('Corbel', 75)
        text = levelfont.render('Level: '+str(level), True, (255, 255, 255))
        show = True
        while show:
            if time.time() - start_time < 3:
                runScreen.blit(text, (250, 200))
            else:
                show = False
            pygame.display.update()


    def player(playerX, playerY, runScreen, playerImg):
        runScreen.blit(playerImg, (playerX, playerY))


    def obstacle(imgD, X, Y, noOfObstacles, runScreen):
        for i in range(noOfObstacles):
            runScreen.blit(imgD[i], (X[i], Y[i]))


    def collide(playerX, playerY, obstacleX, obstacleY):
        dist = math.fabs(playerY-obstacleY)
        if dist < 30 and playerX == obstacleX:
            return True
        else:
            return False


    def gameOver(score, runScreen):
        gameFont = pygame.font.SysFont('Corbel', 64)
        gameText1 = gameFont.render('GAME OVER', True, (255, 255, 255))
        runScreen.blit(gameText1, (200, 200))
        gameText2 = gameFont.render('Score:'+str(score), True, (255, 255, 255))
        runScreen.blit(gameText2, (250, 300))


    def overlap(X, Y, i, noOfObstacles):
        for j in range(noOfObstacles):
            if j != i:
                if X[j] == X[i] and math.fabs(Y[j]-Y[i]) < 80:
                    return True
        else:
            return False


    def spaced(X, Y, i, noOfObstacles, XList):
        if overlap(X, Y, i, noOfObstacles):
            try:
                X[i] = XList[i+1]
            except:
                pass
            Y[i] -= 30
            spaced(X, Y, i, noOfObstacles, XList)
        else:
            return


    def returnButton(mouse, runScreen):
        # button
        buttonX = 300
        buttonY = 400
        color_light = (100, 100, 100)
        color_dark = (50, 50, 50)
        smallfont = pygame.font.SysFont('Corbel', 15)
        returnText = smallfont.render('return to home page', True, (255, 255, 255))
        if buttonX <= mouse[0] <= buttonX+140 and buttonY <= mouse[1] <= buttonY+40:
            pygame.draw.rect(runScreen, color_light, [buttonX, buttonY, 140, 40])
            # if event.type==pygame.MOUSEBUTTONDOWN:
            #send score not c to mysql
            #return
        else:
            pygame.draw.rect(runScreen, color_dark, [buttonX, buttonY, 140, 40])
        runScreen.blit(returnText, (buttonX+10, buttonY+10))


    def questions(X, Y, Y_change, quiz, running, level, noOfObstacles, playerX, playerY, imgList, XList, obstacleY, imgD):
        i = 1
        while i>0 and quiz:
            correct = quizScreen.main()
            if not correct:
                Y[i] = playerY
                X[i] = playerX
                Y_change = -1
                quiz = False
                running = True
            else:
                i += 1
                if i == 4:
                    i = 0
        if quiz:
            noOfObstacles = 6
            obsDicts(noOfObstacles, imgList, XList, obstacleY, X, Y, imgD)
            level += 1
            running = True
            quiz = False
        return Y_change, noOfObstacles, level, running, quiz

    obsDicts(noOfObstacles, imgList, XList, obstacleY, X, Y, imgD)

    score = 0
    level = 1
    done = False
    over = True
    c = 0
    running = True
    quiz = False
    levelChange = 1000

    while not done:

        while running:
            c += 1

            # background
            runScreen.blit(background, (0, 0))

            #title and icon
            pygame.display.set_caption("NameOfGame")
            icon = pygame.image.load('vampire.png')
            pygame.display.set_icon(icon)

            if c % levelChange == 1 and c != 1 and over:
                showlevel(level, runScreen)
                Y_change += 1

            # game over
            for i in range(noOfObstacles):
                if collide(playerX, playerY, X[i], Y[i]):
                    if over:
                        score = c
                        for j in range(noOfObstacles):
                            Y[j] = playerY
                        Y_change = 0
                    gameOver(score, runScreen)
                    over = False
                    quiz = False
                    mouse = pygame.mouse.get_pos()
                    returnButton(mouse, runScreen)

                else:
                    if Y[i] >= 640:
                        Y[i] = 0
                        X[i] = XList[random.randint(0, 3)]

                        spaced(X, Y, i, noOfObstacles, XList)

                    else:
                        Y[i] += Y_change
            # quiz runScreen
            if c % levelChange == 0 and over:
                running = False
                quiz = True

            # keyboard input
            for event in pygame.event.get():
                # action on clicking the x
                if event.type == pygame.QUIT:
                    done = True
                    running = False
                    quiz = False
                # action on pressing arrow keys
                if event.type == pygame.KEYDOWN:
                    if over:
                        if event.key == pygame.K_RIGHT:
                            if XList.index(playerX) != 3:
                                playerX = XList[XList.index(playerX)+1]
                        elif event.key == pygame.K_LEFT:
                            if XList.index(playerX) != 0:
                                playerX = XList[XList.index(playerX)-1]

            obstacle(imgD, X, Y, noOfObstacles, runScreen)
            player(playerX, playerY, runScreen, playerImg)
            pygame.display.update()

        if quiz:
            noOfObstacles = 4
            for i in range(noOfObstacles):
                X[i] = XList[i]
                Y[i] = 300

        while quiz:
            # background
            runScreen.blit(background, (0, 0))

            #title and icon
            pygame.display.set_caption("NameOfGame")
            icon = pygame.image.load('vampire.png')
            pygame.display.set_icon(icon)

            for i in range(noOfObstacles):
                Y[i] += Y_change

                if Y[i] >= 450:
                    Y_change, noOfObstacles, level, running, quiz = questions(X, Y, Y_change, quiz, running, level, noOfObstacles, playerX, playerY, imgList, XList, obstacleY, imgD)

            obstacle(imgD, X, Y, noOfObstacles, runScreen)
            player(playerX, playerY, runScreen, playerImg)
            pygame.display.update()

if __name__ == "__main__":
    run()