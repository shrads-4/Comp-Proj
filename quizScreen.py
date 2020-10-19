import pygame
import sys
import pygbutton
import time
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

def quiz(event, screen, que="<question>", options=["option1", "option2", "option3", "option4"]):
    question = pygbutton.PygButton((200, 80, 300, 80), que)
    answer1 = pygbutton.PygButton((100, 260, 200, 30), options[0])
    answer2 = pygbutton.PygButton((100, 300, 200, 30), options[1])
    answer3 = pygbutton.PygButton((100, 340, 200, 30), options[2])
    answer4 = pygbutton.PygButton((100, 380, 200, 30), options[3])
    
    question.draw(screen)
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

def queType(event, screen):
    type1 = pygbutton.PygButton((250, 200, 200, 30), 'type1')
    type2 = pygbutton.PygButton((250, 300, 200, 30), 'type2')
    type3 = pygbutton.PygButton((250, 400, 200, 30), 'type3')

    type1.draw(screen)
    type2.draw(screen)
    type3.draw(screen)

    buttonEvent1 = type1.handleEvent(event)
    buttonEvent2 = type2.handleEvent(event)
    buttonEvent3 = type3.handleEvent(event)

    if 'down' in buttonEvent1:
        return 'type1'
    elif 'down' in buttonEvent2:
        return 'type2'
    elif 'down' in buttonEvent3:
        return 'type3'

def main():
    screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)
    pygame.display.set_caption("<name/topic>")
    #pygame.display.flip()
    image = pygame.image.load('vampire.png')
    options = ["option1", "option2", "option3", "option4"]
    #answer = options[random.randrange(0, 3)]
    answer = options[0]
    queTypeVariable = True
    questionType = False
    
    while queTypeVariable:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
            questionType = queType(event, screen)
            running = False
        if questionType:
            #screen.fill((174,238,238))
            screen.fill((216,191,216))
            queTypeVariable = False
        pygame.display.update()
    else:
        running = True

    while running:
        screen.blit(image, (400, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()

            Q = quiz(event, screen)
            if answer == Q:
                return True
            elif Q:
                return False

        pygame.display.update()


if __name__ == "__main__":
    print(main())
    pygame.quit()
