import tkinter as tk
import _tkinter
import time

import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

import pyautogui as pag

window_width, window_height = pag.size()
config["Window"]["width"] = str(window_width)
config["Window"]["height"] = str(window_height)

with open("config.ini", "w") as f:
    config.write(f)

import logging

std_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs.txt", encoding="utf-8")

handlers = list()
if config.getboolean("Dev", "log_on_console"):
    handlers.append(std_handler)
if config.getboolean("Dev", "log_on_file"):
    handlers.append(file_handler)

logging.basicConfig(
    format="%(levelname)s [%(asctime)s, in %(name)s] %(message)s",
    level=config.get("Dev", "log_level"),
    handlers=handlers,
)
logger = logging.getLogger(__name__)


import keyboard

from src import *


class App:
    def __init__(self):
        self.window_width = config.getint("Window", "width")
        self.window_height = config.getint("Window", "height")
        self.fullscreen = config.getboolean("Window", "fullscreen")
        self.window = tk.Tk()
        self.window.configure(bg="black")
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        if self.fullscreen:
            # self.window.attributes("-fullscreen", True)
            pass

        self.canvas = tk.Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            borderwidth=0,
            bg="black",
        )
        self.menubar = self.canvas.create_rectangle(
            self.window_width - self.window_width / 4,
            0,
            self.window_width,
            self.window_height,
            fill="#8b0000",
        )
        self.canvas.pack()
        self.player = Player(
            logger,
            config,
            self.canvas,
            self.window_width / 4 * 3 / 2,
            self.window_height / 6 * 5,
            15,
            "a",
        )
        self.enemy_scheduler = EnemyScheduler(self.canvas)

        self.window.update()

    def update(self):
        if keyboard.is_pressed("up"):
            self.player.move("u")
        if keyboard.is_pressed("down"):
            self.player.move("d")
        if keyboard.is_pressed("right"):
            self.player.move("r")
        if keyboard.is_pressed("left"):
            self.player.move("l")

        if keyboard.is_pressed("z"):
            self.player.firing()

        if keyboard.is_pressed("shift"):
            self.player.update("special")
        else:
            self.player.update("normal")

        self.enemy_scheduler.update()

        self.window.update()


if __name__ == "__main__":
    logger.info("起動しました")
    app = App()
    MAX_FPS = config.getint("Window", "MAX_FPS")
    while True:
        try:
            app.update()
        except _tkinter.TclError:
            logger.info("ウィンドウが閉じられました")
            break
        time.sleep(1 / MAX_FPS)
