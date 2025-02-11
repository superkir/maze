import pygame
from map1 import *

pygame.init()

FPS = 70
clock = pygame.time.Clock()
#створи вікно гри

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption("Maze")

#завантаження музики
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

#задай фон сцени
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (wind_w, wind_h))

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self, a, d, s, w):
        keys = pygame.key.get_pressed()
        if keys[a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[d]:
            if self.rect.right < wind_w:
                self.rect.x += self.speed
        if keys[s]:
            if self.rect.bottom < wind_h:
                self.rect.y += self.speed
        if keys[w]:
            if self.rect.y > 0:
                self.rect.y -= self.speed

class Enemy(Sprite):
    def __init__(self, x, y, w, h, image1, image2, speed, x2, direction = "right"):
        super().__init__(x, y, w, h, image1)
        self.image_right = self.image
        self.image_left = pygame.transform.scale(image2, (w, h))
        self.speed = speed
        self.x1 = x
        self.x2 = x2
        self.direction = direction

    def move(self):
        if self.rect.x >= self.x2:
            self.rect.x = self.x2
            self.direction = "left"
            self.image = self.image_left
        elif self.rect.x <= self.x1:
            self.rect.x = self.x1
            self.direction = "right"
            self.image = self.image_right
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Enemy1(Sprite):
    def __init__(self, x, y, w, h, image1, image2, speed, x2, direction = "left"):
        super().__init__(x, y, w, h, image2)
        self.image_left = self.image
        self.image_right = pygame.transform.scale(image1, (w, h))
        self.speed = speed
        self.x1 = x
        self.x2 = x2
        self.direction = direction

    def move(self):
        if self.rect.x <= self.x2:
            self.rect.x = self.x2
            self.direction = "right"
            self.image = self.image_right
        elif self.rect.x >= self.x1:
            self.rect.x = self.x1
            self.direction = "left"
            self.image = self.image_left
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

enem_img1 = pygame.image.load("cyborg.png")
enem_img2 = pygame.transform.flip(enem_img1, True, False)
enemy_img1 =  pygame.image.load("cyborg.png")
enemy_img2 = pygame.transform.flip(enem_img1, True, False)
enemy = Enemy(423, 350, 50, 50, enem_img1, enem_img2, 5, 628)
enemy1 = Enemy1(626, 450, 50, 50, enemy_img1, enemy_img2, 5, 124)
player = Player(0, 400, 50, 50, pygame.image.load("sprite1.png"), 5)

blocks = []
block_size = 25

block_img = pygame.image.load("1.png")

x, y = 0, 0

img_gold = pygame.image.load("treasure.png")
treasure = Sprite(650, 250, 50, 50, img_gold)

for row in lvl1:
    for tile in row:
        if tile == "1":
            blocks.append(Sprite(x, y, block_size, block_size, block_img))
        elif tile == "2":
            treasure = Sprite(x, y, 50, 50, img_gold)
        x += block_size
    x = 0
    y += block_size

font = pygame.font.SysFont("Arial", 80)
font1 = pygame.font.SysFont("Arial", 30)
lose = font.render("You Lose!", True, (0, 0, 250))
win = font.render("You Win!", True, (150, 100, 200))
lose1 = font1.render("Press SPACE to play again", True, (255, 255, 102))
win1 = font1.render("Press SPACE to play again", True, (255, 255, 102))


finish = False
print(len(blocks))
game = True
while game:

    if not finish:
    
        window.blit(background, (0, 0))
        treasure.draw()
        for b in blocks:
            b.draw()
            
        player.draw()
        player.move(pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w)

        enemy.draw()
        enemy.move()
        enemy1.draw()
        enemy1.move()

    

        for b in blocks:
            if player.rect.colliderect(b.rect):
                window.blit(lose, (215, 120))
                window.blit(lose1, (215, 200))
                finish = True

            if player.rect.colliderect(enemy):
                window.blit(lose, (215, 120))
                window.blit(lose1, (215, 200))
                finish = True

            if player.rect.colliderect(enemy1):
                window.blit(lose, (215, 120))
                window.blit(lose1, (215, 200))
                finish = True


            if player.rect.colliderect(treasure):
                window.blit(win, (215, 120))
                window.blit(win1, (215, 200))
                finish = True


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player = Player(0, 400, 50, 50, pygame.image.load("sprite1.png"), 5)
            finish = False

    pygame.display.update()
    clock.tick(FPS)

