#Gabe Keener
#5/3/2021
#Summary: This code allows the user to play a simple shooter game using pygame

import pygame
import os
import time
import random
from pygame import mixer
pygame.font.init()

#Starting pygame music mixer
mixer.init()
mixer.music.set_volume(0.5)
pygame.mixer.music.load("background music.wav")



#Setting up game window
WIDTH, HEIGHT = 1000, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Covid Capture!")
    
    
#Game Assets
COVIDVIRUS = pygame.image.load(os.path.join("assets", "virus.png"))
VIRUS = pygame.image.load(os.path.join("assets", "virus2.png"))
BACTERIA = pygame.image.load(os.path.join("assets", "bacteria.png"))

#Player
PLAYER = pygame.image.load(os.path.join("assets", "bandage.png"))

#Shots
RED = pygame.image.load(os.path.join("assets", "red.png"))
GREEN = pygame.image.load(os.path.join("assets", "green.png"))
BLUE = pygame.image.load(os.path.join("assets", "blue.png"))
VACCINE = pygame.image.load(os.path.join("assets", "pill.png"))

#Background
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "empty area.jpg")), (WIDTH, HEIGHT))

#setting up player shooting
class Shot:
    def __init__(self, x, y, image):
        self.x = x + 70
        self.y = y + 50
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
    def draw (self, window):
        window.blit(self.image, (self.x, self.y))
    def move(self, vel):
        self.x += vel
    def offScreen(self, height):
        return not(self.y <= height and self.y >= 0)
    def collision(self, obj):
        return collide(self, obj)


#Inherting class
class Needle:
    COOLDOWN = 30
    
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.needleImage = None
        self.laserImage = None
        self.lasers = []
        self.coolDownCounter = 0

    def draw(self, window):
        window.blit(self.needleImage, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def moveLasers(self, vel, obj):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offScreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.laser.remove(laser)

    def coolDown(self):
        if self.coolDownCounter >= self.COOLDOWN:
            self.coolDownCounter = 0
        elif self.coolDownCounter > 0:
            self.coolDownCounter += 1

    def shoot(self):
        if self.coolDownCounter == 0:
            laser = Shot(self.x, self.y, self.laserImage)
            self.lasers.append(laser)
            self.coolDownCounter = 1

    def getWidth(self):
        return self.needleImage.get_width()

    def getHeight(self):
        return self.needleImage.get_height()

#health class/player info
class User(Needle):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.needleImage = PLAYER
        self.laserImage = VACCINE
        self.mask = pygame.mask.from_surface(self.needleImage)
        self.maxHealth = health

    def moveLasers(self, vel, objs):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offScreen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

                        
    def draw(self, window):
        super().draw(window)
        self.healthBar(window)

    def healthBar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.needleImage.get_height() + 10, self.needleImage.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.needleImage.get_height() + 10, self.needleImage.get_width() * (self.health / self.maxHealth), 10))

        
#Enemy class
class Virus(Needle):
    COLORMAP = {
        "red": (COVIDVIRUS, RED),
        "green": (VIRUS, GREEN),
        "blue": (BACTERIA, BLUE)
        }
    
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.needleImage, self.laserImage = self.COLORMAP[color]
        self.mask = pygame.mask.from_surface(self.needleImage)

    def move(self, vel):
        self.x += vel

    
#collision class
def collide(obj1, obj2):
    offsetX = obj2.x - obj1.x
    offsetY = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offsetX, offsetY)) != None
        


#main loop
def main():

    #Setting music to loop until game is over
    pygame.mixer.music.play(-1)

    #Setting up FPS/level/lives/font of game
    run = True
    FPS = 60
    level = 0
    lives = 3  
    font = pygame.font.SysFont("times new roman", 50)
    lostFont = pygame.font.SysFont("times new roman", 80)


    #Enemy movment
    enemies = []
    waveLength = 5
    enemyVelocity = 2
    
    #player movement
    velocity = 5

    #laser speed
    laserVelocity = 5

    #constructing player spawn
    needle = User(300, 590)
    
    clock = pygame.time.Clock()

    lost = False
    lostCounter = 0

    def redrawWindow():
        WINDOW.blit(bg, (0, 0))

        #making lives/level text
        livesText = font.render(f"Lives: {lives}", 1, (44, 228, 225))
        levelText = font.render(f"Level: {level}", 1, (44, 228, 225))

        WINDOW.blit(livesText, (10, 10))
        WINDOW.blit(levelText, (WIDTH - levelText.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        needle.draw(WINDOW)

        if lost:
            lostLabel = lostFont.render("You Lose", 1, (241, 10, 10))
            WINDOW.blit(lostLabel, (WIDTH/2 - lostLabel.get_width()/2, 350))
        
        pygame.display.update()
        
        
    
    
    #Setting up QUIT event
    while run:
        clock.tick(FPS)
        redrawWindow()

        if lives <= 0 or needle.health <= 0:
            lost = True
            lostCounter += 1

        if lost:
            if lostCounter > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            
            waveLength += 5
            for i in range(waveLength):
                enemy = Virus(random.randrange(-1500, -100), random.randrange(50, HEIGHT - 100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        




        #setting up key actions
        pressedkeys = pygame.key.get_pressed()

        #moving player left
        if pressedkeys[pygame.K_a]and needle.x + velocity > 0:
            needle.x -= velocity

        #moving player right
        if pressedkeys[pygame.K_d]and needle.x + velocity + needle.getWidth() < WIDTH:
            needle.x += velocity

        #moving player up
        if pressedkeys[pygame.K_w]and needle.y - velocity > 0:
            needle.y -= velocity

        #moving player down
        if pressedkeys[pygame.K_s] and needle.y + velocity + needle.getHeight() + 15 < HEIGHT:
            needle.y += velocity

        #allowing the player to shoot
        if pressedkeys[pygame.K_SPACE]:
            needle.shoot()
        
        for enemy in enemies[:]:
            enemy.move(enemyVelocity)
            enemy.moveLasers(laserVelocity, needle)


            #enemy shoot mechanic
            #if random.randrange(0, 120) == 1:
                #enemy.shoot()

            #setting up player collision
            if collide(enemy, needle):
                needle.health -= 10
                enemies.remove(enemy)
            
            #enemy damage
            elif enemy.x + enemy.getHeight() > WIDTH:
                lives -= 1
                enemies.remove(enemy)


        needle.moveLasers(-laserVelocity, enemies)

        
#main menu screen
def mainMenu():
    titleFont = pygame.font.SysFont("times new roman", 41)
    run = True
    while run:
        WINDOW.blit(bg, (0, 0))
        title = titleFont.render("Press the mouse button when you are ready", 1, (255, 255, 255))
        WINDOW.blit(title, (WIDTH / 2 - title.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
    

mainMenu()
        









    
