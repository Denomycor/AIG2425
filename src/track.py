from pygame.math import clamp
from line import segment
from skel import GameObject
from vec2 import vec2
import pygame


class TrackCarInfo:

    def __init__(self):
        self.laps = 0
        self.distance = 0
        self.current_projected = vec2.zero()



class Track(GameObject):
    
    def __init__(self, game, points, color, width, cars):
        self.MAX_SKIP = 20
        super().__init__(game)
        self.points = points
        self.color = color
        self.width = width
        self.cars = cars
        self.len = self.track_len()
        self.carinfos = [TrackCarInfo() for _ in cars]
        for car in cars:
            self.carinfos[self.cars.index(car)].current_projected = self.track_car(car)
        assert len(points) > 1, "Must have more than 1 point"


    def segments(self):
        return [(self.points[i], self.points[(i + 1)]) for i in range(len(self.points)-1)]


    def draw(self):
        super().draw()
        pygame.draw.circle(self.game.window.display, self.color, self.points[0].to_tuple(), self.width//2)
        for (p1,p2) in self.segments():
            self.draw_line(p1, p2)
            pygame.draw.circle(self.game.window.display, self.color, p2.to_tuple(), self.width//2)

        # draw projected cars
        for car in self.cars:
            pos = self.carinfos[self.cars.index(car)].current_projected
            pygame.draw.circle(self.game.window.display, car.color, pos.to_tuple(), 4)


    def draw_line(self, p1: vec2, p2: vec2):
        dir = p1.direction_to(p2)
        normal = dir.normal_cw()
        p11 = p1 + normal*self.width/2
        p12 = p1 - normal*self.width/2
        p21 = p2 + normal*self.width/2
        p22 = p2 - normal*self.width/2
        points = [p.to_tuple() for p in [p11, p12, p22, p21]]
        pygame.draw.polygon(self.game.window.display, self.color, points)


    def process(self, delta):
        super().process(delta)
        for car in self.cars:
            self.carinfos[self.cars.index(car)].current_projected = self.track_car(car)


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


    def distance_to_track(self, point):
        acc = float('inf')
        for (p1, p2) in self.segments():
            seg = segment(p1, p2)
            dist = seg.distance_to_point(point)
            acc = dist if dist < acc else acc
        return acc


    def current_seg(self, point):
        acc = float('inf')
        candidate = segment(vec2.zero(), vec2.zero())
        for (p1, p2) in self.segments():
            seg = segment(p1, p2)
            dist = seg.distance_to_point(point)
            acc = dist if dist < acc else acc
            candidate = seg if dist < acc else candidate
        return candidate


    def has_point(self, point):
        for (p1, p2) in self.segments():
            seg = segment(p1, p2)
            if seg.distance_to_point(point) <= self.width//2:
                return True
        return False

    
    # distance of the point along the track since the start
    def distance_on_track(self, point):
        acc = 0
        for (p1, p2) in self.segments():
            seg = segment(p1,p2)
            if seg.has_point(point):
                acc += p1.distance_to(point)
                return acc
            else:
                acc += p1.distance_to(p2)
        return acc

    
    # total track len
    def track_len(self):
        acc = 0
        for (p1, p2) in self.segments():
            acc += p1.distance_to(p2)
        return acc

