from __future__ import annotations
import pygame as pg
from typing import override
from src.sprites import Animation
from src.utils import Position, PositionCamera, Direction, GameSettings
from src.core import GameManager


class Entity:
    animation: Animation
    direction: Direction
    position: Position
    game_manager: GameManager
    
    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        # Sprite is only for debug, need to change into animations
        self.animation = Animation(
            "character/ow1.png", ["down", "left", "right", "up"], 4,
            (GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
        )
        
        self.position = Position(x, y)
        self.direction = Direction.DOWN
        self.animation.update_pos(self.position)
        self.game_manager = game_manager

    def update(self, dt: float) -> None:
        self.animation.update_pos(self.position)
        self.animation.update(dt)
        
    def draw(self, screen: pg.Surface, camera: PositionCamera) -> None:
        self.animation.draw(screen, camera)
        if GameSettings.DRAW_HITBOXES:
            self.animation.draw_hitbox(screen, camera)
        
    @staticmethod
    def _snap_to_grid(value: float) -> int:
        return round(value / GameSettings.TILE_SIZE) * GameSettings.TILE_SIZE
    
    @property
    def camera(self) -> PositionCamera:
        '''
        [TODO HACKATHON 3]
        Implement the correct algorithm of player camera
        '''
        # ambil screen size dari GameSettings dengan multiple fallbacks
        screen_w = getattr(GameSettings, "SCREEN_WIDTH",
                    getattr(GameSettings, "WINDOW_WIDTH",
                    getattr(GameSettings, "WIDTH",
                    getattr(GameSettings, "SCREEN_W",
                    getattr(GameSettings, "WINDOW_W",
                    getattr(GameSettings, "DISPLAY_WIDTH", None))))))
        screen_h = getattr(GameSettings, "SCREEN_HEIGHT",
                    getattr(GameSettings, "WINDOW_HEIGHT",
                    getattr(GameSettings, "HEIGHT",
                    getattr(GameSettings, "SCREEN_H",
                    getattr(GameSettings, "WINDOW_H",
                    getattr(GameSettings, "DISPLAY_HEIGHT", None))))))

        # camera tanpa clamp (centered on player)
        cam_x = int(self.position.x - screen_w // 2)
        cam_y = int(self.position.y - screen_h // 2)

        return PositionCamera(cam_x, cam_y)
    
        # --- screen size (pixels) dengan fallbacks ---

        # If still None, fall back to a viewport assumed from tiles (16x12 typical)
        if screen_w is None:
            # try viewport tile count
            viewport_tiles_w = getattr(GameSettings, "VIEWPORT_TILE_WIDTH", 16)
            screen_w = viewport_tiles_w * GameSettings.TILE_SIZE
        if screen_h is None:
            viewport_tiles_h = getattr(GameSettings, "VIEWPORT_TILE_HEIGHT", 16)
            screen_h = viewport_tiles_h * GameSettings.TILE_SIZE

        # --- map size (pixels) with fallbacks ---
        cur_map = getattr(self.game_manager, "current_map", None)
        if cur_map is None:
            # no map — center camera on player (safe fallback)
            cam_x = int(self.position.x - screen_w // 2)
            cam_y = int(self.position.y - screen_h // 2)
            return PositionCamera(cam_x, cam_y)

        # try common map attributes (tile counts and pixel sizes)
        map_pixel_w = None
        map_pixel_h = None

        # If map exposes width/height in pixels directly
        map_pixel_w = getattr(cur_map, "pixel_width", None) or getattr(cur_map, "width_pixels", None) or getattr(cur_map, "width_px", None)
        map_pixel_h = getattr(cur_map, "pixel_height", None) or getattr(cur_map, "height_pixels", None) or getattr(cur_map, "height_px", None)

        # If map exposes tile counts, convert to pixels
        if map_pixel_w is None:
            tiles_w = getattr(cur_map, "width", None) or getattr(cur_map, "tiles_w", None) or getattr(cur_map, "tile_width", None)
            if tiles_w is not None:
                map_pixel_w = tiles_w * GameSettings.TILE_SIZE
        if map_pixel_h is None:
            tiles_h = getattr(cur_map, "height", None) or getattr(cur_map, "tiles_h", None) or getattr(cur_map, "tile_height", None)
            if tiles_h is not None:
                map_pixel_h = tiles_h * GameSettings.TILE_SIZE

        # If still unknown, fall back to very large map so clamping is disabled
        if map_pixel_w is None:
            map_pixel_w = max(screen_w, int(self.position.x + screen_w))
        if map_pixel_h is None:
            map_pixel_h = max(screen_h, int(self.position.y + screen_h))

        # Compute camera top-left so player is centered
        cam_x = int(self.position.x - screen_w // 2)
        cam_y = int(self.position.y - screen_h // 2)

        # Clamp camera
        max_cam_x = max(0, map_pixel_w - screen_w)
        max_cam_y = max(0, map_pixel_h - screen_h)

        if cam_x < 0:
            cam_x = 0
        elif cam_x > max_cam_x:
            cam_x = max_cam_x

        if cam_y < 0:
            cam_y = 0
        elif cam_y > max_cam_y:
            cam_y = max_cam_y

        return PositionCamera(cam_x, cam_y)
        #return PositionCamera(int(self.position.x), int(self.position.y))
        
    def to_dict(self) -> dict[str, object]:
        return {
            "x": self.position.x / GameSettings.TILE_SIZE,
            "y": self.position.y / GameSettings.TILE_SIZE,
        }
        
    @classmethod
    def from_dict(cls, data: dict[str, float | int], game_manager: GameManager) -> Entity:
        x = float(data["x"])
        y = float(data["y"])
        return cls(x * GameSettings.TILE_SIZE, y * GameSettings.TILE_SIZE, game_manager)
        