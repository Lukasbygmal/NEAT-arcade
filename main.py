import pygame
from map_creator import MapCreator

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Map Creator")
font = pygame.font.SysFont(None, 44)


def main():
    map_creator = MapCreator(screen)
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    track_surface, start_pos, checkpoints = map_creator.get_map_data()
                    pygame.image.save(track_surface, "custom_track.png")
                    print(f"Map saved! Start position: {start_pos}")
                    print(f"Checkpoints: {checkpoints}")

        map_creator.handle_events(events)

        screen.fill((0, 0, 0))
        map_creator.draw()

        mode_text = font.render(
            f"Mode: {map_creator.mode} (1=Track, 2=Off Track, 3=Start, 4=Checkpoint) | Press S to save",
            True,
            (255, 255, 255),
        )
        screen.blit(mode_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
