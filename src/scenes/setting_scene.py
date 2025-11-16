'''
[TODO HACKATHON 5] 
Try to mimic the menu_scene.py or game_scene.py to create this new scene
'''
import pygame as pg

from src.utils import GameSettings, Logger
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components.overlay import OverlayPanel
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager

pg.init()

# untuk ngatur font
pg.font.init()
minecraft_font = pg.font.Font('assets/fonts/Minecraft.ttf', 24)
pokemon_font = pg.font.Font('assets/fonts/Pokemon Solid.ttf', 24)

class SettingScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")
        Logger.info("SettingScene initialized")

        # Bikin "Back" button
        px = GameSettings.SCREEN_WIDTH // 2
        py = GameSettings.SCREEN_HEIGHT // 2
        self.back_button = Button(
            "UI/button_back.png", "UI/button_back_hover.png",
            px - 50, py, 100, 100,
            lambda: scene_manager.change_scene("menu")
        )
        self.btn_back = Button(
            img_path="UI/button_back.png",
            img_hovered_path="UI/button_back_hover.png",
            x=GameSettings.SCREEN_WIDTH // 2 - 200,
            y=GameSettings.SCREEN_HEIGHT // 2 + 90,
            width=75,
            height=75,
            on_click=self.on_back_clicked
        )

        # Close button buat overlay
        self.button_x = Button(
            "UI/button_x.png", "UI/button_x_hover.png",
            x=(GameSettings.SCREEN_WIDTH // 2) + 200,
            y=(GameSettings.SCREEN_HEIGHT // 2) - 190,
            width=40,
            height=40,
            on_click=self.on_back_clicked
        )

        # Menu Button buat buka overlay (Checkpoint 2 To do 01)
        w, h = 500, 400
        x = (GameSettings.SCREEN_WIDTH - w) // 2
        y = (GameSettings.SCREEN_HEIGHT - h) // 2

        self.overlay = OverlayPanel(x, y, w, h)
        self.overlay.add_child(self.btn_back)
        self.overlay.add_child(self.button_x)
        self.overlay.show()

    def on_back_clicked(self):
        Logger.info("Back to menu clicked")
        scene_manager.change_scene("menu")

    def update(self, dt: float):
        self.btn_back.update(dt)
        self.overlay.update(dt)

    def draw(self, screen: pg.Surface):
        self.background.draw(screen)

        self.overlay.draw(screen)

        title_text = minecraft_font.render("Settings", False, (0, 0, 0))
        title_rect = title_text.get_rect(center=(GameSettings.SCREEN_WIDTH // 2 - 170, GameSettings.SCREEN_HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)