from sensor import RaycastSensor, Sensor
from skel import WorldObject
from vec2 import vec2
import pygame
import shapes
import math
from transform import apply_transform_to_points, chain_transforms, rotation, transpose, scale


class Car(WorldObject):
    
    def __init__(self, game, *, top_speed: float, acceleration: float, steering: float, break_strenght: float, color, recorder):
        super().__init__(game)
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.steering = steering
        self.break_strenght = break_strenght
        self.velocity = vec2.zero()
        self.color = color

        self.pos = vec2(1920/4, 1080/4)

        self.recorder = recorder  
        self.sensors = []


    def init_sensors(self, track):
        angles = [-0.6, -0.3, 0, 0.3, 0.6]  # 5 sensores angulados
        for angle in angles:
            sensor = RaycastSensor(self.game, 100, track)
            sensor.rotation = angle
            sensor.debug = True
            self.add_object(sensor)
            self.sensors.append(sensor)
        self.debug = True


    def manual_forward(self, delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction = vec2.from_angle(self.rotation)
            self.pos += direction * self.top_speed * delta
            return "forward"
        return None

    def manual_steer(self, delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rotation += self.steering * delta
            return "right"
        elif keys[pygame.K_a]:
            self.rotation -= self.steering * delta
            return "left"
        return None


    def process(self, delta):
        super().process(delta)

        action = self.manual_steer(delta)
        forward = self.manual_forward(delta)

        # Combina ações (se virar e andar, regista como "left_forward" por ex.)
        combined_action = None
        if forward and action:
            combined_action = f"{action}_{forward}"
        elif forward:
            combined_action = forward
        elif action:
            combined_action = action

        if self.recorder and combined_action:
            distances = [sensor.distance for sensor in self.sensors]
            self.recorder.record(distances, combined_action)


    def draw(self):
        super().draw()
        points = shapes.triangle()
        transform = chain_transforms(scale(vec2(10, 10)), rotation(self.rotation), transpose(self.pos))
        points2 = apply_transform_to_points(points, transform)

        f_points = [v.to_tuple() for v in points2]
        
        pygame.draw.polygon(self.game.window.display, self.color, f_points)


class CarAI:
    pass

