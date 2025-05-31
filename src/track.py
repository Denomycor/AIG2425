from line import segment
from skel import GameObject
from vec2 import vec2
import pygame


class Track(GameObject):
    
    def __init__(self, game, points, color, width, cars):
        super().__init__(game)
        self.points = points
        self.color = color
        self.width = width
        self.cars = cars
        assert len(points) > 1, "Must have more than 1 point"


    def segments(self):
        return [(self.points[i], self.points[(i + 1)]) for i in range(len(self.points)-1)]


    def draw(self):
        super().draw()
        pygame.draw.circle(self.game.window.display, self.color, self.points[0].to_tuple(), self.width//2)
        for (p1,p2) in self.segments():
            pygame.draw.line(self.game.window.display, self.color, p1.to_tuple(), p2.to_tuple(), self.width)
            pygame.draw.circle(self.game.window.display, self.color, p2.to_tuple(), self.width//2)

        # draw projected cars
        for car in self.cars:
            pos = self.track_car(car)
            pygame.draw.circle(self.game.window.display, car.color, pos.to_tuple(), 4)


    def track_car(self, car):
        point = vec2.zero()
        distance = float("inf")

        for (p1, p2) in self.segments():
            seg = segment(p1, p2)
            pp = seg.project_point(car.pos)
            dist = pp.distance_to(car.pos)
            if(dist < distance):
                distance = dist
                point = pp

        return point


    def has_point(self, point):
        for (p1, p2) in self.segments():
            seg = segment(p1, p2)
            if seg.distance_to_point(point) <= self.width//2:
                return True
        return False

