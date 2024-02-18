import tkinter as tk
from abc import ABC, abstractmethod
import math

from .bullet import NormalBullet
from .custom_error import *


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
    def __init__(self, canvas: tk.Canvas, first_x, first_y, size, id, scripts):
        super().__init__(canvas, first_x, first_y, size)
        self.last_x = first_x
        self.last_y = first_y
        self.frame_mag = 1
        self.bullets = list()
        self.id = id
        self.frame = 1
        self.is_first_firing = True
        self.fire_functions = list()
        self.hp = 5
        self.counts = [0 for _ in range(1, 100)]
        self.enemy = self.canvas.create_oval(
            first_x + self.size,
            first_y + self.size,
            first_x - self.size,
            first_y - self.size,
            fill="yellow",
        )

        self.scripts = list()
        for script in scripts:
            if script.startswith("moveto("):
                args = script.replace("moveto(", "")
                args = args[::-1]
                args = args.replace(")", "")
                args = args[::-1]
                args = args.split(", ")

                for i, arg in enumerate(args):
                    args[i] = arg.split("=")

                for arg in args:
                    try:
                        int(arg)
                    except ValueError:
                        pass

                self.scripts.append(["moveto", int(args[0]), int(args[1])])

            elif script.startswith("firing("):
                pass
            else:
                idx = script.find("(")
                raise ScriptNameError(script[:idx])

    def moveto(self, x, y, frame):
        self.last_x = x
        self.last_y = y
        self.frame = frame
        self.frame_mag = 50 / frame

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

        """-----敵の発射スケジュール設定ここから-----"""

        if (
            round(self.x) == self.last_x
            and round(self.y) == self.last_y
            and self.hp > 0
        ):
            if self.id == 0:
                if self.is_first_firing:
                    self.is_first_firing = False
                    self.fire_functions.append(self.firing("circle"))
                    self.fire_functions.append(
                        self.firing(
                            "radiation",
                            dir=player_dir,
                            column=3,
                            column_space=10,
                            row=5,
                            row_space=10,
                        )
                    )

        """-----ここまで-----"""

        for i, g in enumerate(self.fire_functions):
            try:
                next(g)
            except StopIteration:
                del self.fire_functions[i]
                print("stop")

        for i, bullet in reversed(list(enumerate(self.bullets))):
            bullet.update()
            if bullet.is_out(self.canvas.winfo_width(), self.canvas.winfo_height()):
                self.canvas.delete(self.bullets[i].bullet)
                del self.bullets[i]

        self.canvas.lift(self.enemy)

    def firing(self, mode, **options):
        """
        弾を発射します。

        mode:str\n
        使えるモード:\n
            radiation\n
            指定した向きに向かって弾を発射します\n
            オプション:\n
                dir
                向きを指定します\n
                column
                縦の弾の数を指定します\n
                column_space
                縦の間隔を指定します\n
                row
                横の弾の数を指定します\n
                row_space
                横の間隔を指定します\n

        """
        match mode:
            case "radiation":
                frame = 0
                row_space = options["row_space"]
                column_space = options["column_space"]
                column = 1 if not "column" in options.keys() else options["column"]
                row = 1 if not "row" in options.keys() else options["row"]
                dir = options["dir"]
                column_count = 0
                while True:
                    if frame % row_space == 0:
                        for j in range(row):
                            self.bullets.append(
                                NormalBullet(
                                    canvas=self.canvas,
                                    x=self.x,
                                    y=self.y,
                                    size=15,
                                    speed=5,
                                    color="blue",
                                    dir=dir + column_space * row / 2 - j * column_space,
                                )
                            )
                        column_count += 1
                    if column_count == column:
                        break
                    frame += 1
                    yield

                return

            case "circle":
                dir2 = 0
                for i in range(50):
                    dir2 += 360 / 50
                    self.bullets.append(
                        NormalBullet(self.canvas, self.x, self.y, 15, 3, "blue", dir2)
                    )

            case _ as e:
                raise TypeError(f"{e}というオプションはありません")
