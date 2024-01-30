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
        self.now_frame = 0
        self.logger = logger
        self.config = config
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.bullets = list()
        self.now_mode = "normal"

        self.bullet_cooldown = 5

        # 仮
        self.size = 30
        match character:
            case "reimu":
                # 画像取得
                pass
        # 仮
        self.character = [
            self.canvas.create_oval(
                self.x + self.size,
                self.y + self.size,
                self.x - self.size,
                self.y - self.size,
                fill="red",
            )
        ]

    def update(self, mode: str):
        self.now_frame += 1

        if mode == "normal":
            if self.now_mode == "normal":
                self.canvas.moveto(
                    self.character[0], self.x - self.size, self.y - self.size
                )
            elif self.now_mode == "special":
                self.speed = 15
                self.now_mode = "normal"
                self.canvas.delete(self.character[0])
                self.canvas.delete(self.character[1])
                self.character = list()
                self.character = [
                    self.canvas.create_oval(
                        self.x + self.size,
                        self.y + self.size,
                        self.x - self.size,
                        self.y - self.size,
                        fill="red",
                    )
                ]
        elif mode == "special":
            if self.now_mode == "special":
                self.canvas.moveto(
                    self.character[0], self.x - self.size, self.y - self.size
                )
                self.canvas.moveto(self.character[1], self.x - 10, self.y - 10)
            elif self.now_mode == "normal":
                self.speed = 5
                self.now_mode = "special"
                self.canvas.delete(self.character[0])
                self.character = list()
                self.character = [
                    self.canvas.create_oval(
                        self.x + self.size,
                        self.y + self.size,
                        self.x - self.size,
                        self.y - self.size,
                        fill="purple",
                    ),
                    self.canvas.create_oval(
                        self.x + self.size - 20,
                        self.y + self.size - 20,
                        self.x - self.size + 20,
                        self.y - self.size + 20,
                        fill="red",
                    ),
                ]

        for i, bullet in reversed(list(enumerate(self.bullets))):
            bullet.update()
            if bullet.is_out(self.canvas.winfo_width(), self.canvas.winfo_height()):
                self.canvas.delete(self.bullets[i].bullet)
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
        if self.now_frame % self.bullet_cooldown == 0:
            self.bullets.append(
                NormalBullet(self.canvas, self.x, self.y - 20, 7, 50, "red")
            )
            self.bullets.append(
                NormalBullet(self.canvas, self.x - 20, self.y, 7, 50, "red")
            )
            self.bullets.append(
                NormalBullet(self.canvas, self.x + 20, self.y, 7, 50, "red")
            )
        for c in self.character:
            self.canvas.lift(c)
