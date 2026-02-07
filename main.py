import pygame, sys, json, os
from pygame.locals import *
pygame.init()

# -- Constants --
WIDTH = 400
HEIGHT = 711
BLUE = "#004CFF"
LIGHT_BLUE = "#5B8CFF"
RED = "#FF0000"
GREEN = "#2BFF00"
BLACK = "#000000"
WHITE = "#FFFFFF"
GREY = "#606060"
FONT_SMALL = pygame.font.SysFont("arialrounded", 20)
FONT_MEDIUM = pygame.font.SysFont("arialrounded", 30)
FONT_BIG = pygame.font.SysFont("arialrounded", 40)
STARTING_HEIGHT = 51
LINE_LENGHT = 17
COLOR_CODE = {
    "BLUE":BLUE,
    "LIGHT_BLUE":LIGHT_BLUE
}
HEX_TO_KEY = {v: k for k, v in COLOR_CODE.items()}

# -- JSON --
def load_data():
    with open("assets/data/tasks.json") as f:
        data = json.load(f)

        for task in data:
            task["color"] = COLOR_CODE[task["color"]]

    return data

def save_data(tasks):
    os.makedirs("assets/data", exist_ok=True)
    tasks_to_save = []
    for task in tasks:
        to_save = {
            "text":task["text"],
            "status":task["status"],
            "color":HEX_TO_KEY[task["color"]]
        }
        tasks_to_save.append(to_save)
    with open("assets/data/tasks.json", "w") as f:
        json.dump(tasks_to_save, f, indent=2)

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
checkbox_empty = pygame.image.load("assets/images/checkbox_empty.png")
checkbox_empty = pygame.transform.scale(checkbox_empty, (32, 32))
checkbox_tick = pygame.image.load("assets/images/checkbox_tick.png")
checkbox_tick = pygame.transform.scale(checkbox_tick, (32, 32))

# -- List initialization --
do_list = load_data()
typing = False
current_input = ""
tab = False

# -- Functions --
def render_item(item, y):
    text = item["text"]
    if len(text)<=17:
        text = FONT_MEDIUM.render(text, True, item["color"])
        text_rect = text.get_rect(topleft=(20, y))
        screen.blit(text, text_rect)
        if item["status"] == 0:
            screen.blit(checkbox_empty, (348, y+5))
        else:
            screen.blit(checkbox_tick, (348, y+5))
        item["rect"] = text_rect
        return y
    else:
        words = text.split(" ")
        lines = []
        for word in words:
            if len(lines)==0:
                lines.append(word+" ")
            elif len(lines[-1]+word)<=17:
                lines[-1]+=word+" "
            else:
                lines.append(word+" ")
        starting_y = y
        for line in lines:
            text = FONT_MEDIUM.render(line, True, item["color"])
            text_rect = text.get_rect(topleft=(20, y))
            screen.blit(text, text_rect)
            y+=35
        text_rect = Rect(20, starting_y, 325, y-starting_y)
        item["rect"] = text_rect
        if item["status"] == 0:
            screen.blit(checkbox_empty, (348, (starting_y+y)/2-5))
        else:
            screen.blit(checkbox_tick, (348, (starting_y+y)/2-5))
        return y-35

# -- Main loop --
while True:
    MOUSE_POS = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if(add_text_rect.collidepoint(MOUSE_POS)):
                typing = not typing
            if(complete_rect.collidepoint(MOUSE_POS)):
                tab = True
            if(incomplete_rect.collidepoint(MOUSE_POS)):
                tab = False
            for i in do_list:
                if "rect" in i:
                    if i["rect"].collidepoint(MOUSE_POS) and i["status"] == tab:
                        i["status"] = not i["status"]
                        save_data(do_list)
                        break
        if event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.key == pygame.K_RETURN:
                do_list.append({"text":current_input, "status":0, "color":BLUE})
                current_input = ""
                typing = False
                save_data(do_list)
            else:
                current_input+=event.unicode

    screen.fill(WHITE)
    # Render elements
    y = STARTING_HEIGHT
    for item in do_list:
        if item["status"]==0 and not tab:
            y = render_item(item, y)
            y+=40
        if item["status"]==1 and tab:
            y = render_item(item, y)
            y+=40
    current_input_text = FONT_MEDIUM.render(current_input, True, BLUE)
    current_input_rect = current_input_text.get_rect(topleft=(20, y))
    screen.blit(current_input_text, current_input_rect)
    screen.blit(add_text, add_text_rect)
    if typing:
        screen.blit(typing_text, typing_text_rect)

    # Render tabs
    if tab:
        complete = FONT_SMALL.render("Complete", True, GREY)
        incomplete = FONT_SMALL.render("Incomplete", True, BLACK)
    if not tab:
        complete = FONT_SMALL.render("Complete", True, BLACK)
        incomplete = FONT_SMALL.render("Incomplete", True, GREY)
    screen.blit(complete, complete_rect)
    screen.blit(incomplete, incomplete_rect)
    pygame.draw.line(screen, BLACK, (0, 40), (400, 40))

    # Effects
    for i in do_list:
        if "rect" in i:
            if i["rect"].collidepoint(MOUSE_POS) and i["status"] == tab:
                i["color"] = LIGHT_BLUE
            else:
                i["color"] = BLUE

    pygame.display.update()