from skel import WorldObject
from vec2 import vec2
import pygame


class Sensor(WorldObject):

    def __init__(self, game, reach, track):
        super().__init__(game)
        self.reach = reach
        self.state = False
        self.track = track


    def target_pos(self):
        pos = self.get_global_pos()
        rot = self.get_global_rotation()

        direction = vec2.from_angle(rot)
        return pos + direction * self.reach


    def debug_draw(self):
        super().debug_draw()
        p1 = self.get_global_pos()
        p2 = self.target_pos()
        pygame.draw.line(self.game.window.display, (0,255,0) if self.state else (0,0,255), p1.to_tuple(), p2.to_tuple(), 4)


    def process(self, delta):
        super().process(delta)
        self.state = self.track.has_point(self.target_pos())

