from abc import ABC, abstractmethod

class Environment(ABC):
    """
    Abstract base class for all simulation environments.
    """
    
    @abstractmethod
    def reset(self):
        """Reset the environment to its initial state."""
        pass
    
    @abstractmethod
    def step(self, action):
        """Execute one step in the environment."""
        pass
    
    @abstractmethod
    def _get_state(self):
        """Get current state representation."""
        pass
    
    @abstractmethod
    def is_alive(self):
        """Check if entity is still alive."""
        pass
    
    @abstractmethod
    def render_entity(self, screen):
        """Render the entity on screen."""
        pass