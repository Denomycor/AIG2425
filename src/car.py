from car_ai import DecisionTreeWrapper
from label import Label
from sensor import RaycastSensor
from skel import WorldObject
from vec2 import vec2
from recorder import DataRecorder
import pygame
import shapes
import math
import pandas as pd
from transform import apply_transform_to_points, chain_transforms, rotation, transpose, scale



def deg_to_rad(ang):
    return ang * math.pi / 180


class AbstractCar(WorldObject):
    
    def __init__(self, game, *, top_speed: float, acceleration: float, steering: float, break_strenght: float, drag_force: float, color):
        super().__init__(game)
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.steering = steering
        self.break_strenght = break_strenght
        self.velocity = vec2.zero()
        self.color = color
        self.drag_force = drag_force

        self.sensors = []
        self.velocity = vec2(0,0)
        self.last_action = 0

        self.name = Label(game, "Toyota Corolla", color=color)
        self.add_object(self.name)
        self.name.pos = vec2(-50, -30)


    def init_sensors(self, track):
        angles = [0, 30, -30, 60, -60, 90, -90, 120, -120]
        for i in range(9):
            s = RaycastSensor(self.game, 150, track)
            s.rotation = deg_to_rad(angles[i])
            s.debug = True
            self.add_object(s)
            self.sensors.append(s)


    # Generate a list with the feature names
    def input_names(self):
        ls = []
        for i in range(len(self.sensors)):
            ls.append("s"+str(i+1)+"d")
        for i in range(len(self.sensors)):
            ls.append("s"+str(i+1)+"c")
        return ls


    # Pack sensor info with feature names
    def sensor_prediction(self, data):
        names = self.input_names()
        assert len(data) == len(names), "Incorrect len"
        dic = {}
        for i in range(len(data)):
            dic[names[i]] = data[i]
        return dic


    def accelerate(self):
        direction = vec2.from_angle(self.rotation)
        self.velocity += direction * self.acceleration
        self.last_action = self.last_action | 0x01


    def brake(self):
        v = self.velocity.len()
        v = max(0, v-self.break_strenght)
        self.velocity = self.velocity.limit_len(v)
        self.last_action = self.last_action | 0x02


    def steer_left(self, delta):
        self.rotation += self.steering * delta
        self.last_action = self.last_action | 0x04


    def steer_right(self, delta):
        self.rotation -= self.steering * delta
        self.last_action = self.last_action | 0x08


    def drag(self):
        v = self.velocity.len()
        v = max(0, v-self.drag_force)
        self.velocity = self.velocity.limit_len(v)


    def dispatch_actions(self, mask, delta):
        if(mask & 0x01):
            self.accelerate()
        if(mask & 0x02):
            self.brake()
        if(mask & 0x04):
            self.steer_left(delta)
        if(mask & 0x08):
            self.steer_right(delta)


    def manual_controls(self, delta):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_DOWN]):
            self.brake()
        elif keys[pygame.K_w]:
            self.accelerate()

        if keys[pygame.K_d]:
            self.steer_left(delta)
        if keys[pygame.K_a]:
            self.steer_right(delta)


    # Pack all sensor info into an array
    def pack_sensors(self):
       return [s.collision_distance() if s.state else -1 for s in self.sensors] + [s.state for s in self.sensors]


    def draw(self):
        super().draw()
        points = shapes.triangle()
        transform = chain_transforms(scale(vec2(10, 10)), rotation(self.rotation), transpose(self.pos))
        points2 = apply_transform_to_points(points, transform)

        f_points = [v.to_tuple() for v in points2]
        
        pygame.draw.polygon(self.game.window.display, self.color, f_points)



class ManualCar(AbstractCar):

    def __init__(self, game, *, top_speed: float, acceleration: float, steering: float, break_strenght: float, drag_force: float, color):
        super().__init__(game, top_speed=top_speed, acceleration=acceleration, steering=steering, break_strenght=break_strenght, drag_force=drag_force, color=color)


    def init_sensors(self, track):
        super().init_sensors(track)
        # self.recorder = DataRecorder("manual_drive_data.csv", self.input_names() + ["action"])


    def process(self, delta):
        super().process(delta)
        self.last_action = 0
        self.manual_controls(delta)

        self.drag()
        self.velocity = self.velocity.limit_len(self.top_speed)
        self.pos += self.velocity * delta
        # self.recorder.add_entry([str(v) for v in self.pack_sensors() + [self.last_action]])



class DTCar(AbstractCar):
    
    def __init__(self, game, *, top_speed: float, acceleration: float, steering: float, break_strenght: float, drag_force: float, color):
        super().__init__(game, top_speed=top_speed, acceleration=acceleration, steering=steering, break_strenght=break_strenght, drag_force=drag_force, color=color)
        self.wrapper = DecisionTreeWrapper("manual_drive_data.csv")
        self.model = self.wrapper.make_model()


    def process(self, delta):
        super().process(delta)
        self.last_action = 0
        inp = self.sensor_prediction(self.pack_sensors())
        out = self.model.predict(pd.DataFrame([inp]))
        self.dispatch_actions(out[0], delta)

        self.drag()
        self.velocity = self.velocity.limit_len(self.top_speed)
        self.pos += self.velocity * delta

