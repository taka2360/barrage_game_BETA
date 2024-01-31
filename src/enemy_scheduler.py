from .enemy import Fairy
import tkinter as tk


class EnemyScheduler:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.frame = 0
        self.enemies = list()

    def update(self, player_x, player_y) -> list:
        self.frame += 1

        if self.frame == 1:
            self.enemies.append(
                Fairy(
                    self.canvas,
                    first_x=0,
                    first_y=200,
                    last_x=200,
                    last_y=300,
                    frame=60,
                    size=30,
                    id=0,
                ),
            )

        for e in self.enemies:
            e.update(player_x, player_y)
            if e.hp <= 0:
                self.canvas.delete(e.enemy)

        return self.enemies
