from skel import Game, Window
from car import AutoCar, ManualCar
import pygame
import math
from vec2 import vec2

from track import Track


def main():
    pygame.init()

    window = Window((1920/2, 1080/2), "Test", (255,255,255))
    game = Game(window)
    car = AutoCar(
        game,
        top_speed=160.0,
        acceleration=15.0,
        steering=math.pi*1.5,
        break_strenght=15.0,
        drag_force=10.0,
        color=(255, 0, 0)
    )
    car.debug = True
    car.pos = vec2(100, 100)

    track = Track(game, [vec2(100, 100), vec2(100, 400), vec2(400, 400), vec2(600,100), vec2(900, 100), vec2(900, 400), vec2(600, 400), vec2(400,100), vec2(100,100)], (0,0,0), 70, [car])
    car.init_sensors(track)

    game.add_object(track)
    game.add_object(car)


    while(game.running):
        game.run()


if __name__ == "__main__":
    main()

