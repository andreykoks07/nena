#Создай собственный Шутер!
from pygame import *
from random import *
from time import time as timer
mixer.init()
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Galaxy Shooter')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))

win = font1.render('YOU WIN!', True, (0,255,0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0)) 


score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 5 #проиграли, если пропустили столько
goal = 10
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Ast(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

clock = time.Clock()

mixer.music.load('fire.ogg')
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
space = mixer.Sound('space.ogg')
mixer.music.play()

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80 , 50, randint(1 , 4))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 2):
   asteroid = Ast('asteroid.png', randint(80, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)

ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

finish = False
run = True 
rel_time = False

num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
               if num_fire < 5 and rel_time == False:
                num_fire = num_fire +1
                fire_sound.play()
                ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

 
    if not finish:
        window.blit(background,(0,0))
        bullets.update()
        ship.update()
        asteroids.update()
        ship.reset()
        monsters.update()
        monster.reset()
        asteroids.draw(window)
        bullets.draw(window)
        monsters.draw(window)
        text = font2.render('Счёт:' + str(score),1,(255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render('Пропущено:' + str(lost),1,(255,255,255))
        window.blit(text_lose, (10,50))

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1 , (150,0,0))
                window.blit(reload, (260, 460))

            else:
                num_fire = 0
                now_time = timer()

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))



        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        
        display.update()
    clock.tick(60)