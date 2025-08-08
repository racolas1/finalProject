import sys
import pygame
from sudoku_generator import *

width = 640
height = 512
square_size =
screen = pygame.display.set_mode((width, height))

def start_screen():
    title_font = pygame.font.SysFont("comicsans", 30)
    button_font = pygame.font.SysFont("comicsans", 20)
    screen.fill("yellow")

    title_surface = title_font.render("Sodoku", 0 , "black")
    border = title_surface.get_rect(center = (width//2, height//2))
    screen.blit(title_surface, border)

    easy_text = button_font.render("Easy", 0 , "black")
    medium_text = button_font.render("Medium", 0, "black")
    hard_text = button_font.render("Hard", 0, "black")
    quit_text = button_font.render("Quit", 0 , "black")

    start_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    start_surface.fill("green")
    start_surface.blit(easy_text, (10, 10))

    start_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    start_surface.fill("yellow")
    start_surface.blit(easy_text, (10, 10))

    quit_surface = pygame.Surface((quit_text.get_size()[0] + 20, quit_text.get_size()[1] + 20))
    quit_surface.fill("red")
    quit_surface.blit(quit_text, (10, 10))

    start_rectangle = start_surface.get_rect(center = (width//2, height//2) + 50)
    quit_rectangle = quit_surface.get_rect(center = (width//2, height//2) + 150)

    screen.blit(start_surface, start_rectangle)
    screen.blit(quit_surface, quit_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rectangle.collidepoint(event.pos):
                    return
                elif quit_rectangle.collidepoint(event.pos):
                    sys.exit()
        pygame.display.update()

def game_over:
    game_over_font = pygame.font.Font(None, 40)
    screen.fill("red")
    if winner != 0:
        text = f"Player {winner} wins!"
    else:
        text f"Player {winner} loses!"
    game_over_surf = game_over_font.render(text, 0 , "black")
    game_over_rect = game_over_surf.get_rect(center=(width//2, height//2))
    screen.blit(game_over_surf, game_over_rect)
    restart_surf = game_over_font.render(text, 0 , "black")
    restart_rect = restart_surf.get_rect(center=(width//2, height//2))
    screen.blit(restart_surf, restart_rect)

    menu_surf = game_over_font.render(text, 0 , "black")
    menu_rect = menu_surf.get_rect(center=(width//2, height//2))
    screen.blit(menu_surf, menu_rect)

    if __name__ = 'main':
        game_over = false
        winner = 0

        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sodoku")

        screen.fill("yellow")
        board = generate_sudoku()

        # vertical lines
        for i in range(9):
            pygame.draw.line(screen, "dark green", (i * 32, 0), (i * 32, 512))
        # Horizontal lines
        for i in range(9):
            pygame.draw.line(screen, "dark green", (0, i * 32), (640, i * 32))

        while True:
            try:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                            clicked_row = int(event.pos[1] / square_size)
                            clicked_col = int(event.pos[0] / square_size)
                            print(clicked_row, clicked_col)

                        if




