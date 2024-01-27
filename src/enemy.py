import tkinter as tk
from abc import ABC, abstractmethod


class Enemy(ABC):
    def __init__(self, canvas: tk.Canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size

    @abstractmethod
    def update(self):
        pass

    def is_out(self, window_width, window_height):
        if (
            self.x + self.size / 2 < 0
            or self.x - self.size / 2 > window_width
            or self.y + self.size / 2 < 0
            or self.y - self.size / 2 > window_height
        ):
            return True
        else:
            return False


class Fairy(Enemy):
    def __init__(
        self, canvas: tk.Canvas, first_x, first_y, last_x, last_y, frame, size, speed, dir
    ):
        super().__init__(canvas, first_x, first_y, size)
        self.speed = speed
        self.dir = dir
        self.enemy = self.canvas.create_oval(
            first_x + self.size,
            first_y + self.size,
            first_x - self.size,
            first_y - self.size,
            fill="yellow",
        )

    def update(self):
        self.y -= self.speed
        self.canvas.moveto(self.enemy, self.x - self.size, self.y)
