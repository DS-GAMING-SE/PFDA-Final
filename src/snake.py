import pygame
import random

from enum import Enum


class Inputs(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Explosion():
    def __init__(self, tile_size, size, pos = (0,0)):
        self.tile_size = tile_size
        self.size = size
        self.pos = pos
        self.color = pygame.Color(255, 255, 255)
        self.alpha = 255
        self.explode_timer = 0
        self.explode_time = 400
        self.dead = False
        self.surface = self.update_surface()

    def update(self, time):
        self.explode_timer += time
        if self.explode_timer>self.explode_time:
            self.dead = True
        self.alpha = 255 * (1-(self.explode_timer / self.explode_time))
        self.size = self.size * (1 + (self.explode_timer / self.explode_time))
    
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        if self.dead:
            return
        self.surface.set_alpha(self.alpha)
        pos = ((self.pos[0]*self.tile_size)+(self.tile_size-self.size)/2, (self.pos[1]*self.tile_size)+(self.tile_size-self.size)/2)
        rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        surface.blit(self.surface, pos)
        pygame.draw.rect(self.surface, self.color, rect)

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

    def eaten(self, segments):
        occupied = True
        while occupied:
            print("Food Occupy Check")
            new_pos = (random.randrange(0,29), random.randrange(0,29))
            occupied = new_pos == self.pos
            occupied = self.segment_search(new_pos,segments)
        self.pos = new_pos
    
    def segment_search(self, pos, segments):
        for segment in segments:
                if pos == segment.pos:
                    return True
        return False


class SnakeSegment():
    def __init__(self, size, pos = (0,0)):
        self.tile_size = size
        self.size = size * 0.8
        self.pos = pos
        self.color = pygame.Color(255, 255, 255)
        self.alpha = 255
        self.surface = self.update_surface()

    def update(self, time, next_segment):
        self.pos = next_segment.pos
    
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        self.color.a = self.alpha
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, ((self.pos[0]*self.tile_size)+(self.tile_size-self.size)/2, (self.pos[1]*self.tile_size)+(self.tile_size-self.size)/2))

class SnakeHead():
    def __init__(self, size, pos = (0,0)):
        self.tile_size = size
        self.size = size
        self.pos = pos
        self.alive = True
        self.color = pygame.Color(255, 255, 255)
        self.alpha = 255
        self.exploded = False
        self.segments = [] # youngest/furthest back segments are first in list
        self.explosion = None
        self.surface = self.update_surface()
        for i in range(5):
            self.grow((self.pos[0], self.pos[1]+i))

    def update(self, time, direction, food):
        if self.alive:
            self.check_for_collision(direction)
            if not self.alive:
                return
            if len(self.segments)>0: # Segments start from the back and move to the spot that the next segment is
                back_pos = self.segments[0].pos
                for i in range(len(self.segments)-1):
                    self.segments[i].update(time, self.segments[i+1])
                self.segments[len(self.segments)-1].update(time, self)
            self.pos = self.move(direction)
            self.check_for_food(food, back_pos)
        elif not self.exploded:
            self.explosion = Explosion(self.tile_size, self.size, self.pos)
            self.exploded = True
        else:
            self.explosion.update(time)

    def move(self, direction): # help from https://www.youtube.com/watch?v=AvV6UxuzH5c
        new_pos = self.pos
        if (direction == Inputs.UP):
            new_pos = (self.pos[0], self.pos[1] - 1)
        elif (direction == Inputs.DOWN):
            new_pos = (self.pos[0], self.pos[1] + 1)
        elif (direction == Inputs.LEFT):
            new_pos = (self.pos[0] - 1, self.pos[1])
        elif (direction == Inputs.RIGHT):
            new_pos = (self.pos[0] + 1, self.pos[1])
        return new_pos


    def grow(self, pos = (0,0)):
        self.segments.insert(0, SnakeSegment(self.tile_size, pos))
        print("Segment added")

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        self.color.a = self.alpha
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        if self.exploded:
            self.explosion.draw(surface)
        surface.blit(self.surface, ((self.pos[0]*self.tile_size)+((self.tile_size-self.size)/2), (self.pos[1]*self.tile_size)+(self.tile_size-self.size)/2))
        for segment in self.segments:
            segment.draw(surface)

    def check_for_food(self, food, pos):
        if self.pos == food.pos:
            self.grow(pos)
            food.eaten(self.segments)
    
    def check_for_collision(self, direction):
        next_pos = self.move(direction)
        if next_pos[0] < 0 or next_pos[0] > 29 or next_pos[1] < 0 or next_pos[1] > 29: # Check borders
            print("Collision")
            self.alive = False
            return
        for i in range(0,len(self.segments)-2): # Don't check the first few and last segment because realistically you can't collide with them
            if next_pos == self.segments[i].pos:
                print("Collision")
                self.alive = False
                return


        

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
    
def draw_world_border(surface):
    rect = pygame.Rect(0, 0, 600, 600)
    surface.blit(surface, (0,0))
    pygame.draw.rect(surface, "White", rect, 4)

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
        draw_world_border(screen)
        player.update(deltatime, direction, food)
        food.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        deltatime = clock.tick(12)
    pygame.quit()

if __name__ == "__main__":
    main()