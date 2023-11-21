import pygame
import random

from enum import Enum


class Inputs(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class SnakeSegment():
    def __init__(self, size, pos = (0,0)):
        self.size = size
        self.pos = pos
        self.surface = self.update_surface()

    def update(self, time, next_segment):
        self.pos = next_segment.pos
    
    def update_surface(self):
        surf = pygame.Surface((self.size*0.9, self.size*0.9))
        surf.fill('White')
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)

class SnakeHead():
    def __init__(self, size, pos = (0,0)):
        self.size = size
        self.pos = pos
        self.segments = [] # youngest/furthest back segments are first in list
        self.surface = self.update_surface()
        for i in range(5):
            self.grow((0, self.size * i))

    def update(self, time, direction):
        if len(self.segments)>0: # Segments start from the back and move to the spot that the next segment is
            for i in range(len(self.segments)-1):
                self.segments[i].update(time, self.segments[i+1])
            self.segments[len(self.segments)-1].update(time, self)
        self.move(direction)

    def move(self, direction): # help from https://www.youtube.com/watch?v=AvV6UxuzH5c
        if (direction == Inputs.UP):
            self.pos = (self.pos[0], self.pos[1] - self.size)
        elif (direction == Inputs.DOWN):
            self.pos = (self.pos[0], self.pos[1] + self.size)
        elif (direction == Inputs.LEFT):
            self.pos = (self.pos[0] - self.size, self.pos[1])
        elif (direction == Inputs.RIGHT):
            self.pos = (self.pos[0] + self.size, self.pos[1])

    def grow(self, pos = (0,0)):
        self.segments.insert(0, SnakeSegment(self.size, (self.pos[0] + pos[0], self.pos[1] + pos[1])))
        print("Segment added")

    def update_surface(self):
        surf = pygame.Surface((self.size*0.9, self.size*0.9))
        surf.fill('White')
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)
        for segment in self.segments:
            segment.draw(surface)

def gather_movement_inputs(event, current_direction):
    if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_direction != Inputs.DOWN:
        return Inputs.UP
    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_direction != Inputs.UP:
        return Inputs.DOWN
    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and current_direction != Inputs.LEFT:
        return Inputs.RIGHT
    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and current_direction != Inputs.RIGHT:
        return Inputs.LEFT
    else:
        return current_direction

def main():
    pygame.init
    pygame.display.set_caption("Snake")
    resolution = (800, 600)
    tile_size = 20
    screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    deltatime = 0
    running = True
    direction = Inputs.UP
    player = SnakeHead(tile_size, (resolution[0]/2, resolution[1]/2))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                direction = gather_movement_inputs(event, direction)
        screen.fill('Black')
        player.update(deltatime, direction)
        player.draw(screen)
        pygame.display.flip()
        deltatime = clock.tick(12)
    pygame.quit()
    

if __name__ == "__main__":
    main()