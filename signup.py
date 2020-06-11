import pygame as pg


def signup_page():
    pg.init()
    screen = pg.display.set_mode((800, 640))
    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')
    FONT = pg.font.Font(None, 32)
    font=pg.font.Font(None, 20)

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

            screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(screen)

            screen.blit(FONT.render('Sign up now!', True,(0,0,0)),(370,50))
            screen.blit(FONT.render('Username',True,(0,0,0)),(220,150))
            screen.blit(FONT.render('Password', True, (0, 0, 0)),(220,250))
            screen.blit(FONT.render('Email', True,(0,0,0)),(220,350))
            screen.blit(FONT.render("Date of birth",True,(0,0,0)),(220,450))
            pg.draw.rect(screen,(255,100,100),(390,550,100,32))
            textsurface=font.render('Register',True,(0,0,0))
            textsurf,textrect=textsurface,textsurface.get_rect()
            textrect.center=(440,566)
            screen.blit(textsurf,textrect)
    
            

            pg.display.flip()
            clock.tick(30)


    if __name__ == '__main__':
        main()
        pg.quit()
signup_page()
