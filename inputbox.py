#Code Based on https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame/46390412

from constants import COLOR
import pygame as pg

class InputBox():
    def __init__(self, x, y, w, h, screen, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.screen = screen
        self.color = COLOR['WHITE']
        self.text = text
        self.font = pg.font.SysFont(None, 18)
        self.txt_surface = self.font.render(text, True, self.color)
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
            self.color = COLOR['RED'] if self.active else COLOR['WHITE']
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = not self.active
                    self.color = COLOR['WHITE']
                    return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, COLOR['WHITE'])

    # def update(self):
    #     # Resize the box if the text is too long.
    #     width = max(40, self.txt_surface.get_width()+10)
    #     self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(self.screen, self.color, self.rect, 1)
