import pygame
from track import Track
from car import Car


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.track = Track(1200, 800)
        self.car = Car(self.track.start_position, self.track.start_angle)

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.car.increase_speed()
                elif event.key == pygame.K_DOWN:
                    self.car.decrease_speed()
                elif event.key == pygame.K_LEFT:
                    self.car.turn_left()
                elif event.key == pygame.K_RIGHT:
                    self.car.turn_right()

    def update(self):
        self.car.update_position()
        if(self.car.is_alive):
            print(self.car.get_state(self.track))
        

        if not self.track.is_on_track(self.car.position):
            self.car.kill_car()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.track.track_surface, (0, 0))
        self.car.render(self.screen)
        self.car.render_rays(self.screen, self.track)
        pygame.display.flip()
