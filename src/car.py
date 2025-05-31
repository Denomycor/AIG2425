from sensor import RaycastSensor, Sensor
from skel import WorldObject
from vec2 import vec2
import pygame
import shapes
import math
from transform import apply_transform_to_points, chain_transforms, rotation, transpose, scale


class Car(WorldObject):
    
    def __init__(self, game, *, top_speed: float, acceleration: float, steering: float, break_strenght: float, color):
        super().__init__(game)
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.steering = steering
        self.break_strenght = break_strenght
        self.velocity = vec2.zero()
        self.color = color

        self.pos = vec2(1920/4, 1080/4)


    def init_sensors(self, track):
        s1 = RaycastSensor(self.game, 50, track)
        s2 = RaycastSensor(self.game, 50, track)
        s3 = RaycastSensor(self.game, 50, track)
        s2.rotation = math.pi/2
        s3.rotation = -math.pi/2
        s3.debug = True
        s2.debug = True
        s1.debug = True
        self.debug = True
        self.add_object(s1)
        self.add_object(s2)
        self.add_object(s3)


    def manual_forward(self, delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction = vec2.from_angle(self.rotation)
            self.pos += direction * self.top_speed * delta


    def manual_steer(self, delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rotation += self.steering * delta
        if keys[pygame.K_a]:
            self.rotation -= self.steering * delta


    def process(self, delta):
        super().process(delta)
        self.manual_steer(delta)
        self.manual_forward(delta)


    def draw(self):
        super().draw()
        points = shapes.triangle()
        transform = chain_transforms(scale(vec2(10, 10)), rotation(self.rotation), transpose(self.pos))
        points2 = apply_transform_to_points(points, transform)

        f_points = [v.to_tuple() for v in points2]
        
        pygame.draw.polygon(self.game.window.display, self.color, f_points)


class CarAI:
    pass

