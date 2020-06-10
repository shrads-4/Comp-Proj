import pygame

pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)

# game loop
running = True
while running:
    #background temp color
    screen.fill((255,163,249))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

    #title and icon
    pygame.display.set_caption("NameOfGame")
    icon=pygame.image.load('run.png')
    pygame.display.set_icon(icon)

