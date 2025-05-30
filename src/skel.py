import pygame
from vec2 import vec2


class GameObject(object):

    def __init__(self, game):
        self.game = game
        self.objects: list[GameObject] = []

    def add_object(self, game_object):
        self.objects.append(game_object)

    def remove_object(self, game_object):
        self.objects.remove(game_object)

    def draw(self):
        for c in self.objects:
            c.draw()

    def process(self, delta):
        for c in self.objects:
            c.process(delta)

    def on_event(self, events):
        for c in self.objects:
            c.on_event(events)


class Game:

    def __init__(self, window):
        self.objects: list[GameObject] = []
        self.window: Window = window
        self.running = True
        self.clock = pygame.time.Clock()

    def add_object(self, game_object: GameObject):
        self.objects.append(game_object)

    def remove_object(self, game_object: GameObject):
        self.objects.remove(game_object)

    def run(self):
        self.window.display.fill((255, 255, 255))
        events = []
        delta = self.clock.tick(60) / 1000
        for e in pygame.event.get():
            events.append(e)
            if(e.type == pygame.QUIT):
                self.running = False
                return

        for go in self.objects:
            go.on_event(events)

        for go in self.objects:
            go.process(delta)

        for go in self.objects:
            go.draw()

        pygame.display.flip()


class Window:

    def __init__(self, size, caption, color):
        self.width = size[0]
        self.height = size[1]
        self.default_color = color
        self.display = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(caption)
        self.display.fill(self.default_color)


class WorldObject(GameObject):

    def __init__(self, game):
        super().__init__(game)
        self.pos = vec2.zero()
        self.rotation = 0
        self.scale = vec2.one()

