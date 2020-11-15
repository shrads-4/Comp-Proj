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

    class DropDown():
        # Test List
        option_list = ["Change password", "Delete account"]

        def __init__(self, color_menu, color_option, x, y, w, h):
            self.color_menu = color_menu
            self.color_option = color_option
            self.x = x
            self.y = y
            self.w = w
            self.h = h

        # Draw the initial button 'select mode'
        def draw_main(self, win, text=''):
            pg.draw.rect(win, self.color_menu, (self.x, self.y, self.w, self.h), 0)
            if text != '':
                msg = FONT.render(text, 1, (0,0,0))
                screen.blit(msg, (self.x + (self.w // 2 - msg.get_width() // 2), self.y + (self.h // 2 - msg.get_height() // 2)))

        # Draw list of option 'calibration' and 'test'
        def draw_opt(self, win, text=[]):
            opt_list =[]
            if draw:
                for i, el in enumerate(text):
                    opt_list.append(pg.draw.rect(win, self.color_option, (self.x, self.y + (i+1)*self.h, self.w, self.h), 0))

                    # write each option
                    msg = FONT.render(text[i], 1, (0, 0, 0))
                    screen.blit(msg, (self.x + (self.w // 2 - msg.get_width() // 2),
                                        self.y + (i+1)*self.h + (self.h // 2 - msg.get_height() // 2)))

        # Detect when the mouse is within the 'select mode' box
        def choose_main(self, pos):
            if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
                return True
            else:
                return False
        # Detect when the mouse is within the option list
        def choose_opt(self, pos):
            if self.x < pos[0] < self.x + self.w and 2*self.y < pos[1] < 2*self.y + self.h:
                return True
            else:
                return False

    class InputBox:

        def __init__(self, x, y, w, h, text=''):
            self.rect = pg.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.txt_surface = font.render(text, True, self.color)
            self.active = False

        def handle_event(self, event):
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        self.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.txt_surface = font.render(self.text, True, self.color)

        def update(self):
            width = max(200, self.txt_surface.get_width()+10)
            self.rect.w = width

        def draw(self, screen):
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            pg.draw.rect(screen, self.color, self.rect, 2)

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

            #for menu
            if event.type == pg.MOUSEMOTION:
                if list1.choose_main(pos):
                    list1.color_menu = COLOR_ACTIVE

                else:
                    list1.color_menu = COLOR_INACTIVE

            #for options
            if event.type == pg.MOUSEMOTION:
                if list1.choose_opt(pos):
                    list1.color_option = COLOR_LIST_ACTIVE
                else:
                    list1.color_option = COLOR_LIST_INACTIVE

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and list1.choose_main(pos):
                    if draw == False:
                        draw = True

                    elif draw == True:
                        draw = False

            
        click=pg.mouse.get_pressed()
        button('Start running',300,250,200,42)
        if 500>pos[0]>300 and 292>pos[1]>250 and click[0]==1:
            score = run.run()
            updateScore(score,username)
        button('High score',300,350,200,42)
        if 500>pos[0]>300 and 392>pos[1]>350 and click[0]==1:
            showScore(username)
        screen.blit(font.render('Welcome to', True,(0,0,0)),(320,50))
        screen.blit(font.render('<name of game>',True,(0,0,0)),(280,150))
        list1.draw_main(screen, "User details")
        list1.draw_opt(screen, ["Change password", "Delete account"])

        pg.display.flip()
        clock.tick(30)
        
if __name__ == '__main__':
    main('User1')
    pg.quit()


