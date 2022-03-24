import sys
import time
import math
import pygame
import threading
import random

# vars
n = 0
score = 0
level_k = 1
new_level_flag = False
personal_best = 0
stop_flag = False
mainloop_stop_flag = False
ans_flag = False
# main pygame stuff
pygame.init()
screen = pygame.display.set_mode((300, 500))
pygame.display.set_caption("TouchColor on PyGame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 30)
# background
background = pygame.image.load('touchcolorbg.png')
background = pygame.transform.scale(background, (300, 500)) 
# text
personal_best_text_surface = pygame.font.SysFont("Calibri", 20).render('PB: ' + str(personal_best), True, (157, 0, 255))
score_text_surface = font.render(str(score), True, (0, 0, 0))
level_text_surface = pygame.font.SysFont("Calibri", 40).render('Level ' + str(score // 10 + 1), True, (0, 0, 0))


def score_update(): # renders scores for pb and current
    global score_text_surface, personal_best_text_surface, score, personal_best
    score_text_surface = font.render(str(score), True, (0, 0, 0))
    if score > personal_best:
        personal_best = score
    personal_best_text_surface = pygame.font.SysFont("Calibri", 20).render('PB: ' + str(personal_best), True, (157, 0, 255))


# main program


class SimpleRect: # just rectangles
    def __init__(self, pos, size, color):
        self.x, self.y = pos
        self.i = 0
        self.size = size
        self.color = color
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def change_color(self, color): # animation of changing color
        global new_level_flag
        self.color = color
        self.i = 0
        tmp = -3.14
        while tmp <= 3.14:
            self.i = (math.cos(tmp) + 1) * 5
            self.surface = pygame.Surface((self.size[0] + self.i * 2, self.size[1] + self.i * 2))
            self.surface.fill(self.color)
            if new_level_flag:
                break
            game_show()
            try: # for case when app is closed, but function is still running
                pygame.display.update()
            except:
                exit()
            tmp += 0.01 / level_k
        self.i = 0
        if new_level_flag:
            exit()
        game_show()
        pygame.display.update()

    def show(self):
        screen.blit(self.surface, (self.x - self.i, self.y - self.i))
        pygame.display.update()


class Button:
    def __init__(self, pos, size, color, target):
        self.i = 0
        self.x, self.y = pos
        self.size = size
        self.color = color
        self.target = target
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        screen.blit(self.surface, (self.x + self.i, self.y + self.i))

    def action(self):  # when button is pressed
        t = threading.Thread(target=lambda: answ(self.color))
        t.start()
        self.i = 0
        tmp = -3.14
        while tmp <= 3.14:
            self.i = (math.cos(tmp) + 1) * 3
            self.surface = pygame.Surface((self.size[0] - self.i * 2, self.size[1] - self.i * 2))
            self.surface.fill(self.color)
            game_show()
            pygame.display.update()
            tmp += 0.01
        self.surface = pygame.Surface((self.size[0], self.size[1]))
        self.surface.fill(self.color)
        self.i = 0
        game_show()
        pygame.display.update()

    def click(self, event): # detection of clicking and later instructions
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.rect.collidepoint(x, y):
                    self.action()


def new_level():
    global score, level_text_surface, personal_best_text_surface, new_level_flag, level_k
    level_k = level_k / 1.1
    pygame.display.update()
    screen.blit(background, (0, 0))
    level_text_surface = pygame.font.SysFont("Calibri", 40).render('Level ' + str(score // 10 + 1), True, (0, 0, 0, 0))
    new_level_show()
    screen.blit(level_text_surface, (150 - level_text_surface.get_size()[0] // 2 - 1, 150 - level_text_surface.get_size()[1] // 2))
    pygame.display.update()
    new_level_show()
    for _ in range(6):
        pygame.display.update()
        new_level_show()
        pygame.display.update()
        time.sleep(0.5)

    new_level_flag = False

def answ(color):
    global score, stop_flag, ans_flag, new_level_flag, score_text_surface, level_k
    present_color = ShowColor.color
    if color == present_color and not ans_flag:
        score += 1
        score_update()
    elif not ans_flag:
        score = 0
        level_k = 1
        score_update()
    if score != 0 and score % 10 == 0:
        new_level_flag = True
    ans_flag = True
    stop_flag = True


def starttimer():
    global stop_flag, ans_flag
    prev_cl = ShowColor.color
    t = threading.Thread(target=lambda: ShowColor.change_color(random.choice([_ for _ in ['red', 'blue', 'purple', 'yellow', 'green', (0, 255, 255)] if _ != prev_cl])))
    t.start()
    timer1sec = threading.Thread(target=wait1sec)
    stop_flag = False
    ans_flag = False
    timer1sec.start()


def wait1sec():
    global stop_flag, new_level_flag, level_k
    if stop_flag:
        sys.exit(0)
    time.sleep(level_k)
    if mainloop_stop_flag:
        exit(0)
    elif new_level_flag:
        new_level()
    starttimer()
    sys.exit(0)


def mainloop():
    starttimer()
    global mainloop_stop_flag
    while True:
        clock.tick(144)
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop_stop_flag = True
                pygame.quit()
                exit(0)
            all_button_click(event)
        if not new_level_flag:
            game_show()
            pygame.display.update()


def all_button_click(event):
    RedButton.click(event)
    GreenButton.click(event)
    PurpleButton.click(event)
    LightBlueButton.click(event)
    YellowButton.click(event)
    BlueButton.click(event)


def game_show():
    screen.blit(background, (0, 0))
    screen.blit(score_text_surface, (150 - score_text_surface.get_size()[0] // 2 - 1, 30))
    screen.blit(personal_best_text_surface, (0, 0))
    RedButton.show()
    GreenButton.show()
    PurpleButton.show()
    LightBlueButton.show()
    YellowButton.show()
    BlueButton.show()
    ShowColor.show()


def new_level_show():
    screen.blit(background, (0, 0))
    screen.blit(level_text_surface, (150 - level_text_surface.get_size()[0] // 2 - 1,150 - level_text_surface.get_size()[1] // 2))
    screen.blit(personal_best_text_surface, (0, 0))
    RedButton.show()
    GreenButton.show()
    PurpleButton.show()
    LightBlueButton.show()
    YellowButton.show()
    BlueButton.show()

RedButton = Button(
    (0, 300),
    (100, 100),
    'red',
    'red'
)
GreenButton = Button(
    (0, 400),
    (100, 100),
    'green',
    'green'
)
PurpleButton = Button(
    (100, 300),
    (100, 100),
    'purple',
    'purple'
)
LightBlueButton = Button(
    (100, 400),
    (100, 100),
    (0, 255, 255),
    (0, 255, 255)
)
YellowButton = Button(
    (200, 300),
    (100, 100),
    'yellow',
    'yellow'
)
BlueButton = Button(
    (200, 400),
    (100, 100),
    'blue',
    'blue'
)
ShowColor = SimpleRect(
    (100, 100),
    (100, 100),
    'blue'
)
mainloop()
