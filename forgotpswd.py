import pygame as pg
import os
import homepage
import time
import mysql.connector
import user_details
import loginpage
from functions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)

def validateUser(username,email,dob,newpwd):
    con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
    if con.is_connected():
        try:
            cur = con.cursor(buffered=True)
            cur.execute('select email from user_dets where username = "{}" and dob = "{}"'.format(username,dob))
            result=cur.fetchone()
            if result and email==result[0]:
               cur.execute('update user_dets set pwd="{}" where username="{}"'.format(newpwd,username)) 
               con.commit()
               return True
            else:
                showError('User information does not match. Try Again.',screen)
                return False
        except mysql.connector.Error:
            showError('Database Issue; Please Try Later',screen)
            return False
        finally:
            con.close()
    else:
        showError('Error Connecting to Database; Please Try Later',screen)
        return False

def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(470, 200, 140, 32)
    input_box2 = InputBox(470, 300, 140, 32)
    input_box3 = InputBox(470, 400, 140, 32)
    input_box4 = InputBox(470, 500, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4]
    done = False

    while not done:
        for box in input_boxes:
            box.update()

        screen.fill((174,214,220))
        pg.display.set_caption("Brain Rush!")

        for box in input_boxes:
            box.draw(screen)

        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()

        screen.blit(BFONT.render('Brain Rush!', True,(0,0,0)),(325,50))
        playerImg = pg.image.load('vampire.png')
        pg.display.set_icon(playerImg)
        screen.blit(playerImg, (375, 100))
        screen.blit(FONT.render("Username", True, (0, 0, 0)),(100,200))
        screen.blit(FONT.render('Email', True, (0, 0, 0)),(100,300))
        screen.blit(FONT.render('Date Of Birth', True,(0,0,0)),(100,400))
        screen.blit(FONT.render('New password', True,(0,0,0)),(100,500))
        
        button('Set password',300,580,175,32,screen)
        button('Back',50,580,150,32,screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
            for box in input_boxes:
                box.handle_event(event) 

        if 475>mouse[0]>300 and 612>mouse[1]>580 and click[0]==1 and not done:
            Username,Email,DOB,new_pwd = input_boxes[0].text, input_boxes[1].text, input_boxes[2].text, input_boxes[3].text
            if Username and Email and DOB and new_pwd and validateUser(Username,Email,DOB,new_pwd) and not done:
                done = True
                showError('Password has been reset',screen)
                user_details.main(Username)
                
        
        if 200>mouse[0]>50 and 612>mouse[1]>580 and click[0]==1 and not done:
            done = True
            loginpage.main()

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)
        

if __name__ == "__main__":
    main()
    pg.quit()
