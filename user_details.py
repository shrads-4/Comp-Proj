import pygame as pg
import os
import time
import homepage

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
font=pg.font.SysFont('Corbel', 32, bold=True)
RFONT = pg.font.SysFont('Corbel', 20, bold=True)


def textobjects(text,font):
    textsurface=font.render(text,True,(0,0,0))
    return textsurface,textsurface.get_rect()

def button(msg,x,y,w,h):
    
    pg.draw.rect(screen,(255,154,141),(x,y,w,h))
    textsurf,textrect=textobjects(msg,RFONT)
    textrect.center=((x+(w//2)),(y+(h//2)))
    screen.blit(textsurf,textrect)

def showError(message, x = 200, y = 300):
    start_time = time.time()
    levelfont = pg.font.SysFont('Corbel', 25, italic = True)
    text = levelfont.render(message, True, (255,0,0))
    show = True
    while show:
        if time.time() - start_time < 3:
            screen.blit(text, (x, y))
        else:
            show = False
        pg.display.update()


def main(username,email,screen):
    clock = pg.time.Clock()
    done=False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        screen.fill((174, 214, 220))
    
        screen.blit(font.render('Username:'+username,True,(0,0,0)),(120,50))
        screen.blit(font.render('Email:'+email,True,(0,0,0)),(120,150))
        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()

        button('Change password',115,250,200,42)
        if 315>mouse[0]>115 and 292>mouse[1]>250 and click[0]==1:
            import change_pwd
            
        button('Delete account',520,250,200,42)
        if 720>mouse[0]>520 and 292>mouse[1]>250 and click[0]==1:
            #sql statement to delete from table
            showError('Account deleted', 550)
            import signup
        button('Return to homepage',300,350,250,42)
        button('Logout',320,450,200,42)
        if 520>mouse[0]>320 and 492>mouse[1]>450 and click[0]==1:
            import login
                   
        if 550>mouse[0]>300 and 392>mouse[1]>350 and click[0]==1:
            homepage.main('User1')

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)

#take username and email from sql
username='x'
email='y'
main(username,email,screen)
pg.quit()
