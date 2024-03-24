from .enemy import Fairy

import tkinter as tk
import json


class EnemyScheduler:
    def __init__(self, canvas: tk.Canvas, stage_width, stage_height):
        self.canvas = canvas
        self.stage_width = stage_width
        self.stage_height = stage_height
        self.frame = 0
        self.enemies = list()
        with open("src\enemy.json", encoding="utf-8") as file:
            self.data = json.load(file)

    def update(self, player_x, player_y) -> list:

        for key, enemy in self.data.items():
            if key == "$comment":
                continue
            if self.frame == enemy["spawn_frame"]:
                match enemy["type"]:
                    case "Fairy":
                        self.enemies.append(
                            Fairy(
                                self.canvas,
                                enemy["spawn_coords"][0] * self.stage_width / 1200,
                                enemy["spawn_coords"][1] * self.stage_height / 1000,
                                enemy["size"],
                                enemy["scripts"],
                            )
                        )

        self.frame += 1

        for i, enemy in enumerate(self.enemies):
            enemy.update(player_x, player_y)
            if enemy.hp <= 0:
                self.canvas.delete(enemy.enemy)

        return self.enemies
