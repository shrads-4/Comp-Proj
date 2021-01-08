import pygame as pg
import os
import time
import homepage
import mysql.connector

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

def main(username):
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
            if time.time() - start_time < 2:
                screen.blit(text, (x, y))
            else:
                show = False
            pg.display.update()

    def getscores():
        con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'compclass12', database = 'project')
        if con.is_connected():
            try:
                cur = con.cursor(buffered=True)
                cur.execute('select username,high_score from user_dets')
                result = cur.fetchall()
                x=result
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later')
                x=False
            finally:
                con.close()
                return x
        else:
            showError('Error Connecting to Database; Please Try Later')
            return False

    screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
    font1=pg.font.SysFont('Corbel',26,bold=True)
    font=pg.font.SysFont('Corbel', 32, bold=True)
    RFONT = pg.font.SysFont('Corbel', 20, bold=True)
    clock = pg.time.Clock()
    done=False
    loop = 1
    while not done:
        if loop:
            start_time = time.time()
            show = True
            while show:
                if time.time() - start_time > 0.088:
                    show = False
            loop = 0
            
        screen.fill((174, 214, 220))
        pg.display.set_caption("Brain Rush!")
        
        screen.blit(font.render('Leaderboard',True,(0,0,0)),(310,30))
        screen.blit(font.render('Username',True,(0,0,0)),(140,100))
        screen.blit(font.render('High Score',True,(0,0,0)),(510,100))
        a=getscores()
        if a:
            y=170
            for i in a:
                screen.blit(font1.render(i[0],True,(0,0,0)),(150,y))
                screen.blit(font1.render(str(i[1]),True,(0,0,0)),(530,y))
                y+=50
        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()

        button('Back',290,550,200,42)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
        
        if 520>mouse[0]>320 and 592>mouse[1]>550 and click[0]==1 and not done:
            done = True
            homepage.main(username)

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)

if __name__ == "__main__":
    main('user')
    pg.quit()

        
