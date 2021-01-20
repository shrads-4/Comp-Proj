import pygame as pg, os, time, homepage, mysql.connector
from functions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()


def main(username):

    def getscores():
        con = mysql.connector.connect(
            host='localhost', user='root', passwd='Shraddha4', database='comp_proj')
        if con.is_connected():
            try:
                cur = con.cursor(buffered=True)
                cur.execute(
                    'select username,high_score from user_dets order by high_score desc;')
                result = cur.fetchall()
                x = result
            except mysql.connector.Error:
                showError('Database Issue; Please Try Later', screen)
                x = False
            finally:
                con.close()
                return x
        else:
            showError('Error Connecting to Database; Please Try Later', screen)
            return False

    screen = pg.display.set_mode((800, 640), pg.RESIZABLE)

    clock = pg.time.Clock()
    done = False
    loop = 1
    pg.display.set_caption("Brain Rush!")
    icon = pg.image.load('vampire.png')
    bg_main = pg.image.load("QImages\\lbpg.jpg")
    pg.display.set_icon(icon)

    while not done:

        screen.blit(bg_main, (0, 0))

        if loop:
            start_time = time.time()
            show = True
            while show:
                if time.time() - start_time > 0.088:
                    show = False
            loop = 0

        screen.blit(BFONT.render('Leaderboard', True, (0, 0, 0)), (310, 30))
        screen.blit(BFONT.render('Username', True, (0, 0, 0)), (140, 100))
        screen.blit(BFONT.render('High Score', True, (0, 0, 0)), (510, 100))
        a = getscores()
        if a:
            y = 170
            for i in a:
                screen.blit(FONT.render(i[0], True, (0, 0, 0)), (150, y))
                screen.blit(FONT.render(str(i[1]), True, (0, 0, 0)), (530, y))
                y += 50
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        button('Back', 290, 550, 200, 42, screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()

        if 520 > mouse[0] > 320 and 592 > mouse[1] > 550 and click[0] == 1 and not done:
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
