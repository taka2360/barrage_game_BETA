import tkinter as tk
from abc import ABC, abstractmethod


class Bullet(ABC):
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


class NormalBullet(Bullet):
    def __init__(self, canvas: tk.Canvas, x, y, size, speed):
        super().__init__(canvas, x, y, size)
        self.speed = speed

        self.bullet = self.canvas.create_oval(
            x + self.size,
            y + self.size,
            x - self.size,
            y - self.size,
            fill="red",
        )

    def update(self):
        self.y -= self.speed
        self.canvas.moveto(self.bullet, self.x - self.size, self.y)
