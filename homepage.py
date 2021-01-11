import pygame as pg
import os
import run
import mysql.connector
import time
import user_details
import Leaderboard
import tutorial
from functions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()


def main(username):

    clock = pg.time.Clock()
    font = pg.font.SysFont('Corbel', 60, bold=True)
    screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
    
    def showScore(username):
        con = mysql.connector.connect(host='localhost', user='root', passwd='Shraddha4', database='comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor()
                cur.execute('select high_score from user_dets where username = "{}"'.format(username))
                high_score = cur.fetchone()[0]
                bgImg = pg.image.load('QImages\\confetti.jpg')
                screen.blit(bgImg,(0,0))
                showError('High Score: '+str(high_score), screen, x=290, y=300, color = (0,0,0), size=35)
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later',screen)
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later',screen)
        return False

    def updateScore(score, username):
        con = mysql.connector.connect(host='localhost', user='root', passwd='Shraddha4', database='comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor()
                cur.execute('select high_score from user_dets where username = "{}"'.format(username))
                high_score = cur.fetchone()
                if high_score:
                    if score > high_score[0]:
                        cur.execute('update user_dets set high_score = {} where username = "{}"'.format(score, username))
                        con.commit()
                        return True
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later',screen)
            finally:
                con.close()
        else:
            showError('Error Connecting to Database; Please Try Later',screen)
            return False

    done = False
    loop = 1

    while not done:
        pg.display.set_caption("Brain Rush!")
        try:
            screen.fill((174, 214, 220))
        except:
            done = True
            continue

        if loop:
            start_time = time.time()
            show = True
            while show:
                if time.time() - start_time > 0.088:
                    show = False
            loop = 0

        bg_main = pg.image.load("QImages\\traffic_wp.jpg")
        screen.blit(bg_main,(0,0))
        
        screen.blit(font.render('Welcome to Brain Rush!!!', True, (0, 0, 0)), (75, 20))
        playerImg = pg.image.load('vampire.png')
        pg.display.set_icon(playerImg)
        screen.blit(playerImg, (370, 70))

        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        button('Start running', 300, 150, 200, 42,screen)
        button('How to play', 300, 250, 200, 42,screen)
        button('High score', 300, 350, 200, 42,screen)
        button('User details', 300, 450, 200, 42,screen)
        button('Leaderboard', 300, 550, 200, 42,screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()

        if 500 > pos[0] > 300 and 192 > pos[1] > 150 and click[0] == 1 and not done:
            score = run.run()
            if updateScore(score, username):
                try:
                    showError('New High Score!:'+str(score), screen, x=200, y=100, size=35)
                except:
                    pass
                
        if 500 > pos[0] > 300 and 292 > pos[1] > 250 and click[0] == 1 and not done:
            tutorial.main(username)
        
        if 500 > pos[0] > 300 and 392 > pos[1] > 350 and click[0] == 1 and not done:
            showScore(username)
        
        if 500 > pos[0] > 300 and 492 > pos[1] > 450 and click[0] == 1 and not done:
            screen.fill((174, 214, 220))
            done = True
            user_details.main(username)
                
        if 500 > pos[0] > 300 and 592 > pos[1] > 550 and click[0] == 1 and not done:
            Leaderboard.main(username)

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)


if __name__ == '__main__':
    main('user')
    pg.quit()
