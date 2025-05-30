from skel import GameObject
import pygame


class Track(GameObject):
    
    def __init__(self, game, points, color, width):
        super().__init__(game)
        self.points = points
        self.color = color
        self.width = width
        assert len(points) > 1, "Must have more than 1 point"

    def segments(self):
        return [(self.points[i], self.points[(i + 1)]) for i in range(len(self.points)-1)]

    def draw(self):
        super().draw()
        pygame.draw.circle(self.game.window.display, self.color, self.points[0].to_tuple(), self.width//2)
        for (p1,p2) in self.segments():
            pygame.draw.line(self.game.window.display, self.color, p1.to_tuple(), p2.to_tuple(), self.width)
            pygame.draw.circle(self.game.window.display, self.color, p2.to_tuple(), self.width//2)

