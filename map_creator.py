import pygame

class MapCreator:
    def __init__(self, screen):
        self.screen = screen
        self.width = 1200
        self.height = 800
        self.grid_size = 25
        self.cols = self.width // self.grid_size
        self.rows = self.height // self.grid_size
        
        self.green = (55, 125, 34)
        self.gray = (128, 128, 128)
        self.white = (255, 255, 255)
        self.gold = (255, 215, 0)
        
        self.grid = [[self.green for _ in range(self.cols)] for _ in range(self.rows)]
        self.start_pos = None
        self.gold_positions = []
        self.mode = 1
        self.mouse_pressed = False
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.mode = 1
                elif event.key == pygame.K_2:
                    self.mode = 2
                elif event.key == pygame.K_3:
                    self.mode = 3
                elif event.key == pygame.K_4:
                    self.mode = 4
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pressed = True
                    self.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    self.handle_click(pygame.mouse.get_pos())
    
    def handle_click(self, pos):
        x, y = pos
        col = x // self.grid_size
        row = y // self.grid_size
        
        if 0 <= col < self.cols and 0 <= row < self.rows:
            if self.mode == 1:
                self.grid[row][col] = self.gray
                if (col, row) == self.start_pos:
                    self.start_pos = None
                if (col, row) in self.gold_positions:
                    self.gold_positions.remove((col, row))
            elif self.mode == 2:
                self.grid[row][col] = self.green
                if (col, row) == self.start_pos:
                    self.start_pos = None
                if (col, row) in self.gold_positions:
                    self.gold_positions.remove((col, row))
            elif self.mode == 3:
                if self.start_pos:
                    old_col, old_row = self.start_pos
                    if self.grid[old_row][old_col] == self.white:
                        self.grid[old_row][old_col] = self.green
                self.start_pos = (col, row)
                self.grid[row][col] = self.white
                if (col, row) in self.gold_positions:
                    self.gold_positions.remove((col, row))
            elif self.mode == 4:
                if (col, row) not in self.gold_positions:
                    self.gold_positions.append((col, row))
                    self.grid[row][col] = self.gold
                    if (col, row) == self.start_pos:
                        self.start_pos = None
    
    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.grid[row][col]
                rect = pygame.Rect(col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
    
    def get_map_data(self):
        surface = pygame.Surface((self.width, self.height))
        
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.grid[row][col]
                if color == self.white or color == self.gold:
                    color = self.gray
                rect = pygame.Rect(col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(surface, color, rect)
        
        for col, row in self.gold_positions:
            center_x = col * self.grid_size + self.grid_size // 2
            center_y = row * self.grid_size + self.grid_size // 2
            pygame.draw.rect(surface, self.gold, (center_x - 37, center_y - 37, 75, 75))
        
        start_position = None
        if self.start_pos:
            col, row = self.start_pos
            start_position = (col * self.grid_size + self.grid_size // 2, row * self.grid_size + self.grid_size // 2)
        
        checkpoints = []
        for col, row in self.gold_positions:
            checkpoint_pos = (col * self.grid_size + self.grid_size // 2, row * self.grid_size + self.grid_size // 2)
            checkpoints.append(checkpoint_pos)
        
        return surface, start_position, checkpoints