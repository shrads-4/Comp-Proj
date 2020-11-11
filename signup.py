import pygame as pg
import os
import time
import mysql.connector
import homepage

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
COLOR_INACTIVE = pg.Color(226,226,226)
COLOR_ACTIVE = pg.Color(74,83,107)
RFONT = pg.font.SysFont('Corbel', 20, bold=True)
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
           # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

def button(msg,x,y,w,h):
    
    pg.draw.rect(screen,(255,154,141),(x,y,w,h))
    textsurf,textrect=textobjects(msg,RFONT)
    textrect.center=((x+(w//2)),(y+(h//2)))
    screen.blit(textsurf,textrect)

def textobjects(text,font):
    textsurface=font.render(text,True,(0,0,0))
    return textsurface,textsurface.get_rect()
    
def showError(message, x = 200, y = 600):
    start_time = time.time()
    levelfont = pg.font.SysFont('Corbel', 25, italic = True)
    text = levelfont.render(message, True, (255,0,0))
    show = True
    while show:
        if time.time() - start_time < 3:
            screen.blit(text, (x, y))
        else:
            show = False
        pg.display.update()

def validateUsername(username, pwd, email, dob):
    con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Shraddha4', database = 'comp_proj')
    if con.is_connected():
        try:
            cur = con.cursor(buffered = 'True')
            cur.execute('select username from user_dets;')
            result = []
            for uName in cur.fetchall():
                result+=uName
            print(result)
            if username in result:
                showError('This username is taken. Enter a different one.', 150)
                return False
            else:
                if email[0] not in ('@','.') and email[-1] not in ('@','.') and '@' in email and '.' in email and email[email.index('@')+1] != '.' and len(dob)==10:
                    cur.execute('insert into user_dets values("{}","{}","{}","{}");'.format(username, pwd, email, dob))
                    con.commit()
                    showError('Registered!', 350)
                    return True
                else:
                    showError('Enter vaild email/enter date of birth in the format: YYYY-MM-DD', 75)
                    return False
        except mysql.connector.Error:
            showError('Database Issue; Please Try Later')
            return False
        finally:
            con.close()
    else:
        showError('Error Connecting to Database; Please Try Later', 100)
    return False

def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(350, 150, 140, 32)
    input_box2 = InputBox(350, 250, 140, 32)
    input_box3 = InputBox(350, 350, 140, 32)
    input_box4 = InputBox(350, 450, 140, 32)
    input_boxes = [input_box1, input_box2,input_box3,input_box4]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((174, 214, 220))
        for box in input_boxes:
            box.draw(screen)

        screen.blit(font.render('Sign up now!', True,(0,0,0)),(370,50))
        screen.blit(FONT.render('Username',True,(0,0,0)),(210,155))
        screen.blit(FONT.render('Password', True, (0,0,0)),(210,255))
        screen.blit(FONT.render('Email', True,(0,0,0)),(210,355))
        screen.blit(FONT.render('Date of birth',True,(0,0,0)),(210,455))
        
        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()
        button('Register',390,550,100,32)
        if 490>mouse[0]>390 and 582>mouse[1]>550 and click[0]==1:
            username, pwd, email, dob = input_boxes[0].text, input_boxes[1].text, input_boxes[2].text, input_boxes[3].text
            if username and pwd and email and dob and validateUsername(username, pwd, email, dob):
                done = True
                homepage.main()
            elif not username or not pwd or not dob or not email:
                showError('Please fill all fields', 300)
            
        try:
            pg.display.update()
        except:
            pass
        clock.tick(30)


main()
pg.quit()
