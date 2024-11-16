#Создай собственный Шутер!
#амамамамамаммамамамамамамам ура додел этоооо чудо юдо
from pygame import *
from random import randint
import time as t
init()
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, name_image, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(name_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global win_width, win_height
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y<win_height-150:                      
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x<win_width-100:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet(self.rect.centerx, self.rect.y,'bullet.png',  60, 10, 30)
        bullets.add(bullet1)
        global lost_fire, fire
        lost_fire = t.time()
        fire.play()

class Enemy(GameSprite):
    global win_width, win_height
    def update(self):
        self.rect.y += self.speed
        #телепортация обратно на вверх
        if self.rect.y > win_height:
            global lost
            lost += 1
            self.kill()
            monsters.add(Enemy(randint(300,win_width-300), randint(-250,-50), "ufo.png", 5, 150, 100))



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()

        

win = display.set_mode((0, 0), FULLSCREEN)
win_width, win_height = display.get_surface().get_size()
display.set_caption("СКУТЕРхочет эту альтушку.png(>_<)СКИБИДИИИИИИИИИИИИИИ ТОИЛЕЕЕЕЕТТТТТТТТТТ ГИПНО ДЕНССССССССССССССССССССССССС ГИПНО ДЕНСССССССССССССССС")
font1 = font.SysFont("Arial", 30)
font2 = font.SysFont("Arial", 5)
timer = time.Clock()

finish = False
game = True
FPS = 60
score = 0
lost = 0

bullets = sprite.Group()
monsters=sprite.Group()
lost_fire = 0
for i in range(5):
    monsters.add(Enemy(randint(300,win_width-300), randint(-250,-50), "ufo.png", 5, 150, 100))

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
image_win = font1.render('YOU WIN!', True, (255,255,255))
image_lose = font1.render('YOU LOSE!', True, (255,255,255))

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

#тупые объекты
player = Player(150, 150, "rocket.png", 10, 100, 150)




while game:
    #обновление экрана
    display.update()
    #задержка
    timer.tick(FPS)
    #обработка событий
    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN  and e.key == K_ESCAPE ):
            game = False
        elif (e.type == KEYDOWN and e.key == K_r):
            player = Player(150, 150, "rocket.png", 10, 100, 150)
            monsters=sprite.Group()
            for i in range(5):
                monsters.add(Enemy(randint(300,win_width-300), randint(-250,-50), "ufo.png", 5, 150, 100))

            finish = False
        elif (e.type == KEYDOWN and e.key == K_SPACE ):
            if t.time() - lost_fire > 1 and not(finish):
                player.fire()
    
    if not(finish):
        #игровая логика
        player.update()
        monsters.update()
        bullets.update()

        monsters_list = sprite.groupcollide(monsters, bullets, True, True)
        for monst in monsters_list:
            score += 1
            monsters.add(Enemy(randint(300,win_width-300), randint(-250,-50), "ufo.png", 5, 150, 100))


        image_score = font1.render('Счёт: '+str(score), True, (255 ,255, 255))
        image_lose = font1.render('Попущено: '+str(lost), True, (255 ,255, 255))
        #зачистка экрана
        win.blit(background, (0, 0))
        win.blit(image_score,(550, 150))
        win.blit(image_lose,(550, 200))

        #отрисовка
        player.reset()

        monsters.draw(win)
        bullets.draw(win)

        
        #победа
        if score >= 50:
            win.blit(image_win, (win_width//2-300,win_height//2-150))
            finish = True
        #поражение
        monsters_list = sprite.spritecollide(player, monsters, True)
        if len(monsters_list) > 0 or lost >= 5:
            win.blit(image_lose, (win_width//2-300, win_height//2-150))
            finish = True



