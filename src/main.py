from skel import Game, Window
from car import Car
import pygame
import math
from vec2 import vec2

from track import Track


def main():
    pygame.init()

    window = Window((1920/2, 1080/2), "Test", (255,255,255))
    game = Game(window)
    car = Car(
        game,
        top_speed=220.0,
        acceleration=15.0,
        steering=math.pi*2,
        break_strenght=20.0,
        drag_force=5.0,
        color=(255, 0, 0)
    )
    track = Track(game, [vec2(200, 200), vec2(800, 500), vec2(700, 300)], (0,0,0), 40, [car])

    game.add_object(track)
    game.add_object(car)

    car.init_sensors(track)
    while(game.running):
        game.run()


if __name__ == "__main__":
    main()

