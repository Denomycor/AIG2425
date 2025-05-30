from skel import Game, Window
import pygame


def main():
    pygame.init()

    window = Window((1920/2, 1080/2), "Test", (255,255,255))
    game = Game(window)

    while(game.running):
        game.run()


if __name__ == "__main__":
    main()

