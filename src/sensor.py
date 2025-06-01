from skel import WorldObject
from vec2 import vec2
import pygame
from line import segment


class Sensor(WorldObject):

    def __init__(self, game):
        super().__init__(game)
        self.state = False


class PointSensor(Sensor):

    def __init__(self, game, reach, track):
        super().__init__(game)
        self.reach = reach
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


# https://en.wikipedia.org/wiki/Ray_marching
class RaycastSensor(Sensor):
    
    def __init__(self, game, reach, track):
        super().__init__(game)
        self.reach = reach
        self.track = track
        self.collision_point = vec2(0,0)
        self.epsilon = 0.1
        self.distance = self.reach  # valor inicial caso não haja colisão


    def sdf(self, point) -> float:
        min_signed_dist = float('inf')
        for (p1, p2) in self.track.segments():
            seg = segment(p1, p2)
            dist_to_center = seg.distance_to_point(point)
            signed_dist = dist_to_center - (self.track.width / 2)
            min_signed_dist = min(min_signed_dist, signed_dist)
        
        # we invert the sign to make everything but the track shape the obstacle
        return -min_signed_dist


    def process(self, delta):
        super().process(delta)
        self.raymarch()


    def debug_draw(self):
        super().debug_draw()
        p1 = self.get_global_pos()
        p2 = self.collision_point if self.state else self.target_pos()
        pygame.draw.line(self.game.window.display, (0,255,0) if self.state else (0,0,255), p1.to_tuple(), p2.to_tuple(), 4)


    def target_pos(self):
        pos = self.get_global_pos()
        rot = self.get_global_rotation()

        direction = vec2.from_angle(rot)
        return pos + direction * self.reach


    def raymarch(self):
        pos = self.get_global_pos()
        rot = self.get_global_rotation()

        direction = vec2.from_angle(rot)
        acc = 0
        i = 0
        while acc < self.reach:
            i += 1
            if i > 100:
                self.state = False
                self.distance = self.reach  # sem colisão, distância máxima
                return

            point = pos + direction * acc
            dist = self.sdf(point)
            if dist <= self.epsilon:
                self.state = True
                self.collision_point = point
                self.distance = acc  # <--- Aqui guardamos a distância
                return
            else:
                acc += dist

        self.state = False
        self.distance = self.reach  # sem colisão
        return

