import pygame
import math


class Car:
    def __init__(self, start_position, start_angle):
        self.position = list(start_position)
        self.angle = start_angle
        self.max_speed = 20
        self.min_speed = 2
        self.speed = self.min_speed
        self.acceleration = 0.02
        self.turn_rate = 10
        self.width = 45
        self.height = 20
        self.total_distance = 0
        self.last_position = list(start_position)
        self.is_alive = True
        self.ray_angles = [-75, -35, 0, 35, 75]

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

    def update_position(self):
        """Update car position and calculate distance traveled"""
        if not self.is_alive:
            return
        self.last_position = list(self.position)

        rad_angle = math.radians(self.angle)
        self.position[0] += self.speed * math.cos(rad_angle) #TODO magic number matching fps, ugly
        self.position[1] += self.speed * math.sin(rad_angle)

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
        self.speed = self.min_speed
        self.total_distance = 0
        self.last_position = list(start_position)
        self.is_alive = True
        self.current_checkpoint = 0
        self.checkpoints_passed = 0
        
    def raycast(self, track, angle_offset=0, max_distance=200):
        """Cast a ray from car position in given direction and return distance to wall"""
        if not self.is_alive:
            return 0
        
        ray_angle = math.radians(self.angle + angle_offset)
        start_x, start_y = self.position
        step_size = 2
        distance = 0
        
        while distance < max_distance:
            ray_x = start_x + distance * math.cos(ray_angle)
            ray_y = start_y + distance * math.sin(ray_angle)
            
            if not track.is_on_track((ray_x, ray_y)):
                return distance
            
            distance += step_size
        
        return max_distance
    
    def get_state(self, track):
        """Get current state for RL agent - returns normalized sensor readings and car info"""
        if not self.is_alive: #TODO DO I NEED THIS??
            return [0, 0, 0, 0, 0]
        
        ray_distances = [self.raycast(track, angle) for angle in self.ray_angles]
        
        max_sensor_range = 100
        normalized_rays = [min(d / max_sensor_range, 1.0) for d in ray_distances]
        rad = math.radians(self.angle)
        normalized_angle_vector = [math.cos(rad), math.sin(rad)]
        normalized_speed = (self.speed - self.min_speed) / (self.max_speed - self.min_speed) * 2 - 1

        return normalized_rays + [normalized_speed] + normalized_angle_vector
        
    def render_rays(self, screen, track, color=(255, 255, 0)):
        """Debug function to visualize rays (optional)"""
        if not self.is_alive:
            return
    
        
        for angle_offset in self.ray_angles:
            distance = self.raycast(track, angle_offset)
            ray_angle = math.radians(self.angle + angle_offset)
            
            end_x = self.position[0] + distance * math.cos(ray_angle)
            end_y = self.position[1] + distance * math.sin(ray_angle)
            
            pygame.draw.line(screen, color, self.position, (end_x, end_y), 1)

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
