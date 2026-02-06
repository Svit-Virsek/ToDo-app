import pygame, sys
from pygame.locals import *
pygame.init()

# -- Constants --
WIDTH = 400
HEIGHT = 711
BLUE = "#004CFF"
RED = "#FF0000"
GREEN = "#2BFF00"
BLACK = "#000000"
WHITE = "#FFFFFF"
GREY = "#606060"
FONT_SMALL = pygame.font.SysFont("arialrounded", 20)
FONT_MEDIUM = pygame.font.SysFont("arialrounded", 30)
FONT_BIG = pygame.font.SysFont("arialrounded", 40)
STARTING_HEIGHT = 31

# -- Screen objects --
screen = pygame.display.set_mode((WIDTH, HEIGHT))
typing_text = FONT_SMALL.render("Typing...", True, GREY)
typing_text_rect = typing_text.get_rect(topleft=(20, 670))
add_text = pygame.image.load("assets/images/add_text_button.png")
add_text_rect = add_text.get_rect(topleft=(316, 627))

# -- List initialization --
do_list = [{"text":"Sample element", "status":0}]
typing = False
current_input = ""

# -- Main loop --
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if(add_text_rect.collidepoint(event.pos)):
                typing = not typing
        if event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.key == pygame.K_RETURN:
                do_list.append({"text":current_input, "status":0})
                current_input = ""
            else:
                current_input+=event.unicode

    screen.fill(WHITE)
    for item in do_list:
        status = "[ ]" if item["status"]==0 else "[X]"
        text = item["text"] + "   "+ status
        text = FONT_MEDIUM.render(text, True, BLUE)
        text_rect = text.get_rect(topleft=(20, STARTING_HEIGHT))
        screen.blit(text, text_rect)
        STARTING_HEIGHT+=40
    current_input_text = FONT_MEDIUM.render(current_input, True, BLUE)
    current_input_rect = current_input_text.get_rect(topleft=(20, STARTING_HEIGHT))
    screen.blit(current_input_text, current_input_rect)
    STARTING_HEIGHT=31
    screen.blit(add_text, add_text_rect)
    if typing:
        screen.blit(typing_text, typing_text_rect)

    pygame.display.update()