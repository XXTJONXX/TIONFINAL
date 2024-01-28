
import pygame
class Mouse:
    def __init__(self, cell):
        self.cell = cell
        self.image = pygame.image.load("mouse4.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        print("MOUSE " + str(self.cell))

    def set_position(self, cell):
        self.cell = cell


