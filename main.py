import pygame
import random
import os
import sys


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


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Игра 'Ping Pong'", "",
                  "Правила игры",
                  "После подачи мяча, нужно отбить его ракеткой",
                  "главная задача: не пропустить мяч"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


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

        if (cur_time - self.time) <= 1400:
            start_counter = 3
        if 1400 < (cur_time - self.time) <= 2100:
            start_counter = 2
        if 2100 < (cur_time - self.time) <= 2800:
            start_counter = 1
        if (cur_time - self.time) >= 2800:
            self.active = True
        time_counter = font.render(str(start_counter), True, grey_color)
        time_counter_rect = time_counter.get_rect(center=(width / 2, height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

    def actions(self):
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.speed_y *= -1
        if pygame.sprite.spritecollide(self, self.pad, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.pad, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.actions()

        else:
            self.counter()


class Computer(Block):
    def __init__(self, path, x, y, speed):
        super().__init__(path, x, y)
        self.speed = speed

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.screen_constrain()


class GameRunner:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.computer_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()


pygame.init()
clock = pygame.time.Clock()

size = width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ping Pong')

bg_color = pygame.Color('#2F373F')
grey_color = pygame.Color('grey')
font = pygame.font.Font(None, 50)
middle_strip = pygame.Rect(width / 2 - 2, 0, 4, height)

start_screen()

player = Player('Paddle.png', width - 20, height / 2, 5)
computer = Computer('Paddle.png', 20, width / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(computer)

ball = Ball('Ball.png', width / 2, height / 2, 4, 4, paddle_group)
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

game_manager = GameRunner(ball_group, paddle_group)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    screen.fill(pygame.Color('white'))
    pygame.draw.rect(screen, grey_color, middle_strip)

    game_manager.run_game()

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
