import pygame
import math


class Track:
    def __init__(self, width, height):
        self.track_image = pygame.image.load("track_1.png").convert()
        self.track_image = pygame.transform.scale(self.track_image, (width, height))
        self.track_surface = self.track_image.copy()
        self.width = width
        self.height = height

        self.background_color = (55, 125, 34)
        self.start_position = (580, 540)
        self.start_angle = 0

    def draw_track(self, surface):
        """Draw the track surface"""
        surface.blit(self.track_surface, (0, 0))

    def is_on_track(self, position):
        """Check if car has crashed returns False if crashed"""
        x, y = int(position[0]), int(position[1])

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        pixel_color = self.track_surface.get_at((x, y))[:3]
        if pixel_color == self.background_color:
            return False
        return True
