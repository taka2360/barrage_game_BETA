import tkinter as tk
import time
import logging

std_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs.txt", encoding='utf-8')
logging.basicConfig(
    format="%(levelname)s [%(asctime)s, in %(name)s] %(message)s",
    level=logging.DEBUG,
    handlers=[std_handler, file_handler],
)
logger = logging.getLogger(__name__)

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

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
            self.window.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(
            self.window, width=self.window_width, height=self.window_height, relief=tk.FLAT, bd=0, bg="black"
        )
        self.canvas.pack()
        self.window.update()

    def update(self):
        self.window.update()


if __name__ == "__main__":
    logger.info("起動しました")
    app = App()
    MAX_FPS = config.getint("Window", "MAX_FPS")
    while True:
        app.update()
        time.sleep(1 / MAX_FPS)
