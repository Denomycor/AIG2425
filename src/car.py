from sensor import RaycastSensor
from skel import WorldObject
from vec2 import vec2
import pygame
import shapes
import math
from transform import apply_transform_to_points, chain_transforms, rotation, transpose, scale


class Car(WorldObject):
    
    def __init__(self, game, *, top_speed: float, acceleration: float, steering: float, break_strenght: float, drag_force: float, color):
        super().__init__(game)
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.steering = steering
        self.break_strenght = break_strenght
        self.velocity = vec2.zero()
        self.color = color
        self.drag_force = drag_force

        self.velocity = vec2(0,0)


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


    def accelerate(self):
        direction = vec2.from_angle(self.rotation)
        self.velocity += direction * self.acceleration


    def brake(self):
        v = self.velocity.len()
        v = max(0, v-self.break_strenght)
        self.velocity = self.velocity.limit_len(v)


    def drag(self):
        v = self.velocity.len()
        v = max(0, v-self.drag_force)
        self.velocity = self.velocity.limit_len(v)


    def steer_left(self, delta):
        self.rotation += self.steering * delta


    def steer_right(self, delta):
        self.rotation -= self.steering * delta


    def manual_controls(self, delta):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_s]):
            self.brake()
        elif keys[pygame.K_w]:
            self.accelerate()

        if keys[pygame.K_d]:
            self.steer_left(delta)
        if keys[pygame.K_a]:
            self.steer_right(delta)


    def process(self, delta):
        super().process(delta)
        self.manual_controls(delta)

        self.drag()
        self.velocity = self.velocity.limit_len(self.top_speed)
        self.pos += self.velocity * delta


    def draw(self):
        super().draw()
        points = shapes.triangle()
        transform = chain_transforms(scale(vec2(10, 10)), rotation(self.rotation), transpose(self.pos))
        points2 = apply_transform_to_points(points, transform)

        f_points = [v.to_tuple() for v in points2]
        
        pygame.draw.polygon(self.game.window.display, self.color, f_points)

