import pygame
import math

class Car:
    def __init__(self, start_position, start_angle):
        self.position = list(start_position)
        self.angle = start_angle
        self.speed = 0
        
        self.max_speed = 5
        self.min_speed = -2
        self.acceleration = 0.5
        self.friction = 0.95
        self.turn_rate = 3
        
        self.width = 20
        self.height = 10
    
    def accelerate(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
    
    def brake(self):
        self.speed = max(self.speed - self.acceleration, self.min_speed)
    
    def apply_friction(self):
        self.speed *= self.friction
    
    def turn_left(self):
        self.angle -= self.turn_rate
    
    def turn_right(self):
        self.angle += self.turn_rate
    
    def update_position(self, dt):
        rad_angle = math.radians(self.angle)
        self.position[0] += self.speed * math.cos(rad_angle) * dt * 60
        self.position[1] += self.speed * math.sin(rad_angle) * dt * 60
    
    def stop(self):
        self.speed = 0
    
    def get_rect(self):
        return pygame.Rect(self.position[0] - self.width//2, 
                          self.position[1] - self.height//2, 
                          self.width, self.height)
    
    def render(self, screen):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill((255, 0, 0))
        rotated_surface = pygame.transform.rotate(surface, -self.angle)
        rect = rotated_surface.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(rotated_surface, rect.topleft)