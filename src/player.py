import logging
import tkinter as tk

class Player:
    def __init__(self, logger, canvas:tk.Canvas, x, y, speed, character):
        self.logger = logger
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        match character:
            case "reimu":
                #画像取得
                pass
        #仮
        self.canvas.create
    

    def update(self):
        pass

    def move(self, dir):
        match dir:
            case 'u':
                self.y -= self.speed
            case 'd':
                self.y += self.speed
            case 'r':
                self.x += self.speed
            case 'l':
                self.x -= self.speed

        
    
