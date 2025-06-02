import pygame
from vec2 import vec2

from skel import WorldObject


class Label(WorldObject):

    def __init__(self, game, text = "", size = 20, color = (0,0,0)):
        super().__init__(game)
        self.update(text, size, color)

    def update(self, text, size, color):
        self.text = text
        self.size = size
        self.font = pygame.font.Font(None, self.size)
        self.texture = self.font.render(self.text, True, color)

    def draw(self):
        super().draw()
        self.game.window.display.blit(self.texture, self.get_global_pos().to_tuple())

