from pygame import *
from random import choice, randint
import pickle
import sys

init()
mixer.init()
font.init()

#створи вікно гри
TILESIZE = 45
MAP_WIDTH, MAP_HEIGHT = 20, 15
WIDTH, HEIGHT = TILESIZE*MAP_WIDTH, TILESIZE*MAP_HEIGHT
FPS = 60

window = display.set_mode((WIDTH, HEIGHT)) #створюємо вікно 
display.set_caption("Maze")
clock = time.Clock() # Створюємо ігровий таймер

font1 = font.SysFont("Impact",35)
font2 = font.SysFont("Impact",50)

# mixer.music.load("space.ogg") 
# mixer.music.set_volume(0.2)
# mixer.music.play(loops=-1)

fire_sound = mixer.Sound('fire.ogg')

#задай фон сцени
bg = image.load("bg_castle.png") # завантажуємо картинку в гру
bg = transform.scale(bg, (WIDTH, HEIGHT)) #змінюємо розмір картинки
# bg_y1 = 0
# bg_y2 = -HEIGHT
# bg_speed = 2
player_img = image.load('Survivor.png')
enemy1_img = image.load('__Bat02_Idle_001.png')
enemy2_img = image.load('frame-2.png')
bullet_img  = image.load('pngwing.com (1).png')
wall_img = image.load('stone_gray2.png')
treasure_img = image.load('dngn_closed_door.png')
coins_img = image.load('coin 2.png')
apples_img = image.load('apple.png')
sprites = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.right_image = self.image
        self.left_image = transform.flip(self.image,flip_x=True,flip_y=False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)


class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)
        self.hp = 5
        self.damage = 1
        self.coins = 0
        self.speed = 5
        self.dir = "right"

    def update(self):
        global hp_label
        self.old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed() #отримуємо список натиснутих клавіш
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.dir = "left"
            self.image = self.left_image
        if keys[K_d] and self.rect.right < WIDTH    :
            self.rect.x += self.speed
            self.dir = "right"
            self.image = self.right_image

        collidelist = sprite.spritecollide(self, walls, False)
        if len(collidelist) > 0: # при зіткненні будь-якого спрайту з spritegroup1 із будьяким спрайтом з spritegroup2
            self.rect.x, self.rect.y = self.old_pos 

    def fire(self):
        bullet = Bullet(self.dir,self.rect.centerx, self.rect.centery +15)
        fire_sound.play()

enemys = sprite.Group()
class Enemy(GameSprite):
    def __init__(self,enemy_img, x, y):
        super().__init__(enemy_img, TILESIZE, TILESIZE-10, x, y)
        self.rect.centery=y
        self.hp = 3
        self.damage = 1
        self.speed = 5
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = choice(self.dir_list)
        enemys.add(self)

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        if self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed
        
        collidelist = sprite.spritecollide(self, walls, False)
        if len(collidelist) > 0: # при зіткненні будь-якого спрайту з spritegroup1 із будьяким спрайтом з spritegroup2
            self.rect.x, self.rect.y = self.old_pos 
            self.dir = choice(self.dir_list)

bullets =  sprite.Group()
class Bullet(GameSprite):
    def __init__(self,dir,player_x,player_y):
        super().__init__(bullet_img,20,40,player_x,player_y)
        self.rect.centerx = player_x
        self.rect.bottom = player_y
        self.speed = 5
        bullets.add(self)
        self.dir=dir
        if self.dir == "left":
            self.image = transform.flip(self.image,flip_x=True,flip_y=False)
       


    def update(self):
        if self.dir == "right":
            self.rect.x += self.speed 
        if self.dir == "left":
            self.rect.x -= self.speed
        if self.rect.y < 0 :
            self.kill()

walls = sprite.Group()

class Wall(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall_img, TILESIZE, TILESIZE, x, y)
        walls.add(self)

player = Player(player_img, TILESIZE, TILESIZE,  300, 300)
coins = sprite.Group()
apples = sprite.Group()
treasure = sprite.Group()
hp_label = font1.render(f"HP: {player.hp}",True,(255,255,255))  
GG_text = font2.render("You loose", True,(255,0,0))
coins_label = font1.render(f"coins: {player.coins}",True,(255,255,255))
GG = False

with open("lvl1.txt", "r") as file: 
    x, y = 0, 0
    map = file.readlines()
    for row in map:
        for symbol in row:
            if symbol == 'W':
                Wall(x,y)
            elif symbol == 'E':
                Enemy(enemy2_img,x,y)
            elif symbol == 'P':
                player.rect.x = x
                player.rect.y = y
                player.start_x, player.start_y = x,y
            elif symbol == "T":
                treasure  = GameSprite(treasure_img,TILESIZE,TILESIZE,x,y)
            elif symbol == "C":
                coins.add(GameSprite(coins_img,TILESIZE,TILESIZE,x,y))
            elif symbol == "A":
                apples.add(GameSprite(apples_img,TILESIZE,TILESIZE,x,y))
            x += TILESIZE
        y+=TILESIZE
        x = 0

# TILESIZE = 45
# MAP_WIDTH, MAP_HEIGHT = 25, 20
# WIDTH, HEIGHT = TILESIZE*MAP_WIDTH, TILESIZE*MAP_HEIGHT
# FPS = 60

# with open("lvl2.txt", "r") as file:
#     x, y = 0, 0
#     map = file.readlines()
#     for row in map:
#         for symbol in row:
#             if symbol == 'W':
#                 Wall(x,y)
#             elif symbol == 'E':
#                 Enemy(enemy2_img,x,y)
#             elif symbol == 'P':
#                 player.rect.x = x
#                 player.rect.y = y
#                 player.start_x, player.start_y = x,y
#             elif symbol == "T":
#                 treasure  = GameSprite(exit_img,TILESIZE,TILESIZE,x,y)
#             elif symbol == "C":
#                 coins.add(GameSprite(coins_img,TILESIZE,TILESIZE,x,y))
#             elif symbol == "A":
#                 apples.add(GameSprite(apples_img,TILESIZE,TILESIZE,x,y))
#             x += TILESIZE
#         y+=TILESIZE
#         x = 0



while True:
    #оброби подію «клік за кнопкою "Закрити вікно"
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
                sys.exit()
            if e.key == K_SPACE:
                player.fire()

    if not GG:
        now = time.get_ticks()
        

        walls_collide = sprite.groupcollide( walls,bullets,False, True, sprite.collide_mask)
        bullets_collide = sprite.groupcollide( enemys,bullets,False, True, sprite.collide_mask)
        for enemy in bullets_collide:
            enemy.hp -= 1   
            if enemy.hp <= 0:
                enemy.kill()

  

        collide_list = sprite.spritecollide(player,enemys,False,sprite.collide_mask)

        for enemy in collide_list:
            player.hp -= 1
            hp_label = font1.render(f"HP: {player.hp}",True,(255,255,255)) 
            enemys.remove(enemy)


        sprites.update()
    
        if sprite.spritecollide(player,apples,True):
            player.hp +=2
            hp_label = font1.render(f"HP: {player.hp}",True,(255,255,255))


        if sprite.spritecollide(player,coins,True):
            player.coins += 1
            coins_label = font1.render(f"coins: {player.coins}",True,(255,255,255))

        if player.hp <= 0:
            GG = True
        if sprite.spritecollide(player,enemys,True):
            GG = True
            GG_text = font2.render("Game Over", True,(255,0,0))

        # if sprite.spritecollide(player,treasure,True):
        #     GG = True
        #     GG_won = font2.render("You won", True,(255,0,0))


    window.blit(bg, (0,0))
    sprites.draw(window)
    window.blit(hp_label,(10,10))
    window.blit(coins_label, (150,10))
    if GG:
        window.blit(GG_text,(400,250))
    display.update()
    clock.tick(FPS)


