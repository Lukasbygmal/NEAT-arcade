import pygame
from enum import Enum
from typing import List, Tuple, Optional


class EditMode(Enum):
    TRACK = 1
    OFF_TRACK = 2
    START = 3
    CHECKPOINT = 4


class Colors:
    OFF_TRACK = (55, 125, 34)
    TRACK = (128, 128, 128)
    START = (255, 255, 255)
    CHECKPOINT = (255, 215, 0)
    GRID_LINE = (0, 0, 0)


class RaceMapCreator:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = 1200
        self.height = 800
        self.grid_size = 25
        self.cols = self.width // self.grid_size
        self.rows = self.height // self.grid_size

        self.grid = [
            [Colors.OFF_TRACK for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.start_pos: Optional[Tuple[int, int]] = None
        self.gold_positions: List[Tuple[int, int]] = []
        self.mode = EditMode.TRACK
        self.mouse_pressed = False

        self.key_mode_map = {
            pygame.K_1: EditMode.TRACK,
            pygame.K_2: EditMode.OFF_TRACK,
            pygame.K_3: EditMode.START,
            pygame.K_4: EditMode.CHECKPOINT,
        }

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.mode = self.key_mode_map.get(event.key, self.mode)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pressed = True
                self._handle_grid_click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION and self.mouse_pressed:
                self._handle_grid_click(pygame.mouse.get_pos())

    def _pos_to_grid(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert screen position to grid coordinates."""
        x, y = pos
        col, row = x // self.grid_size, y // self.grid_size
        return (col, row) if 0 <= col < self.cols and 0 <= row < self.rows else None

    def _grid_to_center_pos(self, col: int, row: int) -> Tuple[int, int]:
        """Convert grid coordinates to center pixel position."""
        return (
            col * self.grid_size + self.grid_size // 2,
            row * self.grid_size + self.grid_size // 2,
        )

    def _clear_position_from_special_lists(self, col: int, row: int) -> None:
        """Remove position from start_pos and gold_positions if present."""
        if (col, row) == self.start_pos:
            self.start_pos = None
        if (col, row) in self.gold_positions:
            self.gold_positions.remove((col, row))

    def _handle_grid_click(self, pos: Tuple[int, int]) -> None:
        grid_pos = self._pos_to_grid(pos)
        if not grid_pos:
            return

        col, row = grid_pos

        if self.mode == EditMode.TRACK:
            self.grid[row][col] = Colors.TRACK
            self._clear_position_from_special_lists(col, row)

        elif self.mode == EditMode.OFF_TRACK:
            self.grid[row][col] = Colors.OFF_TRACK
            self._clear_position_from_special_lists(col, row)

        elif self.mode == EditMode.START:
            self._clear_old_start_position()
            self.start_pos = (col, row)
            self.grid[row][col] = Colors.START
            if (col, row) in self.gold_positions:
                self.gold_positions.remove((col, row))

        elif self.mode == EditMode.CHECKPOINT:
            if (col, row) not in self.gold_positions:
                self.gold_positions.append((col, row))
                self.grid[row][col] = Colors.CHECKPOINT
                if (col, row) == self.start_pos:
                    self.start_pos = None

    def _clear_old_start_position(self) -> None:
        """Clear the old start position from the grid."""
        if self.start_pos:
            old_col, old_row = self.start_pos
            if self.grid[old_row][old_col] == Colors.START:
                self.grid[old_row][old_col] = Colors.OFF_TRACK

    def _is_track_edge(self, row: int, col: int) -> bool:
        """Check if position is a valid track edge."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        return self.grid[row][col] == Colors.TRACK

    def _draw_corner_triangle(
        self,
        surface: pygame.Surface,
        row: int,
        col: int,
        dr1: int,
        dc1: int,
        dr2: int,
        dc2: int,
        triangle_points: List[Tuple[int, int]],
    ) -> None:
        """Draw corner smoothing triangle if L-corner is detected."""
        if self._is_track_edge(row + dr1, col + dc1) and self._is_track_edge(
            row + dr2, col + dc2
        ):
            pygame.draw.polygon(surface, Colors.TRACK, triangle_points)

    def _add_corner_smoothing(self, surface: pygame.Surface) -> None:
        """Add triangular smoothing to inner corners of L-shaped tracks."""
        corner_configs = [
            (-1, 0, 0, -1, [(0, 0), (1, 0), (0, 1)]),  # Top-left L
            (-1, 0, 0, 1, [(1, 0), (0, 0), (1, 1)]),  # Top-right L
            (1, 0, 0, -1, [(0, 1), (0, 0), (1, 1)]),  # Bottom-left L
            (1, 0, 0, 1, [(1, 1), (0, 1), (1, 0)]),  # Bottom-right L
        ]

        for row in range(self.rows):
            for col in range(self.cols):
                if not self._is_track_edge(row, col):
                    x, y = col * self.grid_size, row * self.grid_size

                    for dr1, dc1, dr2, dc2, offsets in corner_configs:
                        triangle_points = [
                            (x + ox * self.grid_size, y + oy * self.grid_size)
                            for ox, oy in offsets
                        ]
                        self._draw_corner_triangle(
                            surface, row, col, dr1, dc1, dr2, dc2, triangle_points
                        )

    def draw(self) -> None:
        """Draw the current grid state to the screen."""
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.grid[row][col]
                rect = pygame.Rect(
                    col * self.grid_size,
                    row * self.grid_size,
                    self.grid_size,
                    self.grid_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, Colors.GRID_LINE, rect, 1)

    def get_map_data(
        self,
    ) -> Tuple[pygame.Surface, Optional[Tuple[int, int]], List[Tuple[int, int]]]:
        """Generate final map surface and position data, convert start and checkpoints to track"""
        surface = pygame.Surface((self.width, self.height))
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.grid[row][col]
                if color in (Colors.START, Colors.CHECKPOINT):
                    color = Colors.TRACK

                rect = pygame.Rect(
                    col * self.grid_size,
                    row * self.grid_size,
                    self.grid_size,
                    self.grid_size,
                )
                pygame.draw.rect(surface, color, rect)

        self._add_corner_smoothing(surface)

        start_position = None
        if self.start_pos:
            start_position = self._grid_to_center_pos(*self.start_pos)

        checkpoints = [
            self._grid_to_center_pos(col, row) for col, row in self.gold_positions
        ]

        return surface, start_position, checkpoints
