import tkinter as tk
from abc import ABC, abstractmethod
import math

from .bullet import NormalBullet


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
        self, canvas: tk.Canvas, first_x, first_y, last_x, last_y, frame, size, id
    ):
        super().__init__(canvas, first_x, first_y, size)
        self.last_x = last_x
        self.last_y = last_y
        self.frame_mag = 50 / frame
        self.bullets = list()
        self.id = id
        self.frame = frame
        self.is_first_firing = True
        self.hp = 5
        self.counts = [0 for _ in range(1, 100)]
        self.enemy = self.canvas.create_oval(
            first_x + self.size,
            first_y + self.size,
            first_x - self.size,
            first_y - self.size,
            fill="yellow",
        )

    def moveto(self, x, y):
        self.last_x = x
        self.last_y = y

    def hit(self, bullet):
        self.hp -= bullet.damage

    def update(self, player_x, player_y):
        player_dir = (
            math.degrees(math.atan((player_x - self.x) / (player_y - self.y))) + 180
        )

        self.frame += 1
        if (self.x < self.last_x + 2 and self.x > self.last_x - 2) and (
            self.x < self.last_x + 2 and self.x > self.last_x - 2
        ):
            self.x = self.last_x
            self.y = self.last_y
        self.x += (self.last_x - self.x) / 10 * self.frame_mag
        self.y += (self.last_y - self.y) / 10 * self.frame_mag
        self.canvas.moveto(self.enemy, self.x - self.size, self.y)

        if (
            round(self.x) == self.last_x
            and round(self.y) == self.last_y
            and self.hp > 0
        ):
            if self.id == 0:
                if self.is_first_firing:
                    self.is_first_firing = False
                    self.firing("circle", None, player_dir)
                if self.frame % 10 == 0 and self.counts[0] < 6:
                    self.counts[0] += 1
                    self.firing("radiation", dir=None, player_dir=player_dir)

        for i, bullet in reversed(list(enumerate(self.bullets))):
            bullet.update()
            if bullet.is_out(self.canvas.winfo_width(), self.canvas.winfo_height()):
                self.canvas.delete(self.bullets[i].bullet)
                del self.bullets[i]

        self.canvas.lift(self.enemy)

    def firing(self, mode, dir, player_dir=0):
        match mode:
            case "radiation":
                self.bullets.append(
                    NormalBullet(
                        self.canvas, self.x, self.y, 15, 5, "blue", player_dir + 15
                    )
                )
                self.bullets.append(
                    NormalBullet(
                        self.canvas, self.x, self.y, 15, 5, "blue", player_dir + 5
                    )
                )
                self.bullets.append(
                    NormalBullet(
                        self.canvas, self.x, self.y, 15, 5, "blue", player_dir - 5
                    )
                )
                self.bullets.append(
                    NormalBullet(
                        self.canvas, self.x, self.y, 15, 5, "blue", player_dir - 15
                    )
                )

            case "circle":
                dir2 = 0
                for i in range(50):
                    dir2 += 360 / 50
                    self.bullets.append(
                        NormalBullet(self.canvas, self.x, self.y, 15, 3, "blue", dir2)
                    )

            case _ as e:
                raise TypeError(f"{e}というオプションはありません")
