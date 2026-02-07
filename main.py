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
STARTING_HEIGHT = 51

# -- Screen objects --
screen = pygame.display.set_mode((WIDTH, HEIGHT))
typing_text = FONT_SMALL.render("Typing...", True, GREY)
typing_text_rect = typing_text.get_rect(topleft=(20, 670))
add_text = pygame.image.load("assets/images/add_text_button.png")
add_text_rect = add_text.get_rect(topleft=(316, 627))
complete = FONT_SMALL.render("Complete", True, BLACK)
complete_rect = complete.get_rect(topleft=(30, 5))
incomplete = FONT_SMALL.render("Incomplete", True, GREY)
incomplete_rect = incomplete.get_rect(topleft=(160, 5))

# -- List initialization --
do_list = [{"text":"Sample element", "status":0}]
typing = False
current_input = ""
tab = False

# -- Functions --
def render_item(item):
    text = item["text"]
    text = FONT_MEDIUM.render(text, True, BLUE)
    text_rect = text.get_rect(topleft=(20, y))
    screen.blit(text, text_rect)
    item["rect"] = text_rect

# -- Main loop --
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if(add_text_rect.collidepoint(event.pos)):
                typing = not typing
            if(complete_rect.collidepoint(event.pos)):
                tab = True
            if(incomplete_rect.collidepoint(event.pos)):
                tab = False
            for i in do_list:
                if i["rect"].collidepoint(event.pos) and i["status"] == tab:
                    i["status"] = not i["status"]
                    break
        if event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.key == pygame.K_RETURN:
                do_list.append({"text":current_input, "status":0})
                current_input = ""
                typing = False
            else:
                current_input+=event.unicode

    screen.fill(WHITE)
    # render elements
    y = STARTING_HEIGHT
    for item in do_list:
        if item["status"]==0 and not tab:
            render_item(item)
            y+=40
        if item["status"]==1 and tab:
            render_item(item)
            y+=40
    current_input_text = FONT_MEDIUM.render(current_input, True, BLUE)
    current_input_rect = current_input_text.get_rect(topleft=(20, y))
    screen.blit(current_input_text, current_input_rect)
    screen.blit(add_text, add_text_rect)
    if typing:
        screen.blit(typing_text, typing_text_rect)

    # render tabs
    if tab:
        complete = FONT_SMALL.render("Complete", True, GREY)
        incomplete = FONT_SMALL.render("Incomplete", True, BLACK)
    if not tab:
        complete = FONT_SMALL.render("Complete", True, BLACK)
        incomplete = FONT_SMALL.render("Incomplete", True, GREY)
    screen.blit(complete, complete_rect)
    screen.blit(incomplete, incomplete_rect)
    pygame.draw.line(screen, BLACK, (0, 40), (400, 40))

    pygame.display.update()