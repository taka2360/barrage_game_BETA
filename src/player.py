import logging
import tkinter as tk

class Player:
  def __init__(self, logger, canvas:tk.Canvas, x, y, character):
    self.logger = logger
    self.canvas = canvas
    self.x = x
    self.y = y
    
