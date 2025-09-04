import pygame
from enum import Enum
from race_map_creator import RaceMapCreator
from simulation import NEATSimulation
from race_environment import RaceEnvironment
from track import Track


class GameType(Enum):
    """Enumeration of available game types"""

    RACE = "RACE"
    SPACE = "SPACE"


class GameConfig:
    """Configuration container for different game types"""

    def __init__(
        self, map_creator_class, environment_class, world_class, max_steps=1200
    ):
        self.map_creator_class = map_creator_class
        self.environment_class = environment_class
        self.world_class = world_class
        self.max_steps = max_steps


class Button:
    """Simple button class for menu interactions"""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        color=(100, 100, 100),
        text_color=(255, 255, 255),
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def handle_event(self, event):
        """Handle mouse events for the button"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        """Draw the button on screen"""
        color = (150, 150, 150) if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class GameMenu:
    """Main menu for game type selection"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self._create_buttons()

    def _create_buttons(self):
        """Create menu buttons"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 200
        button_height = 60

        self.buttons = {
            GameType.RACE: Button(
                screen_width // 2 - button_width // 2,
                screen_height // 2 - 50,
                button_width,
                button_height,
                "RACE",
                self.font,
            ),
            GameType.SPACE: Button(
                screen_width // 2 - button_width // 2,
                screen_height // 2 + 20,
                button_width,
                button_height,
                "SPACE",
                self.font,
            ),
        }

    def handle_events(self, events):
        """Handle menu events and return selected game type"""
        for event in events:
            for game_type, button in self.buttons.items():
                if button.handle_event(event):
                    return game_type
        return None

    def draw(self):
        """Draw the menu"""
        self.screen.fill((128, 128, 128))

        title_text = self.font.render("Select Game Type", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(title_text, title_rect)

        for button in self.buttons.values():
            button.draw(self.screen)


def run_game_session(screen, font, game_config):
    """Run the map creation and simulation loop for a selected game type"""
    map_creator = game_config.map_creator_class(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    track_surface, start_pos, checkpoints = map_creator.get_map_data()

                    if start_pos is None:
                        print(
                            "Please place a start position before starting simulation!"
                        )
                        continue

                    pygame.image.save(track_surface, "track.png")
                    print(f"Map saved! Start position: {start_pos}")
                    print(f"Checkpoints: {checkpoints}")
                    print("Starting NEAT simulation...")

                    simulation = NEATSimulation(
                        start=start_pos,
                        checkpoints=checkpoints,
                        screen=screen,
                        environment_class=game_config.environment_class,
                        world_class=game_config.world_class,
                        max_steps=game_config.max_steps,
                    )
                    simulation.run()
                    return True

        map_creator.handle_events(events)

        screen.fill((0, 0, 0))
        map_creator.draw()

        mode_text = font.render(
            f"Mode: {map_creator.mode} (1=Track, 2=Off Track, 3=Start, 4=Checkpoint) | S to start simulation",
            True,
            (255, 255, 255),
        )
        screen.blit(mode_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    return False


def main():
    """Main entry point"""
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Game Launcher")
    font = pygame.font.SysFont(None, 44)
    clock = pygame.time.Clock()

    game_configs = {
        GameType.RACE: GameConfig(RaceMapCreator, RaceEnvironment, Track, 1200),
        GameType.SPACE: GameConfig(   # change when adding space
            RaceMapCreator,
            RaceEnvironment,
            Track,
            1200,
        ),
    }

    menu = GameMenu(screen, font)
    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        selected_game = menu.handle_events(events)

        if selected_game:
            config = game_configs[selected_game]
            if not run_game_session(screen, font, config):
                running = False

        menu.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
