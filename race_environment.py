import numpy as np
import pygame
from track import Track
from car import Car
from environment import Environment


class RaceEnvironment(Environment):
    """
    Reinforcement learning environment for a racing car simulation.
    Provides control, physics, collision, reward logic, and rendering.
    """

    SCREEN_WIDTH = 1200 #TODO this should probably be moved up to simulation
    SCREEN_HEIGHT = 800
    MAX_STEPS = 1200

    def __init__(self, track):
        
        self.track = track
        self.car = Car(self.track.start_position, self.track.start_angle)

        self.current_step = 0
        self.last_distance = 0

    def reset(self):
        """Reset the environment to its initial state."""
        self.car.reset(self.track.start_position, self.track.start_angle)
        self.current_step = 0
        self.last_distance = 0
        return np.array(self._get_state(), dtype=np.float32)

    def step(self, action):
        """
        Execute one step in the environment.

        Args:
            action (int): The action to take (0-6).

        Returns:
            tuple: (state, reward, done, info)
        """
        self.current_step += 1
        self._execute_action(action)
        self.car.update_position()
        self._check_collision()

        reward = self._calculate_reward()
        done = self._is_done()
        state = self._get_state()

        info = {
            "distance_traveled": self.car.total_distance,
            "is_alive": self.car.is_alive,
            "speed": self.car.speed,
            "position": self.car.position.copy(),
            "crashed": not self.car.is_alive and self.current_step < self.MAX_STEPS,
        }

        return np.array(state, dtype=np.float32), reward, done, info

    def _execute_action(self, action):
        """Apply the chosen action to the car."""
        if action == 0:
            pass
        elif action == 1:
            self.car.increase_speed()
        elif action == 2:
            self.car.decrease_speed()
        elif action == 3:
            self.car.turn_left()
        elif action == 4:
            self.car.turn_right()

    def _check_collision(self):
        """Kill the car if any important part is off-track."""
        if not self.car.is_alive:
            return

        if not self.track.is_on_track(self.car.position):
            self.car.kill_car()

    def _calculate_reward(self):
        """Reward for distance progress and staying alive."""
        if not self.car.is_alive:
            return -200 #TODO magic numbers in function

        total_reward = 0
        delta_distance = self.car.total_distance - self.last_distance
        self.last_distance = self.car.total_distance
        
        speed_factor = self.car.speed / self.car.max_speed
        total_reward += delta_distance * speed_factor * 10
        
        hit_checkpoint, new_checkpoint_index = self.track.check_checkpoint_collision(
            self.car.position, self.car.current_checkpoint
        )
    
        if hit_checkpoint:
            total_reward += 15000
            self.car.current_checkpoint = new_checkpoint_index
            self.car.checkpoints_passed += 1
            
        return total_reward

    def _get_state(self):
        """Return current car state."""
        return self.car.get_state(self.track)

    def _is_done(self):
        """Episode ends on death or max steps."""
        return not self.car.is_alive or self.current_step >= self.MAX_STEPS
    
    def is_alive(self):
        """Check if car is still alive."""
        return self.car.is_alive
    
    def render_entity(self, screen):
        """Render the car on screen."""
        self.car.render(screen)