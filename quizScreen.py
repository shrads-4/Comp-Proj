import pygame
import sys
import pygbutton
import time
import os
import random
import mysql.connector

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

def quiz(event, screen, que="<question>", options=["option1", "option2", "option3", "option4"]):
    
    Qfont = pygame.font.SysFont('Corbel', 30)
    text = Qfont.render(que, True, (0, 0, 0))
    screen.blit(text, (25,30))
    
    font = pygame.font.SysFont('Corbel', 20, bold = True)

    answer1 = pygbutton.PygButton((100, 260, 200, 30), options[0], font = font, bgcolor = (174,214,220))
    answer2 = pygbutton.PygButton((100, 300, 200, 30), options[1], font = font, bgcolor = (174,214,220))
    answer3 = pygbutton.PygButton((100, 340, 200, 30), options[2], font = font, bgcolor = (174,214,220))
    answer4 = pygbutton.PygButton((100, 380, 200, 30), options[3], font = font, bgcolor = (174,214,220))
    
    answer1.draw(screen)
    answer2.draw(screen)
    answer3.draw(screen)
    answer4.draw(screen)

    buttonEvent1 = answer1.handleEvent(event)
    buttonEvent2 = answer2.handleEvent(event)
    buttonEvent3 = answer3.handleEvent(event)
    buttonEvent4 = answer4.handleEvent(event)

    if 'down' in buttonEvent1:
        return options[0]
    elif 'down' in buttonEvent2:
        return options[1]
    elif 'down' in buttonEvent3:
        return options[2]
    elif 'down' in buttonEvent4:
        return options[3]

def queType(event, screen, T):

    type1 = pygbutton.PygButton((250, 200, 200, 30), T[0])
    type2 = pygbutton.PygButton((250, 300, 200, 30), T[1])
    type3 = pygbutton.PygButton((250, 400, 200, 30), T[2])

    type1.draw(screen)
    type2.draw(screen)
    type3.draw(screen)

    buttonEvent1 = type1.handleEvent(event)
    buttonEvent2 = type2.handleEvent(event)
    buttonEvent3 = type3.handleEvent(event)

    if 'down' in buttonEvent1:
        return T[0]
    elif 'down' in buttonEvent2:
        return T[1]
    elif 'down' in buttonEvent3:
        return T[2]

def TypeList():
    typeList = ['food', 'tourism', 'history', 'geography', 'music', 'wildlife', 'sports', 'famous']
    random.shuffle(typeList)
    return typeList[:3]

def dbQueData(screen, questionType):
    con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
    if con.is_connected():
        try:
            cur = con.cursor()    
            cur.execute('select min(q_no), max(q_no) from {};'.format(questionType))        
            q_range = cur.fetchall()[0]
            q_no = random.randrange(int(q_range[0]),int(q_range[1]))
            cur.execute('select question from {} where q_no = {};'.format(questionType, q_no))
            question = cur.fetchone()[0]
            cur.execute('select * from {} where name = {};'.format(questionType+'_options', q_no))
            options = list(cur.fetchone())[1:]
            answer = options[0]
            random.shuffle(options)
            if questionType in ('food','tourism'):
                cur.execute('select link from {} where q_no = {};'.format(questionType, q_no))
                link = cur.fetchone()[0]
                if link:
                    image = pygame.image.load(link)
                    screen.blit(image,(0,0))
                else:
                    bg = pygame.image.load("QImages\\background.png")
                    screen.blit(bg,(0,0))
            else:
                bg = pygame.image.load("QImages\\background.png")
                screen.blit(bg,(0,0))
        except mysql.connector.Error:
            error_image = pygame.image.load('traffic-sign.png')
            screen.blit(error_image, (350,300))
        finally:
            con.close()
    else:
        error_image = pygame.image.load('traffic-sign.png')
        screen.blit(error_image, (350,300))
    
    return question, options, answer

def main():
    screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)
    pygame.display.set_caption("<name/topic>")
    queTypeVariable = True
    questionType = False
    T = TypeList()
    screen.fill((226,226,226))
    
    while queTypeVariable:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
            questionType = queType(event, screen, T)
            running = False
        if questionType:
            question, options, answer = dbQueData(screen, questionType)
            queTypeVariable = False
        pygame.display.update()
    else:
        running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()

            Q = quiz(event, screen, question, options)
            if answer == Q:
                return True
            elif Q:
                return False

        pygame.display.update()


if __name__ == "__main__":
    print(main())
    pygame.quit()
