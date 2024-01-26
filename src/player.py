import logging
import tkinter as tk
import configparser

from .bullet import NormalBullet


class Player:
    def __init__(
        self,
        logger: logging.Logger,
        config: configparser.ConfigParser,
        canvas: tk.Canvas,
        x: int,
        y: int,
        speed: int,
        character: str,
    ):
        self.logger = logger
        self.config = config
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.bullets = list()

        # 仮
        self.size = 20
        match character:
            case "reimu":
                # 画像取得
                pass
        # 仮
        self.character = self.canvas.create_oval(
            self.x + self.size,
            self.y + self.size,
            self.x - self.size,
            self.y - self.size,
            fill="red",
        )

    def update(self):
        self.canvas.moveto(self.character, self.x, self.y)
        for i, bullet in enumerate(self.bullets):
            bullet.update()
            if bullet.is_out(self.canvas.winfo_width(), self.canvas.winfo_height()):
                del self.bullets[i]

    def move(self, dir):
        match dir:
            case "u":
                self.y -= self.speed
            case "d":
                self.y += self.speed
            case "r":
                self.x += self.speed
            case "l":
                self.x -= self.speed

    def firing(self):
        self.bullets.append(NormalBullet(self.canvas, self.x+self.size/2, self.y, 10, 10))