import pygame
from vec2 import vec2


class GameObject(object):

    def __init__(self, game):
        self.game = game
        self.objects: list[GameObject] = []
        self.parent: object = None
        self.debug = False

    def add_object(self, game_object):
        self.objects.append(game_object)
        game_object.parent = self

    def remove_object(self, game_object):
        game_object.parent = None
        self.objects.remove(game_object)

    def draw(self):
        for c in self.objects:
            c.draw()

    def debug_draw(self):
        for c in self.objects:
            c.debug_draw()

    def process(self, delta):
        for c in self.objects:
            c.process(delta)

    def on_event(self, events):
        for c in self.objects:
            c.on_event(events)


class Game:

    def __init__(self, window, background=False):
        self.objects: list[GameObject] = []
        self.window: Window = window
        self.running = True
        self.clock = pygame.time.Clock()
        self.background = background
        self.elapsed_time = 0

    def add_object(self, game_object: GameObject):
        self.objects.append(game_object)
        game_object.parent = self

    def remove_object(self, game_object: GameObject):
        game_object.parent = None
        self.objects.remove(game_object)

    def run(self):
        if(not self.background):
            self.window.display.fill(self.window.default_color)
        events = []
        delta = self.clock.tick(60) / 1000
        self.elapsed_time += delta
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
            if(not self.background):
                go.draw()

        for go in self.objects:
            if(go.debug and not self.background):
                go.debug_draw()

        if(not self.background):
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
        self.rotation = 0.0
        self.scale = vec2.one()

    def get_global_pos(self):
        if isinstance(self.parent, WorldObject):
            return self.pos + self.parent.get_global_pos()
        else:
            return self.pos

    def get_global_scale(self):
        if isinstance(self.parent, WorldObject):
            scale = self.parent.get_global_scale()
            return vec2(self.scale.x * scale.x, self.scale.y * scale.y)
        else:
            return self.scale

    def get_global_rotation(self):
        if isinstance(self.parent, WorldObject):
            return self.rotation + self.parent.get_global_rotation()
        else:
            return self.rotation

