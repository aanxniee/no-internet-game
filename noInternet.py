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
        self.jumping = False
        self.jump_increment = 0
        self.crouching = False

    def draw(self):
        pygame.draw.rect(win, (125,125,125), (self.x, self.y, self.w, self.h))

    def move(self):
        keys = pygame.key.get_pressed()

        # detects jumping, no jumping out of crouching
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.jumping and not self.crouching: 
            self.jumping = True

        # detects crouching, no crouching out of jumping
        if (keys[pygame.K_DOWN]) and not self.jumping:
            self.crouching = True
            self.w = 50
            self.h = 25
            self.y = screenHeight - 125
        elif not self.jumping:
            self.crouching = False
            self.y = screenHeight - 150
            self.w = 35
            self.h = 50

        if self.jumping: # parabolic jump
            if self.jump_increment <= 20:
                self.y -= (10 - self.jump_increment) * 2
                self.jump_increment += 1
            else:
                self.jump_increment = 0
                self.jumping = False

class Cactus(object):
    def __init__(self):
        # large cactus and small cactus
        if random.randint(1, 2) == 1:
            self.w = 25
            self.h = 50
            self.big = True
        else:
            self.w = 48
            self.h = 25
            self.big = False

        self.y = (screenHeight - 100) - self.h
        self.x = screenLength
    
    def draw(self):
        pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.w, self.h))

    def hit(self):
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
            return True
        return False

player = Dinosaur() # create dinosaur object
enemies = []
inc = 0

run = True
while run:
    win.fill((255,255,255)) # fill window to white
    pygame.draw.rect(win, (0,0,0), (0, screenHeight-100, screenLength, 100))
    for event in pygame.event.get():
        # allows user to close window
        if event.type == pygame.QUIT:
            run = False
    
    # spawns cactus every 100 increment
    inc += 1
    if inc == 100:
        enemies.append(Cactus())
        inc = 0

    # moves the cactus across the screen
    for enemy in enemies:
        enemy.x -= 5
        enemy.draw()

        if enemy.hit():
            run = False
        
    player.draw()
    player.move()

    clock.tick(30) # 30 fps
    pygame.display.update()


pygame.quit()


