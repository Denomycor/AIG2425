from skel import Game, Window
from car import Car
from dataRecorder import DataRecorder  # NOVO
import pygame
import math
from vec2 import vec2
from track import Track

def main():
    pygame.init()

    window = Window((1920/2, 1080/2), "Test", (255,255,255))
    game = Game(window)

    # Criação do recorder
    recorder = DataRecorder("car_data.csv")  # NOVO

    car = Car(
        game,
        top_speed=220.0,
        acceleration=10.0,
        steering=math.pi*2,
        break_strenght=5.0,
        color=(255, 0, 0),
        recorder=recorder  
    )

    track = Track(
        game,
        [vec2(200, 200), vec2(800, 500), vec2(700, 300)],
        (0,0,0),
        40,
        [car]
    )

    game.add_object(track)
    game.add_object(car)

    car.init_sensors(track)

    while game.running:
        game.run()

    # Guardar os dados recolhidos
    recorder.save()  # NOVO

if __name__ == "__main__":
    main()