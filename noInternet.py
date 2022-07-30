import pygame, random

pygame.init()

screenLength = 600;
screenHeight = 300;

# double parenthesis for coordinates
win = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("TAC No Internet Game")

clock = pygame.time.Clock()

class Dinosaur(object):
    def __init__(self):
        self.w = 35
        self.h = 50
        self.x = 100
        self.y = screenHeight - 150

    def draw(self):
        pygame.draw.rect(win, (125,125,125), (self.x, self.y, self.w, self.h))

player = Dinosaur()

run = True
while run:
    win.fill((255,255,255)) # fill window to white
    for event in pygame.event.get():
        # allows user to close window
        if event.type == pygame.QUIT:
            run = False

    player.draw()

    clock.tick(30) # 30 fps
    pygame.display.update()


pygame.quit()


