import pygame,sys,pygbutton,time
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()  
screen = pygame.display.set_mode((800,640),pygame.RESIZABLE)
pygame.display.set_caption("<name/topic>")
pygame.display.flip() 
image = pygame.image.load('vampire.png')

def quiz():
    i=0
    question = pygbutton.PygButton((200,80,300,80),"<question>")
    answer1 = pygbutton.PygButton((100,260,200,30),"option1")
    answer2 = pygbutton.PygButton((100,300,200,30),"option2")
    answer3 = pygbutton.PygButton((100,340,200,30),"option3")
    answer4 = pygbutton.PygButton((100,380,200,30),"option4")

    question.draw(screen)
    answer1.draw(screen)
    answer2.draw(screen)
    answer3.draw(screen)
    answer4.draw(screen)
    '''
    buttonEvent = answer1.handleEvent(event)
    buttonEvent2= answer2.handleEvent(event)
    buttonEvent3= answer3.handleEvent(event)
    buttonEvent4= answer4.handleEvent(event)'''

    question.draw(screen)
    answer1.draw(screen)
    answer2.draw(screen)
    answer3.draw(screen)
    answer4.draw(screen)

running=True
while running:
    screen.blit(image, (400,250)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running=False

    quiz()

    pygame.display.update()
    
