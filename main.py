from pygame import *
from random import randint
import pickle
import sys

init()
mixer.init()
font.init()

#створи вікно гри
screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
FPS = 60
flags = FULLSCREEN
window = display.set_mode((WIDTH, HEIGHT),flags) #створюємо вікно 
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
bullet_img = image.load('lazer.png')
wall_img = image.load('stone_gray2.png')
exit_img = image.load('dngn_closed_door.png')
coins_img = image.load('coin 2.png')

sprites = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)


class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)
        self.hp = 260
        self.damage = 52
        self.coins = 0
        self.speed = 5

    def update(self):
        global hp_label
        self.old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed() #отримуємо список натиснутих клавіш
        if keys[K_w] and self.rect.y > 0:
            if self.rect.y > 250:
                self.rect.y -= self.speed
            self.bg_speed = 4
        elif keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.bg_speed = 1
        else:
            self.bg_speed = 2
            
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH    :
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        fire_sound.play()

enemys = sprite.Group()

class Enemy(GameSprite):
    def __init__(self):
        rand_x = randint(0,WIDTH-70)
        y = -150    
        super().__init__(enemy_img,100,70,rand_x,y)
        self.speed = 5
        enemys.add(self)

    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > HEIGHT:
            self.kill()

bullets =  sprite.Group()
class Bullet(GameSprite):
    def __init__(self,player_x,player_y):
        super().__init__(bullet_img,20,40,player_x,player_y)
        self.rect.centerx = player_x
        self.rect.bottom = player_y
        self.speed = 5
        bullets.add(self)

    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y < 0 :
            self.kill()




    sprites.draw(window)
    window.blit(hp_label,(10,10))
    if :
        window.blit(Game_over_text,(400,250))
    display.update()
    clock.tick(FPS)



