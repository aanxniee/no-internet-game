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
        self.run_img = [pygame.image.load("run1.png"), pygame.image.load("run2.png")]
        self.crouch_img = [pygame.image.load("crouch1.png"), pygame.image.load("crouch2.png")]
        self.jump_img = pygame.image.load("jump.png")
        self.crouchInc = 0
        self.runInc  = 0

    def draw(self):

        if self.jumping:
            win.blit(self.jump_img, (self.x, self.y))

        elif self.crouching:
            win.blit(self.crouch_img[self.crouchInc//5], (self.x, self.y))

            if self.crouchInc == 9:
                self.crouchInc = -1
            self.crouchInc += 1

        else:
            win.blit(self.run_img[self.runInc//5], (self.x, self.y))

            if self.runInc == 9:
                self.runInc = -1
            self.runInc += 1


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
        self.img = pygame.image.load("cactus.png")

        # large cactus and small cactus
        if random.randint(1, 2) == 1:
            self.w = 25
            self.h = 50
            self.big = True
        else:
            self.w = 48
            self.h = 25
            self.big = False
            self.img = pygame.transform.scale(self.img, (15, self.h))

        self.y = (screenHeight - 98) - self.h
        self.x = screenLength
    
    def draw(self):
        if self.big:
            win.blit(self.img, (self.x, self.y))
        else:
            win.blit(self.img, (self.x, self.y-10))
            win.blit(self.img, (self.x+12, self.y-10))
            win.blit(self.img, (self.x+24, self.y-10))
            win.blit(self.img, (self.x+36, self.y-10))

    # detects collision
    def hit(self):
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
            return True
        return False

player = Dinosaur() # create dinosaur object
enemies = []
inc = 0
gameSpeed = 1
score = 0
scoreIncrement = 0

run = True
while run:
    win.fill((255,255,255)) # fill window to white
    pygame.draw.rect(win, (0,0,0), (0, screenHeight-110, screenLength, 1))
    for event in pygame.event.get():
        # allows user to close window
        if event.type == pygame.QUIT:
            run = False
    
    # spawns cactus every 100 increment
    inc += 1 * gameSpeed # spawn enemy closer together for difficulty
    if inc >= 100:
        enemies.append(Cactus())
        inc = 0
        gameSpeed += 0.1

    # make score increase faster as difficulty increases
    if scoreIncrement <= 5:
        scoreIncrement += 1 * gameSpeed
    else:
        scoreIncrement = 0
        score += 1
        
    # moves the cactus across the screen
    for enemy in enemies:
        enemy.x -= 5 * gameSpeed # make enemy move fastr for difficulty
        enemy.draw() 

        if enemy.hit():
            run = False
        
    player.draw()
    player.move()

    # display score
    font = pygame.font.SysFont("poppins", 50)
    text = font.render(str(score), 1, (0,0,0))
    win.blit(text, (screenLength - text.get_width() - 10, 10))

    clock.tick(30) # 30 fps
    pygame.display.update()


pygame.quit()


