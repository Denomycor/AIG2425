import pygame


class GameObject(object):

    def __init__(self, game):
        self.game = game

    def draw(self):
        pass

    def process(self):
        pass

    def on_event(self, events):
        pass


class Game:

    def __init__(self, window):
        self.objects: list[GameObject] = []
        self.window: Window = window
        self.running = True

    def add_object(self, game_object: GameObject):
        self.objects.append(game_object)

    def remove_object(self, game_object: GameObject):
        self.objects.remove(game_object)

    def run(self):
        events = []
        for e in pygame.event.get():
            events.append(e)
            if(e.type == pygame.QUIT):
                self.running = False
                return

        for go in self.objects:
            go.on_event(events)
            go.process()
            go.draw()

        pygame.display.update()


class Window:

    def __init__(self, size, caption, color):
        self.width = size[0]
        self.height = size[1]
        self.default_color = color
        self.display = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(caption)
        self.display.fill(self.default_color)

