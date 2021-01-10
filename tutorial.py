import pygame as pg, os, functions, homepage, time

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)

font=pg.font.SysFont('Corbel', 32, bold=True)

def main(username):
    done = False
    i=0
    ImgList = [pg.image.load('TutorialImages\\homepage.png'),pg.image.load('TutorialImages\\run.png'),pg.image.load('TutorialImages\\quiz1.png'),pg.image.load('TutorialImages\\quiz2.png'),pg.image.load('TutorialImages\\gameover.png'),pg.image.load('TutorialImages\\homepage2.png'),pg.image.load('TutorialImages\\high score.png'),pg.image.load('TutorialImages\\homepage3.png'),pg.image.load('TutorialImages\\leaderboard.png'),pg.image.load('TutorialImages\\homepage4.png'),pg.image.load('TutorialImages\\userdets.png')]
    while not done:
        pg.display.set_caption("Brain Rush!")
        screen.fill((174,214,220))
        screen.blit(font.render('Brain Rush!', True,(0,0,0)),(325,50))
        icon = pg.image.load('vampire.png')
        pg.display.set_icon(icon)

        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()
        
        functions.button('Back',320,550,150,32,screen)
        functions.button('>',700,300,50,40,screen)
        functions.button('<',50,300,50,40,screen)

        screen.blit(ImgList[i],(140,80))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()

        if 470>mouse[0]>320 and 582>mouse[1]>550 and click[0]==1 and not done:
            done = True
            homepage.main(username)
        
        if 750>mouse[0]>700 and 340>mouse[1]>300 and click[0]==1 and not done:
            time.sleep(0.25)
            pg.event.wait()
            try:
                screen.blit(ImgList[i+1],(140,80))
                i+=1
            except:
                pass

        if 100>mouse[0]>50 and 340>mouse[1]>300 and click[0]==1 and not done:
            time.sleep(0.25)
            pg.event.wait()
            try:
                screen.blit(ImgList[i-1],(140,80))
                i-=1
            except:
                pass
        
        try:
            pg.display.update()
        except:
            pass

if __name__ == "__main__":
    main('User1')
    pg.quit()