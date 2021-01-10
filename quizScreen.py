import pygame
import sys
import pygbutton
import time
import os
import random
import mysql.connector

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

FONT = pygame.font.SysFont('Corbel', 25, bold=True)


def quiz(event, screen, que="<question>", options=["option1", "option2", "option3", "option4"], length = 200):
    
    Q = splitQ(que)
    Qfont = pygame.font.SysFont('Corbel', 30, bold = True)
    for i in range(len(Q)):
        text = Qfont.render(Q[i], True, (0, 0, 0))
        screen.blit(text, (25,20+30*i))
    
    font = pygame.font.SysFont('Corbel', 20, bold = True)

    answer1 = pygbutton.PygButton((100, 260, length, 30), options[0], font = font, bgcolor = (174,214,220))
    answer2 = pygbutton.PygButton((100, 300, length, 30), options[1], font = font, bgcolor = (174,214,220))
    answer3 = pygbutton.PygButton((100, 340, length, 30), options[2], font = font, bgcolor = (174,214,220))
    answer4 = pygbutton.PygButton((100, 380, length, 30), options[3], font = font, bgcolor = (174,214,220))
    
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

    bg_main = pygame.image.load("QImages\\quizbg.jpg")
    screen.blit(bg_main,(0,0))

    screen.blit(FONT.render('Choose a Topic to Answer a Question and Proceed to Next Level!', True,(0,0,0)),(70,70))

    type1 = pygbutton.PygButton((300, 200, 200, 30), T[0], bgcolor=(255,154,141))
    type2 = pygbutton.PygButton((300, 300, 200, 30), T[1], bgcolor=(255,154,141))
    type3 = pygbutton.PygButton((300, 400, 200, 30), T[2], bgcolor=(255,154,141))

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
    typeList = ['Food', 'Tourism', 'History', 'Geography', 'Music', 'Wildlife', 'Sports', 'Famous']
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
            for option in options:
                if len(option)>=25:
                    length = 450
                    break
                else:
                    length = 300
            if questionType in ('Food','Tourism','Wildlife'):
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
            error_image = pygame.image.load('error.png')
            screen.blit(error_image, (350,300))
        finally:
            con.close()
    else:
        error_image = pygame.image.load('error.png')
        screen.blit(error_image, (350,300))
    
    return question, options, answer, length

def splitQ(que):
    L = que.split()
    chunks = [L[i:i+8] for i in range(0, len(L), 8)]
    que = [None]*len(chunks)
    i=0
    for l in chunks:
        que[i] = ' '.join(l)
        i+=1
    return que

def main():
    screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)
    pygame.display.set_caption("Brain Rush!")
    icon = pygame.image.load('vampire.png')
    pygame.display.set_icon(icon)
    queTypeVariable = True
    questionType = False
    T = TypeList()
    screen.fill((226,226,226))
    
    while queTypeVariable:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                return
            questionType = queType(event, screen, T)
            running = False
        if questionType:
            question, options, answer, length = dbQueData(screen, questionType)
            queTypeVariable = False
        
        try:
            pygame.display.update()
        except:
            pass
    else:
        running = True

    while running:
        
        for event in pygame.event.get():
            Q = quiz(event, screen, question, options, length = length)
            if answer == Q:
                msg = FONT.render("That is CORRECT!!!", True, (50,50,50))
                screen.blit(msg, [370, 520])
                pygame.display.flip()
                pygame.time.delay(1200)
                return True
            elif Q:
                msg = FONT.render("Oops, that is INCORRECT :(", True, (50,50,50))
                screen.blit(msg, [370, 520])
                pygame.display.flip()
                pygame.time.delay(1200)
                return False
            
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()

        try:
            pygame.display.update()
        except:
            pass


if __name__ == "__main__":
    print(main())
    pygame.quit()
