from .enemy import Fairy
import tkinter as tk


class EnemyScheduler:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.frame = 0
        self.enemies = list()

    def update(self) -> list:
        self.frame += 1

        if self.frame == 180:
            self.enemies.append([Fairy(self.canvas, 0, 300, 1000, 500, 120, 30), 0])

        for e in self.enemies:
            e[0].update()
            e[1] += 1


        return self.enemies
