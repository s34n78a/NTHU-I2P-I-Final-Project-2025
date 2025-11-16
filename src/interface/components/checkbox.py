import pygame as pg

class Checkbox:
    def __init__(self, x, y, checked=False, label=""):
        self.x = x
        self.y = y
        self.size = 24
        self.checked = checked
        self.label = label
        self.font = pg.font.Font('assets/fonts/Minecraft.ttf', 20)

        self.rect = pg.Rect(x, y, self.size, self.size)

    def update(self, dt):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse) and click:
            self.checked = not self.checked

    def draw(self, screen):
        # Checkbox square
        pg.draw.rect(screen, (0, 0, 0), self.rect, 3)

        if self.checked:
            pg.draw.rect(screen, (0, 0, 0), self.rect.inflate(-8, -8))

        # Label
        txt = self.font.render(self.label, True, (0, 0, 0))
        screen.blit(txt, (self.x + 35, self.y - 2))

    def is_checked(self):
        return self.checked
