import pygame as pg
#import signup
#from signup import signup_page
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode((800, 640), pg.RESIZABLE)
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
font=pg.font.Font(None, 20)
red=(255,0,0)
shadow=(192,192,192)

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
    textsurface=font.render(text,True,(0,0,0))
    return textsurface,textsurface.get_rect()

def button(msg,x,y,w,h):
    
    pg.draw.rect(screen,(255,100,100),(x,y,w,h))
    textsurf,textrect=textobjects(msg,font)
    textrect.center=((x+(w//2)),(y+(h//2)))
    screen.blit(textsurf,textrect)
    
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

        screen.fill(shadow)
        for box in input_boxes:
            box.draw(screen)

        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()
        button('Login',390,450,100,32)
        if 490>mouse[0]>390 and 482>mouse[1]>450 and click[0]==1:
            print('1')
        button('Sign up!',270,540,100,32)
        if 370>mouse[0]>270 and 572>mouse[1]>540 and click[0]==1:
            import signup
        button('Forgot password?',520,540,150,32)
        if 670>mouse[0]>520 and 572>mouse[1]>540 and click[0]==1:
            print('3')
        
        screen.blit(FONT.render('<nameofgame>', True,(0,0,0)),(300,50))
        screen.blit(FONT.render('<tagline>',True,(0,0,0)),(420,150))
        screen.blit(FONT.render('Username', True, (0, 0, 0)),(220,250))
        screen.blit(FONT.render('Password', True,(0,0,0)),(220,350))
        screen.blit(font.render("Don't have an account? ",True,(0,0,0)),(120,550))

        pg.display.flip()
        clock.tick(30)
        
if __name__ == '__main__':
    main()
    pg.quit()
