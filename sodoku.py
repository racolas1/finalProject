import sys

import pygame

width = 640
height = 512
screen = pygame.display.set_mode((width, height))

def start_screen():
    title_font = pygame.font.SysFont("comicsans", 30)
    button_font = pygame.font.SysFont("comicsans", 20)
    screen.fill("yellow")

    title_surface = title_font.render("Sodoku", 0 , "black")
    border = title_surface.get_rect(center = (width//2, height//2))
    screen.blit(title_surface, border)

    start_text = button_font.render("Start", 0 , "black")
    quit_text = button_font.render("Quit", 0 , "black")

    start_surface = pygame.Surface((start_text.get_size()[0] + 20, start_text.get_size()[1] + 20))
    start_surface.fill("yellow")
    start_surface.blit(start_text, (10, 10))

    quit_surface = pygame.Surface((start_text.get_size()[0] + 20, start_text.get_size()[1] + 20))
    quit_surface.fill("yellow")
    quit_surface.blit(start_text, (10, 10))

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



