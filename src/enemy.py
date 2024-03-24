import tkinter as tk
from abc import ABC, abstractmethod
import math

from .bullet import NormalBullet
from .custom_error import *


class Enemy(ABC):
    def __init__(
        self, canvas: tk.Canvas, x: int, y: int, size: int, scripts: list
    ) -> None:
        """
        すべての敵の親クラス
        """

        self.canvas = canvas
        self.x = self.last_x = x
        self.y = self.last_y = y
        self.size = size
        self.canvas_size_adj = [canvas.winfo_depth]
        self.frame_mag = ...
        self.bullets = list()
        self.frame = 1
        self.fire_functions = list()
        self.hp = 30
        self.wait_count = 0
        self.now_script = 0
        self.scripts = self.reshape_script(scripts)

    def update(self, player_x, player_y):

        player_dir = (
            math.degrees(math.atan((player_x - self.x) / (player_y - self.y))) + 180
        )

        if len(self.scripts) > self.now_script and self.wait_count < 1:
            self.now_script += 1
            script = self.scripts[self.now_script - 1]
            match script[0]:
                case "moveto":
                    self.moveto(
                        int(script[1]["x"]),
                        int(script[1]["y"]),
                        int(script[1]["frame"]),
                    )
                case "firing":
                    self.fire_functions.append(
                        self.firing(
                            mode=script[1]["mode"],
                            dir=(
                                int(script[1]["dir"])
                                if type(script[1]["dir"]) == int
                                else player_dir
                            ),
                            column=int(script[1]["column"]),
                            column_space=int(script[1]["column_space"]),
                            row=int(script[1]["row"]),
                            row_space=int(script[1]["row_space"]),
                            speed=int(script[1]["speed"]) if "speed" in script[1].keys() else 5
                        )
                    )
                case "wait":
                    self.wait_count = int(script[1]["frame"])
        else:
            self.wait_count -= 1

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
        self.canvas.moveto(self.enemy, self.x - self.size, self.y - self.size / 2)

        for i, g in enumerate(self.fire_functions):
            try:
                next(g)
            except StopIteration:
                del self.fire_functions[i]

        for i, bullet in reversed(list(enumerate(self.bullets))):
            bullet.update()
            if bullet.is_out(self.canvas.winfo_width(), self.canvas.winfo_height()):
                self.canvas.delete(self.bullets[i].bullet)
                del self.bullets[i]

        self.canvas.lift(self.enemy)

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

    @staticmethod
    def reshape_script(scripts):
        def shaping(arg):
            args = arg[::-1]
            args = args.replace(")", "")
            args = args[::-1]
            args = args.split(", ")
            dict_args = dict()

            for a in args:
                dict_args[a.split("=")[0]] = a.split("=")[1]
            return dict_args

        reshaped_scripts = list()

        for script in scripts:
            if script.startswith("moveto("):
                args = script.replace("moveto(", "")
                dict_args = shaping(args)

                if not "frame" in dict_args.keys():
                    dict_args["frame"] = "60"
                reshaped_scripts.append(["moveto", dict_args])

            elif script.startswith("firing("):
                args = script.replace("firing(", "")
                dict_args = shaping(args)
                reshaped_scripts.append(["firing", dict_args])

            elif script.startswith("wait("):
                args = script.replace("wait(", "")
                dict_args = shaping(args)
                reshaped_scripts.append(["wait", dict_args])

            else:
                idx = script.find("(")
                raise ScriptNameError(script[:idx])

        return reshaped_scripts

    def moveto_main(self):
        if (self.x < self.last_x + 2 and self.x > self.last_x - 2) and (
            self.x < self.last_x + 2 and self.x > self.last_x - 2
        ):
            self.x = self.last_x
            self.y = self.last_y
        self.x += (self.last_x - self.x) / 10 * self.frame_mag
        self.y += (self.last_y - self.y) / 10 * self.frame_mag
        self.canvas.moveto(self.enemy, self.x - self.size, self.y)

    def moveto(self, x, y, frame):
        self.last_x = x
        self.last_y = y
        self.frame = frame
        self.frame_mag = 40 / frame

    def hit(self, bullet):
        self.hp -= bullet.damage

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
                speed = 5 if not "speed" in options.keys() else options["speed"]
                size = 15 if not "size" in options.keys() else options["size"]
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
                                    size=size,
                                    speed=speed,
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
                for _ in range(50):
                    dir2 += 360 / 50
                    self.bullets.append(
                        NormalBullet(self.canvas, self.x, self.y, 15, 3, "blue", dir2)
                    )

            case _ as e:
                raise TypeError(f"{e}というオプションはありません")

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
                speed = 5 if not "speed" in options.keys() else options["speed"]
                size = 15 if not "size" in options.keys() else options["size"]
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
                                    size=size,
                                    speed=speed,
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
                for _ in range(50):
                    dir2 += 360 / 50
                    self.bullets.append(
                        NormalBullet(self.canvas, self.x, self.y, 15, 3, "blue", dir2)
                    )

            case _ as e:
                raise TypeError(f"{e}というオプションはありません")


class Fairy(Enemy):
    def __init__(self, canvas: tk.Canvas, first_x, first_y, size, scripts):
        super().__init__(canvas, first_x, first_y, size, scripts)

        self.enemy = self.canvas.create_oval(
            first_x + self.size,
            first_y + self.size,
            first_x - self.size,
            first_y - self.size,
            fill="yellow",
        )
