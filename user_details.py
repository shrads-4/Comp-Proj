import pygame as pg
import os
import time
import homepage
import loginpage
import signup
import change_pwd
import mysql.connector
from functions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()

def main(username):
    
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
                    showError('Incorrect password', screen, x=300)
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later', screen)
                return False
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later', screen)
            return False

    def delAcc(username):
        inputbox = change_pwd.InputBox(375,250,200,40)
        over = False
        while not over:
            inputbox.update()
            screen.fill((174,214,220))
            bg_main = pg.image.load("QImages\\brain.jpg")
            screen.blit(bg_main,(0,0))
            inputbox.draw(screen)
            mouse=pg.mouse.get_pos()
            click=pg.mouse.get_pressed()
            screen.blit(FONT.render('Enter Password', True,(0,0,0)),(150,260))
            button('Submit',320,350,150,32,screen)
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
            showError('Account deleted', screen, 300)
            return 'signup'
        else:
            return 'homepage'
    
    def getEmail(username):
        con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor(buffered=True)
                cur.execute('select email from user_dets where username="{}"'.format(username))
                email = cur.fetchone()[0]
                return email
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later', screen)
                return False
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later', screen)
            return False

    screen = pg.display.set_mode((800, 640), pg.RESIZABLE)

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
        bg_main = pg.image.load("QImages\\brain.jpg")
        screen.blit(bg_main,(0,0))
        pg.display.set_caption("Brain Rush!")
        icon = pg.image.load('vampire.png')
        pg.display.set_icon(icon)
    
        screen.blit(BFONT.render('Username: '+username,True,(0,0,0)),(120,50))
        email=getEmail(username)
        if email:
            screen.blit(BFONT.render('Email: '+email,True,(0,0,0)),(120,100))
        else:
            screen.blit(BFONT.render('Email: ',True,(0,0,0)),(120,100))
        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()

        button('Change password',115,250,200,42,screen)
        button('Delete account',520,250,200,42,screen)
        button('Return to homepage',300,350,250,42,screen)
        button('Logout',320,450,200,42,screen)

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
    username='user'
    main(username)
    pg.quit()
