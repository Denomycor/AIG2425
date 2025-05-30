from skel import Game, Window
from car import Car
import pygame
import math


def main():
    pygame.init()

    window = Window((1920/2, 1080/2), "Test", (255,255,255))
    game = Game(window)
    car = Car(
        game,
        top_speed=220.0,
        acceleration=10.0,
        steering=math.pi*2,
        break_strenght=5.0,
        color=(0, 0, 0)
    )
    game.add_object(car)

    while(game.running):
        game.run()


if __name__ == "__main__":
    main()

