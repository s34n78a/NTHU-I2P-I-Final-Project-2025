from __future__ import annotations
import pygame as pg
from .entity import Entity
from src.core.services import input_manager
from src.utils import Position, PositionCamera, GameSettings, Logger
from src.core import GameManager
import math
from typing import override

class Player(Entity):
    speed: float = 4.0 * GameSettings.TILE_SIZE
    game_manager: GameManager

    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        super().__init__(x, y, game_manager)
        self.last_teleport_pos = None # biar ga teleport terus


    # cek collision sama enemy trainers lain
    def check_collision_with_enemies(self, rect:pg.Rect) -> bool:
        for enemy in self.game_manager.current_enemy_trainers:
            enemy_rect = pg.Rect(enemy.position.x, enemy.position.y,
                                GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
            if rect.colliderect(enemy_rect):
                return True
        return False

    @override
    def update(self, dt: float) -> None:
        dis = Position(0, 0)
        '''
        [TODO HACKATHON 2]
        Calculate the distance change, and then normalize the distance
        
        [TODO HACKATHON 4]
        Check if there is collision, if so try to make the movement smooth
        Hint #1 : use entity.py _snap_to_grid function or create a similar function
        Hint #2 : Beware of glitchy teleportation, you must do
                    1. Update X
                    2. If collide, snap to grid
                    3. Update Y
                    4. If collide, snap to grid
                  instead of update both x, y, then snap to grid
        
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= ...
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += ...
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= ...
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += ...
        
        self.position = ...
        '''
        
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= 1
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += 1
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= 1
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += 1

        length = math.hypot(dis.x, dis.y)
        if length != 0:
            dis.x = dis.x / length
            dis.y = dis.y / length

        # Hitung movement dlm pixels di delta time dt
        move_x = dis.x * self.speed * dt
        move_y = dis.y * self.speed * dt

        # --- Collision handling ---
        tile_size = GameSettings.TILE_SIZE
        rect = pg.Rect(self.position.x, self.position.y, tile_size, tile_size)
        
        # buat debugging
        # Logger.debug(f"Player rect: {rect}")

        # --- Geser X axis ---
        rect.x += move_x
        if not self.game_manager.current_map.check_collision(rect) and not self.check_collision_with_enemies(rect):
            self.position.x += move_x
        else:
            # Snap to grid biar ga overlap
            if move_x > 0:
                self.position.x = rect.x // tile_size * tile_size
            elif move_x < 0:
                self.position.x = rect.x // tile_size * tile_size + tile_size

        # --- Geser Y axis ---
        rect.y += move_y
        if not self.game_manager.current_map.check_collision(rect) and not self.check_collision_with_enemies(rect):
            self.position.y += move_y
        else:
            if move_y > 0:
                self.position.y = rect.y // tile_size * tile_size
            elif move_y < 0:
                self.position.y = rect.y // tile_size * tile_size + tile_size

        # Cek teleportasi [hackathon 5]
        tp = self.game_manager.current_map.check_teleport(self.position)
        if tp and (self.last_teleport_pos is None or
        self.position.distance_to(self.last_teleport_pos) > GameSettings.TILE_SIZE):
            
            dest = tp.destination
            
            # Inget dari mana sebelum teleport
            prev_map_name = self.game_manager.current_map_key
            
            # ganti map
            self.game_manager.switch_map(dest)
            self.game_manager.try_switch_map()

            for t in self.game_manager.current_map.teleporters:
                if t.destination == prev_map_name:
                    self.position = t.pos.copy()
                    break

            self.last_teleport_pos = self.position.copy() 
            # Save teleport terakhir biar ga teleport terus

        super().update(dt)

    @override
    def draw(self, screen: pg.Surface, camera: PositionCamera) -> None:
        super().draw(screen, camera)
        
    @override
    def to_dict(self) -> dict[str, object]:
        return super().to_dict()
    
    @classmethod
    @override
    def from_dict(cls, data: dict[str, object], game_manager: GameManager) -> Player:
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, game_manager)
