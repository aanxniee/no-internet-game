import pygame, random

pygame.init()

screenLength = 600;
screenHeight = 300;

# double parenthesis for coordinates
win = pygame.display.set_mode((screenLength, screenHeight))

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        # allows user to close window
        if event.type == pygame.QUIT:
            run = False

    clock.tick(30) # 30 fps
    pygame.display.update()


pygame.quit()


