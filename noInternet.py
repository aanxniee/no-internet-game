import pygame, random # import pygame modules

pygame.init() # initalize pygame modules
 
screenLength, screenHeight = 600, 300; # game window dimensions
win = pygame.display.set_mode((screenLength, screenHeight)) # (x, y) coordinates
pygame.display.set_caption("TAC No Internet Game")

clock = pygame.time.Clock() # helps to track time (manages FPS)

class Dinosaur(object):
    # attributes of our dinosaur sprite
    def __init__(self):
        self.w = 35
        self.h = 50

        self.x = 100
        self.y = screenHeight - 150

        self.jumping = False # bool to track if the dinosaur is jumpibg
        self.jumpIncrement = 0 # counter to replicate gravity

        self.crouching = False # bool to track if the dinosaur is crouching

        # import sprite images
        self.run_img = [pygame.image.load("run1.png"), pygame.image.load("run2.png")]
        self.crouch_img = [pygame.image.load("crouch1.png"), pygame.image.load("crouch2.png")]
        self.jump_img = pygame.image.load("jump.png")

        self.runInc  = 0 # counter to animate between the two run costumes
        self.crouchInc = 0 # counter to animate between the two crouch cosutumes

    def draw(self):
        # blit will draw the image to our window
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

        # detects if the up/space keys are pressed (detects jumping), ensures we cannot jump out of crouching
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.jumping and not self.crouching: 
            self.jumping = True

        # detects if the down key is pressed (detects crouching), ensures we cannot crouch out of jumping
        if (keys[pygame.K_DOWN]) and not self.jumping:
            self.crouching = True
            self.w = 50
            self.h = 25
            self.y = screenHeight - 125
        
        # neither jumping or crocuhing
        elif not self.jumping:
            self.crouching = False
            self.y = screenHeight - 150
            self.w = 35
            self.h = 50

        # we use jumpIncrement to recreate gravity --> parabolic jump
        if self.jumping:
            if self.jumpIncrement <= 20:
                self.y -= (10 - self.jumpIncrement) * 2
                self.jumpIncrement += 1
            else:
                self.jumpIncrement = 0
                self.jumping = False

class Cactus(object):
    # attributes of our cactus sprite
    def __init__(self):
        self.img = pygame.image.load("cactus.png")

        # we have two types of cacti, large and small
        if random.randint(1, 2) == 1:
            self.w = 25
            self.h = 50
            self.big = True

        else:
            self.w = 48
            self.h = 25
            self.big = False
            # if it is a small cactus, we will scale the sprite down
            self.img = pygame.transform.scale(self.img, (15, self.h))

        self.y = (screenHeight - 98) - self.h
        self.x = screenLength
    
    def draw(self):
        if self.big:
            win.blit(self.img, (self.x, self.y))
        else:
            # small cactus is comprised of four scaled down large cacti
            win.blit(self.img, (self.x, self.y-10))
            win.blit(self.img, (self.x+12, self.y-10))
            win.blit(self.img, (self.x+24, self.y-10))
            win.blit(self.img, (self.x+36, self.y-10))

    # check if the cactus touches the dinosaur, detects collision
    def hit(self):
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
            return True
        return False

class Bird(object):
    # attributes of our bird sprite
    def __init__(self):
        self.w = 50
        self.h = 25

        self.y = (screenHeight-100) - (self.h + 10) * random.randint(1,3) # bird can spawn are random heights
        self.x = screenLength

        self.flying = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png")]
        self.fly_inc = 0

    def draw(self):
        win.blit(self.flying[self.fly_inc//10], (self.x, self.y))

        if self.fly_inc == 19:
            self.fly_inc = -1
        self.fly_inc +=1 

    def hit(self):
        # check if the bird touches the dinosaur, detects collision
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
            return True
        return False

player = Dinosaur() # create the dinosaur object
enemies = [] # list to store the enemies (cactus and birds) that spawn on our screen

increment = 0 # counter
gameSpeed = 1 # speed at which enemies move/spawn

score = 0 # player's score
scoreIncrement = 0 # rate at which score increases

# ------- MAIN GAME LOOP -------
run = True
end = True

while run:
    win.fill((255,255,255)) # fill window to white
    pygame.draw.rect(win, (0,0,0), (0, screenHeight-110, screenLength, 1)) # draws the ground

    for event in pygame.event.get():
        # allows the user to close window
        if event.type == pygame.QUIT:
            run = False
            end = False
    
    increment += 1 * gameSpeed

    # as time goes on, difficulty of the game will increase
    if increment >= 100:
        if random.randint(1,2) == 1 and score >= 100:
            enemies.append(Bird()) # spawn birds
        else:
            enemies.append(Cactus()) # spawn cactus

        increment = 0
        gameSpeed += 0.1 # increase game speed for difficulty

    # score increases faster as difficulty increases
    if scoreIncrement <= 5:
        scoreIncrement += 1 * gameSpeed
    else:
        scoreIncrement = 0
        score += 1
        
    # moves the enemies across the screen by changing its x value
    for enemy in enemies:
        enemy.x -= 5 * gameSpeed 
        enemy.draw() # draw the object to the screen

        # if there is collision, stop the game
        if enemy.hit():
            run = False
        
        # if the enemy reaches the leftmost side of the screen, remove it (frees memory)
        if enemy.x + enemy.w == 0:
            enemies.remove(enemy)
        
    player.draw()
    player.move()

    # display the score
    font = pygame.font.SysFont("arial", 25)
    text = font.render(str(score), 1, (0,0,0))
    win.blit(text, (screenLength - text.get_width() - 20, 15))

    clock.tick(30) # 30 fps
    pygame.display.update() # render everything to the screen

# if the user loses, display an ending screen
while end:
    win.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False

    # final score and exit message
    font = pygame.font.SysFont("arial", 25)
    finalScore = font.render("Your score: " + str(score), 1, (255,255,255))
    exitScreen = font.render("Click anywhere to exit", 1, (255, 255, 255))
    win.blit(finalScore, (screenLength/2 - finalScore.get_width()/2, screenHeight * 1/3 + 15))
    win.blit(exitScreen, (screenLength/2 - exitScreen.get_width()/2, screenHeight * 2/5 + 20))

    # allows the user to exit the game via a mouse click
    if pygame.mouse.get_pressed()[0]: # [0] represents a left click
        end = False

    pygame.display.update() # render everything to the screen

pygame.quit() # uninitialize pygame modules


