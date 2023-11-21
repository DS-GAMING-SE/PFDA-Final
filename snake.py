import pygame
import random

from enum import Enum


class Inputs(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class SnakeSegment():
    def __init__(self, screen_res, size, pos = (0,0)):
        self.screen_res = screen_res
        self.size = size
        self.pos = pos
        self.surface = self.update_surface()

    def update(self, time):
        return
    
    def update_surface(self):
        surf = pygame.Surface((self.size*0.9, self.size*0.9))
        surf.fill('White')
        return surf

class SnakeHead():
    def __init__(self, screen_res, size, pos = (0,0)):
        self.screen_res = screen_res
        self.size = size
        self.pos = pos
        self.segments = []
        self.surface = self.update_surface()

    def update(self, time, direction):
        for segment in self.segments:
            segment.update(time)
        if (direction == Inputs.UP):
            self.pos = (self.pos[0], self.pos[1] - self.size)
        elif (direction == Inputs.DOWN):
            self.pos = (self.pos[0], self.pos[1] + self.size)
        elif (direction == Inputs.LEFT):
            self.pos = (self.pos[0] - self.size, self.pos[1])
        elif (direction == Inputs.RIGHT):
            self.pos = (self.pos[0] + self.size, self.pos[1])

    def grow(self):
        self.segments.append(SnakeSegment(self.screen_res, self.size, self.pos))

    def update_surface(self):
        surf = pygame.Surface((self.size*0.9, self.size*0.9))
        surf.fill('White')
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)

def gather_movement_inputs(event, current_direction):
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        return Inputs.UP
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        return Inputs.DOWN
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        return Inputs.RIGHT
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        return Inputs.LEFT
    else:
        print("Movement key recognized")
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
    player = SnakeHead(resolution, tile_size, (resolution[0]/2, resolution[1]/2))
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
        deltatime = clock.tick(8)
    pygame.quit()
    

if __name__ == "__main__":
    main()