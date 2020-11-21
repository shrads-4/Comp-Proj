import pygame as pg
import os
import time
import homepage
import loginpage
import signup
import change_pwd
import mysql.connector

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

def main(username,email):
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
    
    def deleteAccount(username, password):
        con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor(buffered=True)
                cur.execute('select pwd from user_dets where username="{}"'.format(username))
                pwd = cur.fetchone()[0]
                if pwd == password:
                    cur.execute('delete from user_dets where username="{}"'.format(username))
                    con.commit()
                    return True
                else:
                    showError('Incorrect password',x=300)
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later')
                return False
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later')
            return False

    def delAcc(username):
        inputbox = change_pwd.InputBox(375,250,200,40)
        over = False
        while not over:
            inputbox.update()
            screen.fill((174,214,220))
            inputbox.draw(screen)
            mouse=pg.mouse.get_pos()
            click=pg.mouse.get_pressed()
            screen.blit(font.render('Enter Password', True,(0,0,0)),(150,260))
            button('Submit',320,350,150,32)
            if 470>mouse[0]>320 and 382>mouse[1]>350 and click[0]==1 and not over:
                over = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    over = True
                    return 'QUIT'
                inputbox.handle_event(event)
            try:
                pg.display.update()
            except:
                pass
        password = inputbox.text
        if deleteAccount(username, password):
            showError('Account deleted', 300)
            return 'signup'
        else:
            return 'homepage'

    screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
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
    
        screen.blit(font.render('Username:'+username,True,(0,0,0)),(120,50))
        screen.blit(font.render('Email:'+email,True,(0,0,0)),(120,150))
        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()

        button('Change password',115,250,200,42)
        button('Delete account',520,250,200,42)
        button('Return to homepage',300,350,250,42)
        button('Logout',320,450,200,42)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()

        if 315>mouse[0]>115 and 292>mouse[1]>250 and click[0]==1 and not done:
            done = True
            change_pwd.main(username)            
        
        if 720>mouse[0]>520 and 292>mouse[1]>250 and click[0]==1 and not done:  
            done = True    
            result = delAcc(username)      
            if result=='QUIT':
                pg.quit()
            elif result=='signup':
                signup.main()
            else:
                homepage.main(username)

        
        if 520>mouse[0]>320 and 492>mouse[1]>450 and click[0]==1 and not done:
            done = True
            loginpage.main()
                   
        if 550>mouse[0]>300 and 392>mouse[1]>350 and click[0]==1 and not done:
            done = True
            homepage.main(username)

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)

if __name__ == "__main__":
    username='shrads'
    email='shradp12@gmail.com'
    main(username,email)
    pg.quit()
