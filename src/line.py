import math
from vec2 import vec2


class segment:

    def __init__(self, start: vec2, end: vec2):
        self.start = start
        self.end = end

    def len(self):
        return self.get_vec().len()

    def get_vec(self):
        return self.end-self.start

    # normalized [0, 1]
    def projection_scalar(self, p: vec2):
        return (p-self.start).dot(self.get_vec()) / self.get_vec().len_squared() 

    # not normalized [0, len]
    def projection_scalar2(self, p: vec2):
        return (p-self.start).dot(self.get_vec()) / self.get_vec().len()

    def project_point(self, p: vec2):
        t = self.projection_scalar(p)
        t = max(0, min(1,t))
        return self.start + self.get_vec() * t

    def distance_to_point(self, p: vec2):
        pp = self.project_point(p)
        return (p - pp).len()

    def has_point(self, p: vec2):
        # cross(A-C, C-B) = 0
        infinite = math.isclose((self.start - p).cross(p - self.end), 0)
        segment = (
            self.start.x < p.x and p.x < self.end.x and
            self.start.y < p.y and p.y < self.end.y 
            
        ) or (
            self.start.x > p.x and p.x > self.end.x and
            self.start.y > p.y and p.y > self.end.y 
        )
        return infinite and segment

