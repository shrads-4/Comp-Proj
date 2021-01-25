import pygame as pg, time

pg.init()

password = 'Shraddha4'

font = pg.font.SysFont('Corbel', 15, bold=True)
BFONT = pg.font.SysFont('Corbel', 32, bold=True)
FONT = pg.font.SysFont('Corbel', 25, bold=True)
COLOR_INACTIVE = pg.Color(226, 226, 226)
COLOR_ACTIVE = pg.Color(74, 83, 107)


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


def textobjects(text, font):
    textsurface = font.render(text, True, (0, 0, 0))
    return textsurface, textsurface.get_rect()


def button(msg, x, y, w, h, screen):

    pg.draw.rect(screen, (255, 154, 141), (x, y, w, h))
    textsurf, textrect = textobjects(msg, FONT)
    textrect.center = ((x+(w//2)), (y+(h//2)))
    screen.blit(textsurf, textrect)


def showError(message, screen, x=200, y=600, size=25, color=(255, 0, 0)):
    start_time = time.time()
    levelfont = pg.font.SysFont('Corbel', size)
    text = levelfont.render(message, True, color)
    show = True
    while show:
        if time.time() - start_time < 1.5:
            screen.blit(text, (x, y))
        else:
            show = False
        pg.display.update()
