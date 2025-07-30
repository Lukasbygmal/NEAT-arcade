import pygame
from track import Track
from car import Car


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.track = Track(1200, 800)
        self.car = Car(self.track.start_position, self.track.start_angle)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.car.accelerate()
        elif keys[pygame.K_DOWN]:
            self.car.brake()
        else:
            self.car.apply_friction()

        if keys[pygame.K_LEFT]:
            self.car.turn_left()
        if keys[pygame.K_RIGHT]:
            self.car.turn_right()

    def update(self, dt):
        self.handle_input()
        self.car.update_position(dt)

        if not self.track.is_on_track(self.car.position):
            self.car.stop()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.track.track_surface, (0, 0))
        self.car.render(self.screen)
        pygame.display.flip()
