import pygame as pg
import os
import homepage
import time
import mysql.connector
import user_details
from functions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)

def validatePwd(username,current_pwd,new_pwd,confirm_pwd):
    con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
    if con.is_connected():
        try:
            cur = con.cursor(buffered=True)
            cur.execute('select pwd from user_dets where username = "{}"'.format(username))
            result=cur.fetchone()
            if new_pwd==confirm_pwd and current_pwd==result[0] and result:
               cur.execute('update user_dets set pwd="{}" where username="{}"'.format(new_pwd,username))
               con.commit()
               return True
            else:
                showError('Password does not match. Try Again.',screen)
                return False
        except mysql.connector.Error:
            showError('Database Issue; Please Try Later',screen)
            return False
        finally:
            con.close()
    else:
        showError('Error Connecting to Database; Please Try Later',screen)
        return False

def main(username):
    clock = pg.time.Clock()
    input_box1 = InputBox(350, 250, 140, 32)
    input_box2 = InputBox(350, 325, 140, 32)
    input_box3 = InputBox(350, 400, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3]
    done = False

    while not done:
        pg.display.set_caption("Brain Rush!")

        for box in input_boxes:
            box.update()

        screen.fill((174,214,220))

        for box in input_boxes:
            box.draw(screen)

        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()

        screen.blit(BFONT.render('Brain Rush!', True,(0,0,0)),(325,50))
        playerImg = pg.image.load('vampire.png')
        screen.blit(playerImg, (375, 125))
        pg.display.set_icon(playerImg)
        screen.blit(FONT.render('Current password', True, (0, 0, 0)),(150,250))
        screen.blit(FONT.render('New password', True, (0, 0, 0)),(150,325))
        screen.blit(FONT.render('Confirm password', True,(0,0,0)),(150,400))
        
        button('Change password',290,500,220,32,screen)
        button('Back',320,550,150,32,screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
            for box in input_boxes:
                box.handle_event(event) 

        if 510>mouse[0]>290 and 532>mouse[1]>500 and click[0]==1 and not done:
            current_pwd,new_pwd,confirm_pwd = input_boxes[0].text, input_boxes[1].text, input_boxes[2].text
            if new_pwd and confirm_pwd and current_pwd and validatePwd(username,current_pwd,new_pwd,confirm_pwd) and not done:
                showError('Password changed successfully',screen)
                done = True
                user_details.main(username)
        
        if 470>mouse[0]>320 and 582>mouse[1]>550 and click[0]==1 and not done:
            done = True
            user_details.main(username)      

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)
        

if __name__ == "__main__":
    main('user')
    pg.quit()
