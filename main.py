import pygame
import random
import os


def load_image(name, colorkey=None):
    filename = os.path.join('data', name)
    image = pygame.image.load(filename).convert()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__()
        self.image = load_image(path)
        self.rect = self.image.get_rect(center=(x, y))


class Player(Block):
    def __init__(self, path, x, y, speed):
        super().__init__(path, x, y)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x, y, speed_x, speed_y, pad):
        super().__init__(path, x, y)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.pad = pad
        self.active = False
        self.time = 0

    def restart(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.time = pygame.time.get_ticks()
        self.rect.center = (width / 2, height / 2)

    def counter(self):
        cur_time = pygame.time.get_ticks()

        start_counter = 3

        if (cur_time - self.time) <= 700:
            start_counter = 3
        if 700 < (cur_time - self.time) <= 1400:
            start_counter = 2
        if 1400 < (cur_time - self.time) <= 2100:
            start_counter = 1
        if (cur_time - self.time) >= 2100:
            self.active = True

    def actions(self):
        pass

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.actions()

        else:
            self.counter()


pygame.init()
clock = pygame.time.Clock()

size = width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ping Pong')

bg_color = pygame.Color('#2F373F')
accent_color = (27, 35, 43)
middle_strip = pygame.Rect(width / 2 - 2, 0, 4, height)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg_color)
    pygame.draw.rect(screen, accent_color, middle_strip)
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
