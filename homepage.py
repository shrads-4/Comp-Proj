import pygame as pg
pg.init()
clock = pg.time.Clock()

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
FONT = pg.font.Font(None, 42)
font=pg.font.Font(None, 30)

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
            font = pg.font.SysFont(None, 30)
            msg = font.render(text, 1, (0,0,0))
            screen.blit(msg, (self.x + (self.w / 2 - msg.get_width() / 2), self.y + (self.h / 2 - msg.get_height() / 2)))

    # Draw list of option 'calibration' and 'test'
    def draw_opt(self, win, text=[]):
        opt_list =[]
        if draw:
            for i, el in enumerate(text):
                opt_list.append(pg.draw.rect(win, self.color_option, (self.x, self.y + (i+1)*self.h, self.w, self.h), 0))

                # write each option
                font = pg.font.SysFont(None, 30)
                msg = font.render(text[i], 1, (0, 0, 0))
                screen.blit(msg, (self.x + (self.w / 2 - msg.get_width() / 2),
                                     self.y + (i+1)*self.h + (self.h / 2 - msg.get_height() / 2)))

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

def button(msg,x,y,w,h):
    
    pg.draw.rect(screen,(255,100,100),(x,y,w,h))
    textsurf,textrect=textobjects(msg,font)
    textrect.center=((x+(w//2)),(y+(h//2)))
    screen.blit(textsurf,textrect)

def textobjects(text,font):
    textsurface=font.render(text,True,(0,0,0))
    return textsurface,textsurface.get_rect()


draw=False
list1 = DropDown(COLOR_INACTIVE, COLOR_LIST_INACTIVE, 300, 450, 200, 50)


done = False

while not done:
    screen.fill(pg.Color('lightskyblue3'))
    for event in pg.event.get():
        pos=pg.mouse.get_pos()
        if event.type == pg.QUIT:
            done = True

    

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
        import run
    button('High scores',300,350,200,42)
    if 500>pos[0]>300 and 392>pos[1]>350 and click[0]==1:
        print('2')
    
    screen.blit(FONT.render('Welcome to', True,(0,0,0)),(320,50))
    screen.blit(FONT.render('<name of game>',True,(0,0,0)),(280,150))
    list1.draw_main(screen, "User details")
    list1.draw_opt(screen, ["Change password", "Delete account"])

    pg.display.flip()
    clock.tick(30)
        
'''if __name__ == '__main__':
    main()'''
pg.quit()


