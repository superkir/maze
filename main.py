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
lose = font.render("You Lose!", True, (0, 0, 250))
win = font.render("You Win!", True, (150, 100, 200))

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

    

        for b in blocks:
            if player.rect.colliderect(b.rect):
                window.blit(lose, (215, 190))
                finish = True


            if player.rect.colliderect(treasure):
                window.blit(win, (215, 190))
                finish = True


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player = Player(0, 400, 50, 50, pygame.image.load("sprite1.png"), 5)
            finish = False

    pygame.display.update()
    clock.tick(FPS)

