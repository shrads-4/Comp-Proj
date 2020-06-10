import pygame

pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 640), pygame.RESIZABLE)

#background
background=pygame.image.load('background.png')

# game loop
running = True
while running:

    #background
    screen.blit(background,(0,0))

    #title and icon
    pygame.display.set_caption("NameOfGame")
    icon=pygame.image.load('vampire.png')
    pygame.display.set_icon(icon)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

    

