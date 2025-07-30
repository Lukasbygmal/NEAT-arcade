import pygame
import math


class Car:
    def __init__(self, start_position, start_angle):
        self.position = list(start_position)
        self.angle = start_angle
        self.speed = 0
        self.max_speed = 8
        self.min_speed = -2
        self.acceleration = 0.2
        self.turn_rate = 3
        self.width = 25
        self.height = 14
        self.total_distance = 0
        self.last_position = list(start_position)
        self.is_alive = True

    def turn_left(self):
        """Turn left"""
        if self.is_alive:
            self.angle -= self.turn_rate

    def turn_right(self):
        """Turn right"""
        if self.is_alive:
            self.angle += self.turn_rate

    def increase_speed(self):
        """Increase speed"""
        if self.is_alive:
            self.speed = min(self.speed + self.acceleration, self.max_speed)

    def decrease_speed(self):
        """Decrease speed"""
        if self.is_alive:
            self.speed = max(self.speed - self.acceleration, self.min_speed)

    def update_position(self, dt):
        """Update car position and calculate distance traveled"""
        if not self.is_alive:
            return

        self.last_position = list(self.position)

        rad_angle = math.radians(self.angle)
        self.position[0] += self.speed * math.cos(rad_angle) * dt * 60
        self.position[1] += self.speed * math.sin(rad_angle) * dt * 60

        dx = self.position[0] - self.last_position[0]
        dy = self.position[1] - self.last_position[1]
        distance_this_frame = math.sqrt(dx * dx + dy * dy)
        self.total_distance += distance_this_frame

    def kill_car(self):
        """Kill the car"""
        self.is_alive = False
        self.speed = 0

    def reset(self, start_position, start_angle):
        """Reset car to initial state for new RL episode"""
        self.position = list(start_position)
        self.angle = start_angle
        self.speed = 0
        self.total_distance = 0
        self.last_position = list(start_position)
        self.is_alive = True

    def get_rect(self):
        """Get pygame rect for collision detection"""
        return pygame.Rect(
            self.position[0] - self.width // 2,
            self.position[1] - self.height // 2,
            self.width,
            self.height,
        )

    def render(self, screen):
        """Render the car on screen"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        color = (255, 128, 0) if self.is_alive else (200, 0, 0)
        surface.fill(color)
        rotated_surface = pygame.transform.rotate(surface, -self.angle)
        rect = rotated_surface.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(rotated_surface, rect.topleft)
