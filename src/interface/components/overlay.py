from __future__ import annotations
import pygame as pg
from typing import List
from .component import UIComponent


class OverlayPanel(UIComponent):
    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
        background_color=(230, 230, 230),
        border_color=(50, 50, 50),
        border_radius=16,
        border_width=4
    ):
        self.rect = pg.Rect(x, y, width, height)
        self.bg = background_color
        self.border = border_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.visible = False
        
        # list buat save child component (button, image, etc.)
        self.children: List[UIComponent] = []

    # nambah child UI component (button, image, etc.)
    def add_child(self, component: UIComponent):
        self.children.append(component)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, dt: float) -> None:
        if not self.visible:
            return

        for child in self.children:
            child.update(dt)

    def draw(self, screen: pg.Surface) -> None:
        if not self.visible:
            return

        # Gambar dark background
        dark = pg.Surface(screen.get_size())
        dark.set_alpha(150)
        dark.fill((0, 0, 0))
        screen.blit(dark, (0, 0))

        # Gambar panel
        pg.draw.rect(screen, self.bg, self.rect, border_radius=self.border_radius)
        pg.draw.rect(screen, self.border, self.rect, self.border_width, border_radius=self.border_radius)

        # Gambar semua child element
        for child in self.children:
            child.draw(screen)
