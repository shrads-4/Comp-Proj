import pygame as pg
import os
import homepage
import time
import mysql.connector

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
COLOR_INACTIVE = pg.Color(226,226,226)
COLOR_ACTIVE = pg.Color(74,83,107)
BFONT = pg.font.SysFont('Corbel', 15, bold=True)
font=pg.font.SysFont('Corbel', 32, bold=True)
FONT = pg.font.SysFont('Corbel', 25, bold=True)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
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
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

def textobjects(text,font):
    textsurface=BFONT.render(text,True,(0,0,0))
    return textsurface,textsurface.get_rect()

def button(msg,x,y,w,h):
    
    pg.draw.rect(screen,(255,154,141),(x,y,w,h))
    textsurf,textrect=textobjects(msg,font)
    textrect.center=((x+(w//2)),(y+(h//2)))
    screen.blit(textsurf,textrect)
    
def showError(message):
    start_time = time.time()
    levelfont = pg.font.SysFont('Corbel', 25)
    text = levelfont.render(message, True, (255, 0, 0))
    show = True
    while show:
        if time.time() - start_time < 3:
            screen.blit(text, (200, 600))
        else:
            show = False
        pg.display.update()

def validatePwd(username,new_pwd,confirm_pwd):
    con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
    if con.is_connected():
        try:
            cur = con.cursor()
            cur.execute('select pwd from user_dets where username = "{}"'.format(username))
            if new_pwd==confirm_pwd:
               cur.execute('update user_dets set pwd="{}" where username="{}"'.format(new_pwd,username))
               return True
            else:
                showError('Password does not match. Try Again.')
                return False
        except mysql.connector.Error:
            showError('Database Issue; Please Try Later')
            return False
        finally:
            con.close()
    else:
        showError('Error Connecting to Database; Please Try Later')
        return False

def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(350, 250, 140, 32)
    input_box2 = InputBox(350, 350, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((174,214,220))
        for box in input_boxes:
            box.draw(screen)

        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()
        
        button('Change password',320,450,150,32)
        if 470>mouse[0]>320 and 482>mouse[1]>450 and click[0]==1:
            new_pwd,confirm_pwd = input_boxes[0].text, input_boxes[1].text
            if new_pwd and confirm_pwd and validatePwd(username,new_pwd,confirm_pwd):
                showError('Password changed successfully')
                import user_details
        button('Back',320,550,150,32)
        if 470>mouse[0]>320 and 582>mouse[1]>550 and click[0]==1:
            import user_details
        screen.blit(font.render('<nameofgame>', True,(0,0,0)),(300,50))
        playerImg = pg.image.load('vampire.png')
        screen.blit(playerImg, (375, 100))
        screen.blit(FONT.render('New password', True, (0, 0, 0)),(150,250))
        screen.blit(FONT.render('Confirm password', True,(0,0,0)),(150,350))
        

        pg.display.flip()
        clock.tick(30)
        

main()
pg.quit()
