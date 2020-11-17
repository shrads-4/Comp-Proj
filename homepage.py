import pygame as pg
import os
import run
import mysql.connector
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

def main(username):

    clock = pg.time.Clock()

    screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
    COLOR_INACTIVE = pg.Color(226,226,226)
    COLOR_ACTIVE = pg.Color(74,83,107)
    BFONT = pg.font.SysFont('Corbel', 15, bold=True)
    font=pg.font.SysFont('Corbel', 32, bold=True)
    FONT = pg.font.SysFont('Corbel', 25, bold=True)
    COLOR_LIST_INACTIVE = (226,226,226)
    COLOR_LIST_ACTIVE = (255,154,141)

    
    def button(msg,x,y,w,h):
        
        pg.draw.rect(screen,(255,100,100),(x,y,w,h))
        textsurf,textrect=textobjects(msg,BFONT)
        textrect.center=((x+(w//2)),(y+(h//2)))
        screen.blit(textsurf,textrect)

    def textobjects(text,font):
        textsurface=FONT.render(text,True,(0,0,0))
        return textsurface,textsurface.get_rect()

    def showError(message, x = 200, y = 600, size = 25):
        start_time = time.time()
        levelfont = pg.font.SysFont('Corbel', size)
        text = levelfont.render(message, True, (255, 0, 0))
        show = True
        while show:
            if time.time() - start_time < 3:
                screen.blit(text, (x, y))
            else:
                show = False
            pg.display.update()

    def showScore(username):
        con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor()
                cur.execute('select high_score from user_dets where username = "{}"'.format(username))
                high_score = cur.fetchone()
                print(high_score[0])
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later')
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later')
        return False

    def updateScore(score, username):
        con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor()
                cur.execute('select high_score from user_dets where username = "{}"'.format(username))
                high_score = cur.fetchone()
                if high_score:
                    if score > high_score[0]:
                        cur.execute('update user_dets set high_score = {} where username = "{}"'.format(score,username))
                        con.commit()
                        showError('New High Score!:'+str(score), x=200, y = 100, size = 35)            
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later')
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later')
            return

    draw=False
    list1 = DropDown(COLOR_INACTIVE, COLOR_LIST_INACTIVE, 300, 450, 200, 50)


    done = False
    score = None

    while not done:
        screen.fill((174,214,220))
        
        if score:
            start_time = time.time()
            show = True
            while show:
                if time.time() - start_time > 0.088:
                    show = False
            score = None

        for event in pg.event.get():
            pos=pg.mouse.get_pos()
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                return
            
        click=pg.mouse.get_pressed()
        button('Start running',300,250,200,42)
        if 500>pos[0]>300 and 292>pos[1]>250 and click[0]==1:
            score = run.run()
            updateScore(score,username)
        button('High score',300,350,200,42)
        if 500>pos[0]>300 and 392>pos[1]>350 and click[0]==1:
            showScore(username)
        button('User details',300,450,200,42)
        if 500>pos[0]>300 and 492>pos[1]>450 and click[0]==1:
            screen.fill((174,214,220))
            import user_details
                            
        screen.blit(font.render('Welcome to', True,(0,0,0)),(320,50))
        screen.blit(font.render('<name of game>',True,(0,0,0)),(280,100))
        playerImg = pg.image.load('vampire.png')
        screen.blit(playerImg, (375, 150))

        pg.display.flip()
        clock.tick(30)
        
if __name__ == '__main__':
    main('User1')
    pg.quit()


