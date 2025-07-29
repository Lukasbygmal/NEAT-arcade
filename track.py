import pygame
import math

class Track:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.track_surface = pygame.Surface((width, height))
        self.collision_surface = pygame.Surface((width, height))
        
        self.track_color = (128, 128, 128)
        self.outline_color = (255, 255, 255)
        self.background_color = (0, 128, 0)
        self.track_on_color = (255, 0, 0)
        
        self.center_x = width // 2
        self.center_y = height // 2
        self.outer_radius = min(width, height) // 2 - 50
        self.inner_radius = self.outer_radius - 80
        
        self.start_position = (self.center_x, self.center_y - self.outer_radius + 40)
        self.start_angle = 90
        
        self._generate_track()
    
    def _generate_track(self):
        self.track_surface.fill(self.background_color)
        self.collision_surface.fill((0, 0, 0))
        
        pygame.draw.circle(self.track_surface, self.track_color, 
                          (self.center_x, self.center_y), self.outer_radius)
        pygame.draw.circle(self.track_surface, self.background_color, 
                          (self.center_x, self.center_y), self.inner_radius)
        
        pygame.draw.circle(self.track_surface, self.outline_color, 
                          (self.center_x, self.center_y), self.outer_radius, 3)
        pygame.draw.circle(self.track_surface, self.outline_color, 
                          (self.center_x, self.center_y), self.inner_radius, 3)
        
        pygame.draw.circle(self.collision_surface, self.track_on_color, 
                          (self.center_x, self.center_y), self.outer_radius)
        pygame.draw.circle(self.collision_surface, (0, 0, 0), 
                          (self.center_x, self.center_y), self.inner_radius)
    
    def draw_track(self, surface):
        surface.blit(self.track_surface, (0, 0))
    
    def is_on_track(self, position):
        x, y = int(position[0]), int(position[1])
        
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        pixel_color = self.collision_surface.get_at((x, y))
        return pixel_color[:3] == self.track_on_color