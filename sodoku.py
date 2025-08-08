import sys
import pygame
from sudoku_generator import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 720
BOARD_WIDTH = 540
BOARD_HEIGHT = 540
BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 50
CELL_SIZE = BOARD_WIDTH // 9
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 120
SKETCH_FONT_SIZE = 20
NUMBER_FONT_SIZE = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (240, 240, 240)


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.original = value != 0  # Track if this was an original number

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = BOARD_X + self.col * CELL_SIZE
        y = BOARD_Y + self.row * CELL_SIZE

        cell_color = WHITE
        if self.selected:
            cell_color = LIGHT_GRAY
        pygame.draw.rect(self.screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))

        if self.selected:
            pygame.draw.rect(self.screen, RED, (x, y, CELL_SIZE, CELL_SIZE), 3)
        else:
            pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)


        if self.sketched_value != 0 and self.value == 0:
            sketch_font = pygame.font.Font(None, SKETCH_FONT_SIZE)
            sketch_surf = sketch_font.render(str(self.sketched_value), True, GRAY)
            self.screen.blit(sketch_surf, (x + 5, y + 5))

        if self.value != 0:
            font = pygame.font.Font(None, NUMBER_FONT_SIZE)
            color = BLACK if self.original else BLUE
            text_surf = font.render(str(self.value), True, color)
            text_rect = text_surf.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.screen.blit(text_surf, text_rect)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None

        removed_cells = {"easy": 30, "medium": 40, "hard": 50}[difficulty]
        self.board_2d = generate_sudoku(9, removed_cells)
        self.original_board = [row[:] for row in self.board_2d]

        self.cells = []
        for row in range(9):
            cell_row = []
            for col in range(9):
                cell = Cell(self.board_2d[row][col], row, col, screen)
                # Mark original cells (cells that came pre-filled)
                cell.original = (self.board_2d[row][col] != 0)
                cell_row.append(cell)
            self.cells.append(cell_row)

    def draw(self):
        # Fill background
        self.screen.fill(BACKGROUND_COLOR)

        title_font = pygame.font.Font(None, 60)
        title_surf = title_font.render("Sudoku", True, BLACK)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 25))
        self.screen.blit(title_surf, title_rect)

        pygame.draw.rect(self.screen, WHITE, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT))

        for row in range(9):
            for col in range(9):
                self.cells[row][col].draw()

        for i in range(0, 10):
            line_width = 4 if i % 3 == 0 else 1
            # Vertical lines
            x = BOARD_X + i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), line_width)
            # Horizontal lines
            y = BOARD_Y + i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), line_width)

        self.draw_buttons()

    def draw_buttons(self):
        button_y = BOARD_Y + BOARD_HEIGHT + 20
        button_spacing = 20
        total_width = 3 * BUTTON_WIDTH + 2 * button_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2

        # Reset button
        reset_rect = pygame.Rect(start_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, ORANGE, reset_rect)
        pygame.draw.rect(self.screen, BLACK, reset_rect, 2)

        # Restart button
        restart_rect = pygame.Rect(start_x + BUTTON_WIDTH + button_spacing, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, ORANGE, restart_rect)
        pygame.draw.rect(self.screen, BLACK, restart_rect, 2)

        # Exit button
        exit_rect = pygame.Rect(start_x + 2 * (BUTTON_WIDTH + button_spacing), button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, ORANGE, exit_rect)
        pygame.draw.rect(self.screen, BLACK, exit_rect, 2)

        # Button text
        button_font = pygame.font.Font(None, 30)

        reset_text = button_font.render("RESET", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_rect.center)
        self.screen.blit(reset_text, reset_text_rect)

        restart_text = button_font.render("RESTART", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        self.screen.blit(restart_text, restart_text_rect)

        exit_text = button_font.render("EXIT", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        self.screen.blit(exit_text, exit_text_rect)

        self.reset_button = reset_rect
        self.restart_button = restart_rect
        self.exit_button = exit_rect

    def select(self, row, col):
        if self.selected_cell:
            prev_row, prev_col = self.selected_cell
            self.cells[prev_row][prev_col].selected = False

        self.selected_cell = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        if BOARD_X <= x <= BOARD_X + BOARD_WIDTH and BOARD_Y <= y <= BOARD_Y + BOARD_HEIGHT:
            row = (y - BOARD_Y) // CELL_SIZE
            col = (x - BOARD_X) // CELL_SIZE
            if 0 <= row < 9 and 0 <= col < 9:
                return (row, col)
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if not self.cells[row][col].original:
                self.cells[row][col].set_cell_value(0)
                self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if not self.cells[row][col].original:
                self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if not self.cells[row][col].original:
                self.cells[row][col].set_cell_value(value)
                self.cells[row][col].set_sketched_value(0)

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                original_value = self.original_board[row][col]
                self.cells[row][col].set_cell_value(original_value)
                self.cells[row][col].set_sketched_value(0)

    def is_full(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return False
        return True

    def auto_solve(self):
        """Automatically solve the board for testing win condition"""
        solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        for row in range(9):
            for col in range(9):
                self.cells[row][col].set_cell_value(solution[row][col])
                self.cells[row][col].set_sketched_value(0)

    def create_invalid_board(self):
        """Create an invalid full board for testing lose condition"""
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    # Fill empty cells with 1 to create duplicates
                    self.cells[row][col].set_cell_value(1)
                    self.cells[row][col].set_sketched_value(0)

    def check_board(self):
        for row in range(9):
            nums = []
            for col in range(9):
                value = self.cells[row][col].value
                if value != 0:
                    if value in nums:
                        return False
                    nums.append(value)

        for col in range(9):
            nums = []
            for row in range(9):
                value = self.cells[row][col].value
                if value != 0:
                    if value in nums:
                        return False
                    nums.append(value)

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                nums = []
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        value = self.cells[row][col].value
                        if value != 0:
                            if value in nums:
                                return False
                            nums.append(value)
        return True


def start_screen(screen):
    screen.fill(WHITE)

    pattern_color = (240, 240, 240)
    for i in range(10):
        for j in range(10):
            x = i * 60
            y = j * 60
            if x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
                pygame.draw.rect(screen, pattern_color, (x, y, 60, 60), 1)

    bg_font = pygame.font.Font(None, 120)
    numbers = ['7', '5', '2', '4', '9', '6', '3']
    positions = [(100, 100), (300, 80), (500, 120), (80, 250), (400, 280), (520, 300), (200, 400)]

    for num, pos in zip(numbers, positions):
        if pos[0] < WINDOW_WIDTH - 60 and pos[1] < WINDOW_HEIGHT - 60:
            num_surf = bg_font.render(num, True, (230, 230, 230))
            screen.blit(num_surf, pos)

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Welcome to Sudoku", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
    screen.blit(title_text, title_rect)

    subtitle_font = pygame.font.Font(None, 40)
    subtitle_text = subtitle_font.render("Select Game Mode:", True, BLACK)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 220))
    screen.blit(subtitle_text, subtitle_rect)

    button_font = pygame.font.Font(None, 36)
    button_width = 140
    button_height = 60
    button_spacing = 40

    total_width = 3 * button_width + 2 * button_spacing
    start_x = (WINDOW_WIDTH - total_width) // 2
    button_y = 320

    easy_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, ORANGE, easy_rect)
    pygame.draw.rect(screen, BLACK, easy_rect, 3)
    easy_text = button_font.render("EASY", True, WHITE)
    easy_text_rect = easy_text.get_rect(center=easy_rect.center)
    screen.blit(easy_text, easy_text_rect)

    medium_rect = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, button_height)
    pygame.draw.rect(screen, ORANGE, medium_rect)
    pygame.draw.rect(screen, BLACK, medium_rect, 3)
    medium_text = button_font.render("MEDIUM", True, WHITE)
    medium_text_rect = medium_text.get_rect(center=medium_rect.center)
    screen.blit(medium_text, medium_text_rect)

    hard_rect = pygame.Rect(start_x + 2 * (button_width + button_spacing), button_y, button_width, button_height)
    pygame.draw.rect(screen, ORANGE, hard_rect)
    pygame.draw.rect(screen, BLACK, hard_rect, 3)
    hard_text = button_font.render("HARD", True, WHITE)
    hard_text_rect = hard_text.get_rect(center=hard_rect.center)
    screen.blit(hard_text, hard_text_rect)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return "easy"
                elif medium_rect.collidepoint(event.pos):
                    return "medium"
                elif hard_rect.collidepoint(event.pos):
                    return "hard"


def game_over_screen(screen, won):
    screen.fill(WHITE)

    pattern_color = (240, 240, 240)
    for i in range(10):
        for j in range(10):
            x = i * 60
            y = j * 60
            if x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
                pygame.draw.rect(screen, pattern_color, (x, y, 60, 60), 1)

    bg_font = pygame.font.Font(None, 120)
    numbers = ['7', '5', '2', '4', '9', '6', '3', '8']
    positions = [(50, 80), (250, 60), (450, 90), (80, 200), (350, 220), (520, 180), (150, 350), (400, 380)]

    for num, pos in zip(numbers, positions):
        if pos[0] < WINDOW_WIDTH - 60 and pos[1] < WINDOW_HEIGHT - 60:
            num_surf = bg_font.render(num, True, (230, 230, 230))
            screen.blit(num_surf, pos)

    title_font = pygame.font.Font(None, 100)
    if won:
        title_text = title_font.render("Game Won!", True, BLACK)
        button_color = GREEN
    else:
        title_text = title_font.render("Game Over :(", True, BLACK)
        button_color = ORANGE

    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
    screen.blit(title_text, title_rect)

    button_font = pygame.font.Font(None, 36)
    button_width = 140
    button_height = 60

    if won:
        exit_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 450, button_width, button_height)
        pygame.draw.rect(screen, button_color, exit_rect)
        pygame.draw.rect(screen, BLACK, exit_rect, 3)
        exit_text = button_font.render("EXIT", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_rect.collidepoint(event.pos):
                        return "exit"
    else:
        restart_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 450, button_width, button_height)
        pygame.draw.rect(screen, button_color, restart_rect)
        pygame.draw.rect(screen, BLACK, restart_rect, 3)
        restart_text = button_font.render("RESTART", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        return "restart"


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku")

    while True:
        difficulty = start_screen(screen)

        board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, screen, difficulty)

        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if hasattr(board, 'reset_button') and board.reset_button.collidepoint(event.pos):
                        board.reset_to_original()
                    elif hasattr(board, 'restart_button') and board.restart_button.collidepoint(event.pos):
                        running = False
                        break
                    elif hasattr(board, 'exit_button') and board.exit_button.collidepoint(event.pos):
                        sys.exit()
                    else:
                        cell_pos = board.click(x, y)
                        if cell_pos:
                            row, col = cell_pos
                            board.select(row, col)

                elif event.type == pygame.KEYDOWN:
                    if board.selected_cell:
                        row, col = board.selected_cell

                        if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                            number = event.key - pygame.K_0
                            board.sketch(number)

                        elif event.key == pygame.K_RETURN:
                            if board.cells[row][col].sketched_value != 0:
                                board.place_number(board.cells[row][col].sketched_value)

                        elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                            board.clear()

                        elif event.key == pygame.K_UP and row > 0:
                            board.select(row - 1, col)
                        elif event.key == pygame.K_DOWN and row < 8:
                            board.select(row + 1, col)
                        elif event.key == pygame.K_LEFT and col > 0:
                            board.select(row, col - 1)
                        elif event.key == pygame.K_RIGHT and col < 8:
                            board.select(row, col + 1)

                    #cheat keys
                    if event.key == pygame.K_w:
                        board.auto_solve()
                    elif event.key == pygame.K_l:
                        board.create_invalid_board()

            board.draw()
            pygame.display.update()

            if board.is_full():
                if board.check_board():
                    result = game_over_screen(screen, True)  # Won
                    if result == "exit":
                        sys.exit()
                else:
                    result = game_over_screen(screen, False)  # Lost
                    if result == "restart":
                        running = False
                        break

            clock.tick(60)
