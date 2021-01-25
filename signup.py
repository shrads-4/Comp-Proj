import pygame as pg, os, time, mysql.connector, homepage
from functions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)


def validateUsername(username, pwd, email, dob):
    con = mysql.connector.connect(
        host='localhost', user='root', passwd=password, database='brain_rush')
    if con.is_connected():
        try:
            cur = con.cursor(buffered='True')
            cur.execute('select username from user_dets;')
            result = []
            for uName in cur.fetchall():
                result += uName
            if username in result:
                showError(
                    'This username is taken. Enter a different one.', screen, 150)
                return False
            else:
                if email[0] not in ('@', '.') and email[-1] not in ('@', '.') and '@' in email and '.' in email and email[email.index('@')+1] != '.' and len(dob) == 10 and '/' not in dob:
                    cur.execute('insert into user_dets values("{}","{}","{}","{}",0);'.format(
                        username, pwd, email, dob))
                    con.commit()
                    showError('Registered!', screen, 350)
                    return True
                else:
                    showError(
                        'Enter vaild email/enter date of birth in the format: YYYY-MM-DD', screen, 75)
                    return False
        except mysql.connector.Error:
            showError('Database Issue; Please Try Later', screen)
            return False
        finally:
            con.close()
    else:
        showError('Error Connecting to Database; Please Try Later', screen, 100)
    return False


def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(350, 150, 140, 32)
    input_box2 = InputBox(350, 250, 140, 32)
    input_box3 = InputBox(350, 350, 140, 32)
    input_box4 = InputBox(350, 450, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4]
    done = False
    bg_main = pg.image.load("QImages\\road.jpg")
    icon = pg.image.load('vampire.png')
    pg.display.set_caption("Brain Rush!")
    pg.display.set_icon(icon)

    while not done:

        screen.blit(bg_main, (0, 0))

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)

        screen.blit(BFONT.render('Sign up now!', True, (0, 0, 0)), (370, 50))
        screen.blit(FONT.render('Username', True, (0, 0, 0)), (210, 155))
        screen.blit(FONT.render('Password', True, (0, 0, 0)), (210, 255))
        screen.blit(FONT.render('Email', True, (0, 0, 0)), (210, 355))
        screen.blit(FONT.render('Date of birth', True, (0, 0, 0)), (210, 455))
        screen.blit(FONT.render('(YYYY-MM-DD)', True, (0, 0, 0)), (555, 455))

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        button('Register', 375, 550, 150, 32, screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
            for box in input_boxes:
                box.handle_event(event)

        if 525 > mouse[0] > 375 and 582 > mouse[1] > 550 and click[0] == 1 and not done:
            username, pwd, email, dob = input_boxes[0].text, input_boxes[
                1].text, input_boxes[2].text, input_boxes[3].text
            if username and pwd and email and dob and validateUsername(username, pwd, email, dob):
                done = True
                homepage.main(username)
            elif not username or not pwd or not dob or not email:
                showError('Please fill all fields', screen, 300)

        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)


if __name__ == "__main__":
    main()
    pg.quit()
