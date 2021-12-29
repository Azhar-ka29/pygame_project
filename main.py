import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
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
