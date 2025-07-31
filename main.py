import pygame
import time
from game import Game

SCREEN_SIZE = 800

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("RL RACER")

font = pygame.font.SysFont(None, 44)


def main():
    game = Game(screen)
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.handle_input(events)
        game.update()
        game.render()
        clock.tick(60)


if __name__ == "__main__":
    main()
