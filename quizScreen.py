import pygame
import sys
import pygbutton
import time
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)
pygame.display.set_caption("<name/topic>")
pygame.display.flip()
image = pygame.image.load('vampire.png')


def quiz(event, que="<question>", options=["option1", "option2", "option3", "option4"]):
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

    question.draw(screen)
    answer1.draw(screen)
    answer2.draw(screen)
    answer3.draw(screen)
    answer4.draw(screen)

    if 'down' in buttonEvent1:
        return options[0]
    elif 'down' in buttonEvent2:
        return options[1]
    elif 'down' in buttonEvent3:
        return options[2]
    elif 'down' in buttonEvent4:
        return options[3]


def main():
    options = ["option1", "option2", "option3", "option4"]
    answer = options[random.randrange(0, 3)]
    running = True
    while running:
        screen.blit(image, (400, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()

            Q = quiz(event)
            if answer == Q:
                return True
            elif Q:
                return False

        pygame.display.update()


if __name__ == "__main__":
    print(main())
    pygame.quit()
