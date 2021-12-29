import pygame


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
