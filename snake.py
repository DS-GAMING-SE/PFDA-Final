import pygame
import random




class SnakeSegment():
    def __init__(self, screen_res, size):
        self.screen_res = screen_res
        self.particle_size = size

class SnakeHead():
    def __init__(self, screen_res, size):
        self.screen_res = screen_res
        self.particle_size = size
        self.segments = []

def main():
    pygame.init
    pygame.display.set_caption("Snake")
    resolution = (800, 600)
    tile_size = 10
    screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    deltatime = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('Black')
        pygame.display.flip()
        deltatime = clock.tick(8)
    pygame.quit()
    

if __name__ == "__main__":
    main()