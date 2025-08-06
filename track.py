import pygame
import math


class Track:
    def __init__(self, width, height, start, checkpoints):
        self.track_image = pygame.image.load("custom_track.png").convert()
        self.track_image = pygame.transform.scale(self.track_image, (width, height))
        self.track_surface = self.track_image.copy()
        self.width = width
        self.height = height

        self.background_color = (55, 125, 34)
        self.start_position = start
        self.start_angle = 0
        self.checkpoints = checkpoints
        self.checkpoint_radius = 50

    def draw_track(self, surface):
        """Draw the track surface"""
        surface.blit(self.track_surface, (0, 0))
        
        for checkpoint_pos in self.checkpoints:
            pygame.draw.circle(surface, (255, 215, 0), checkpoint_pos, self.checkpoint_radius, 3)

    def is_on_track(self, position):
        """Check if car has crashed returns False if crashed"""
        x, y = int(position[0]), int(position[1])

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        pixel_color = self.track_surface.get_at((x, y))[:3]
        if pixel_color == self.background_color:
            return False
        return True
    
    def check_checkpoint_collision(self, car_position, current_checkpoint_index):
        """Check if car has reached the next checkpoint"""
        if current_checkpoint_index >= len(self.checkpoints):
            return False, current_checkpoint_index
            
        checkpoint_pos = self.checkpoints[current_checkpoint_index]
        distance = ((car_position[0] - checkpoint_pos[0])**2 + 
                (car_position[1] - checkpoint_pos[1])**2)**0.5
        
        if distance <= self.checkpoint_radius:
            next_checkpoint = (current_checkpoint_index + 1) % len(self.checkpoints)
            return True, next_checkpoint
        
        return False, current_checkpoint_index
