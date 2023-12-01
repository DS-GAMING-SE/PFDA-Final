import pygame
import random

from enum import Enum


class Inputs(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Food():
    def __init__(self, size, pos = (0,0)):
        self.size = size
        self.pos = pos
        self.surface = self.update_surface()
    
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill('Red')
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, (self.pos[0]*self.size, self.pos[1]*self.size))

class SnakeSegment():
    def __init__(self, size, pos = (0,0)):
        self.size = size
        self.pos = pos
        self.surface = self.update_surface()

    def update(self, time, next_segment):
        self.pos = next_segment.pos
    
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill('White')
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, (self.pos[0]*self.size, self.pos[1]*self.size))

class SnakeHead():
    def __init__(self, size, pos = (0,0)):
        self.size = size
        self.pos = pos
        self.segments = [] # youngest/furthest back segments are first in list
        self.surface = self.update_surface()
        for i in range(5):
            self.grow((self.pos[0], self.pos[1]+i))

    def update(self, time, direction, food):
        if len(self.segments)>0: # Segments start from the back and move to the spot that the next segment is
            back_pos = self.segments[0].pos
            for i in range(len(self.segments)-1):
                self.segments[i].update(time, self.segments[i+1])
            self.segments[len(self.segments)-1].update(time, self)
        self.move(direction)
        self.check_for_food(food, back_pos)

    def move(self, direction): # help from https://www.youtube.com/watch?v=AvV6UxuzH5c
        if (direction == Inputs.UP):
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif (direction == Inputs.DOWN):
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif (direction == Inputs.LEFT):
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif (direction == Inputs.RIGHT):
            self.pos = (self.pos[0] + 1, self.pos[1])

    def grow(self, pos = (0,0)):
        self.segments.insert(0, SnakeSegment(self.size, pos))
        print("Segment added")

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill('White')
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, (self.pos[0]*self.size, self.pos[1]*self.size))
        for segment in self.segments:
            segment.draw(surface)

    def check_for_food(self, food, pos):
        if self.pos == food.pos:
            self.grow(pos)
        

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
    resolution = (600, 600)
    tile_size = 20
    screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    deltatime = 0
    running = True
    direction = Inputs.UP
    player = SnakeHead(tile_size, (resolution[0]/tile_size/2, resolution[1]/tile_size/2))
    food = Food(tile_size, (3,3))
    while running:
        direction_inputted = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not direction_inputted:
                direction = gather_movement_inputs(event, direction)
                direction_inputted = True
        screen.fill('Black')
        player.update(deltatime, direction, food)
        food.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        deltatime = clock.tick(12)
    pygame.quit()
    

if __name__ == "__main__":
    main()