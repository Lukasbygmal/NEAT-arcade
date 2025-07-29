import pygame
import time
from game import Game

SCREEN_SIZE = 800

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("RL RACER")

font = pygame.font.SysFont(None, 44)

def main():
    game = Game(screen)
    running = True

    while running:
        dt = clock.tick(60) / 1000.0 # Might need to lower fps for performance?

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update(dt)
        game.render()

    pygame.quit()


if __name__ == "__main__":
    main()
