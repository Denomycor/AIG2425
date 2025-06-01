import math


# https://github.com/godotengine/godot/blob/master/core/math/vector2.cpp


class vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, rhs):
        return vec2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return vec2(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, e):
        return vec2(self.x * e, self.y * e)

    def __truediv__(self, e):
        return vec2(self.x / e, self.y / e)
    
    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, rhs) -> bool:
        return math.isclose(self.x, rhs.x) and math.isclose(self.y, rhs.y) 

    def __hash__(self):
        return hash((self.x, self.y))

    def len(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
    
    def distance_to(self, rhs):
        return abs((rhs - self).len())

    def angle(self):
        return math.atan2(self.y, self.x)

    def len_squared(self):
        return math.pow(self.x, 2) + math.pow(self.y, 2)

    def dot(self, rhs):
        return self.x * rhs.x + self.y * rhs.y

    def normalized(self):
        l = self.len_squared()
        if(l != 0):
            l = math.sqrt(l);
            return vec2(self.x / l, self.y / l)
        else:
            return vec2(0,0)

    def direction_to(self, rhs):
        return (rhs-self).normalized()

    def cross(self, rhs):
        return self.x * rhs.y - self.y * rhs.x

    def __iter__(self):
        yield self.x
        yield self.y

    @staticmethod
    def from_angle(rad):
        return vec2(math.cos(rad), math.sin(rad))

    @staticmethod
    def zero():
        return vec2(0,0)

    @staticmethod
    def one():
        return vec2(1,1)

    def to_tuple(self):
        return (self.x, self.y)

    def limit_len(self, value):
        if self.len() > value:
            return self.normalized() * value
        else:
            return self

