import pygame as pg, os, functions, homepage, time

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)

font=pg.font.SysFont('Corbel', 32, bold=True)

def main(username):
    done = False
    i=0
    ImgList = [pg.image.load('TutorialImages\\1.png'),pg.image.load('TutorialImages\\2.png'),pg.image.load('TutorialImages\\3.png'),pg.image.load('TutorialImages\\4.png'),pg.image.load('TutorialImages\\5.png'),pg.image.load('TutorialImages\\6.png'),pg.image.load('TutorialImages\\7.png'),pg.image.load('TutorialImages\\8.png'),pg.image.load('TutorialImages\\9.png'),pg.image.load('TutorialImages\\10.png'),pg.image.load('TutorialImages\\11.png')]
    while not done:
        pg.display.set_caption("Brain Rush!")
        screen.fill((174,214,220))
        
        bg_main = pg.image.load("QImages\\road.jpg")
        screen.blit(bg_main,(0,0))
        playerImg = pg.image.load('vampire.png')
        pg.display.set_icon(playerImg)

        screen.blit(font.render('How To Play', True,(0,0,0)),(325,40))

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

