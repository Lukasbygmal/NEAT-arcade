import numpy as np
import pygame
from track import Track
from car import Car


class Environment:
    """
    Reinforcement learning environment for a racing car simulation.

    This class provides a complete RL environment where an agent controls a car
    navigating around a track. The environment handles physics, collision detection,
    reward calculation, and rendering.
    """

    def __init__(self, render_mode=None):
        """
        Initialize the racing environment.

        Args:
            render_mode (str, optional): Rendering mode. Options are 'human' for
                                       visual display or None for headless mode.
        """
        self.render_mode = render_mode

        if self.render_mode == "human":
            pygame.init()
            self.screen = pygame.display.set_mode((1200, 800))
            pygame.display.set_caption("RL Racing")
            self.clock = pygame.time.Clock()
        else:
            pygame.init()
            self.screen = pygame.Surface((1200, 800))

        self.track = Track(1200, 800)
        self.car = Car(self.track.start_position, self.track.start_angle)

        self.max_steps = 2000
        self.current_step = 0
        self.action_space_size = 7
        self.observation_space_size = 10

        self.last_distance = 0

    def reset(self):
        """
        Reset the environment to its initial state.

        Returns:
            np.ndarray: The initial state observation as a numpy array.
        """
        self.car.reset(self.track.start_position, self.track.start_angle)
        self.current_step = 0
        self.last_distance = 0

        state = self._get_state()
        return np.array(state, dtype=np.float32)

    def step(self, action):
        """
        Execute one step in the environment.

        Args:
            action (int): The action to take. Actions are:
                         0: No action
                         1: Increase speed
                         2: Decrease speed
                         3: Turn left
                         4: Turn right
                         5: Increase speed and turn left
                         6: Increase speed and turn right

        Returns:
            tuple: A tuple containing:
                - state (np.ndarray): The new state observation
                - reward (float): The reward for this step
                - done (bool): Whether the episode is finished
                - info (dict): Additional information about the step
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
            "crashed": not self.car.is_alive and self.current_step < self.max_steps,
        }

        return np.array(state, dtype=np.float32), reward, done, info

    def _execute_action(self, action):
        """
        Execute the given action on the car.

        Args:
            action (int): The action index to execute.
        """
        if action == 1:
            self.car.increase_speed()
        elif action == 2:
            self.car.decrease_speed()
        elif action == 3:
            self.car.turn_left()
        elif action == 4:
            self.car.turn_right()
        elif action == 5:
            self.car.increase_speed()
            self.car.turn_left()
        elif action == 6:
            self.car.increase_speed()
            self.car.turn_right()

    def _check_collision(self):
        """
        Check if car has collided with track boundaries.

        Kills the car if any of its corners or center point are outside
        the valid track area.
        """
        if not self.car.is_alive:
            return

        car_rect = self.car.get_rect()
        car_corners = [
            (car_rect.left, car_rect.top),
            (car_rect.right, car_rect.top),
            (car_rect.left, car_rect.bottom),
            (car_rect.right, car_rect.bottom),
            (car_rect.centerx, car_rect.centery),
        ]

        for corner in car_corners:
            if not self.track.is_on_track(corner):
                self.car.kill_car()
                break

    def _get_state(self):
        """
        Get the current state observation.

        Returns:
            The current state from the car's perspective.
        """
        return self.car.get_state(self.track)

    def _calculate_reward(self):
        """
        Calculate the reward for the current step.

        Returns:
            float: The reward value. Negative reward for crashes, positive for
                   distance progress and staying alive.
        """
        if not self.car.is_alive:
            return -100

        distance_reward = self.car.total_distance - self.last_distance
        self.last_distance = self.car.total_distance

        alive_reward = 0.1

        return distance_reward + alive_reward

    def _is_done(self):
        """
        Check if the episode is finished.

        Returns:
            bool: True if the car is dead or max steps reached, False otherwise.
        """
        return not self.car.is_alive or self.current_step >= self.max_steps

    def render(self):
        """
        Render the current state of the environment.

        Returns:
            np.ndarray: RGB array representation if render_mode is 'rgb_array',
                        None otherwise.
        """
        if self.render_mode == "human":
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.track.track_surface, (0, 0))
            self.car.render(self.screen)
            self.car.render_rays(self.screen, self.track)
            pygame.display.flip()
            self.clock.tick(60)
        elif self.render_mode == "rgb_array":
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.track.track_surface, (0, 0))
            self.car.render(self.screen)
            return pygame.surfarray.array3d(self.screen)

    def close(self):
        """
        Clean up and close the environment.

        Properly shuts down pygame resources.
        """
        if hasattr(self, "screen"):
            pygame.quit()


if __name__ == "__main__":
    env = Environment(render_mode="human")

    state = env.reset()
    print(f"Initial state shape: {state.shape}")
    print(f"Action space size: {env.action_space_size}")

    for step in range(1000):
        action = np.random.randint(0, env.action_space_size)
        state, reward, done, info = env.step(action)
        env.render()

        if done:
            print(f"Episode finished at step {step}")
            print(f"Final distance: {info['distance_traveled']}")
            if info["crashed"]:
                print("Car crashed!")
            break

    env.close()
