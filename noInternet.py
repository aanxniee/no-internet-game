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

class Bird(object):
    def __init__(self):
        self.w = 50
        self.h = 25
        self.y = (screenHeight-100) - (self.h + 10) * random.randint(1,3)
        self.x = screenLength
        self.flying = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png")]
        self.fly_inc = 0

    def draw(self):
        win.blit(self.flying[self.fly_inc//10], (self.x, self.y))

        if self.fly_inc == 19:
            self.fly_inc = -1
        self.fly_inc +=1 

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
end = True

while run:
    win.fill((255,255,255)) # fill window to white
    pygame.draw.rect(win, (0,0,0), (0, screenHeight-110, screenLength, 1))
    for event in pygame.event.get():
        # allows user to close window
        if event.type == pygame.QUIT:
            run = False
            end = False
    
    # spawns cactus every 100 increment
    inc += 1 * gameSpeed # spawn enemy closer together for difficulty
    if inc >= 100:
        if random.randint(1,2) == 1 and score >= 100:
            enemies.append(Bird())
        else:
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
        
        if enemy.x + enemy.w == 0:
            enemies.remove(enemy)
        
    player.draw()
    player.move()

    # display score
    font = pygame.font.SysFont("arial", 25)
    text = font.render(str(score), 1, (0,0,0))
    win.blit(text, (screenLength - text.get_width() - 20, 15))

    clock.tick(30) # 30 fps
    pygame.display.update()

while end:
    win.fill((0,0,0))

    for event in pygame.event.get():
        # allows user to close window
        if event.type == pygame.QUIT:
            end = False

    font = pygame.font.SysFont("arial", 25)
    finalScore = font.render("Your score: " + str(score), 1, (255,255,255))
    exitScreen = font.render("Click anywhere to exit", 1, (255, 255, 255))
    win.blit(finalScore, (screenLength/2 - finalScore.get_width()/2, screenHeight * 1/3 + 15))
    win.blit(exitScreen, (screenLength/2 - exitScreen.get_width()/2, screenHeight * 2/5 + 20))

    if pygame.mouse.get_pressed()[0]:
        end = False

    pygame.display.update()

pygame.quit()


