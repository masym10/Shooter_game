#Створи власний Шутер!
from pygame import *
from random import randint
import time as timer
#main_win
window = display.set_mode((700,500))
display.set_caption("Space_Fight_Alone")
#class game
class Sprite(sprite.Sprite):
    def __init__(self, image_name, x, y, w, h, speed):
        super().__init__()
        self.image = image.load(image_name)
        self.image = transform.scale(self.image, (w, h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

count_fires = 0

class Player(Sprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire(self):
        global count_fires
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top, 15, 20, 3)
        bullets.add(bullet)
        mixer.music.load('fire.ogg')
        mixer.music.play()
        count_fires += 1
        
lost = 0

class Enemy(Sprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y >= 500:
            lost += 1
            self.rect.y = 50
            self.rect.x = randint(50,650)
            self.speed = randint(1,2)
            
score = 0
class Bullet(Sprite):
    def update(self):
        self.rect.y -= self.speed
#Text
font.init()
font = font.SysFont('Arial', 30)
#Game_music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
#Game
fps = 60
time = time.Clock()
background_image = image.load('galaxy.jpg')
background = transform.scale(background_image, (700,500))
game = True
#sprite_group
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
#player
player1 = Player('rocket.png', 350, 400, 50, 50, 10)
#count_enemy
max_m = 4
for i in range(1, max_m):
    monster = Enemy('ufo.png', randint(50,650), 50, 50, 50, randint(1,2))
    monsters.add(monster)

max_a = 2
for i in range(1, max_a):
    asteroid = Enemy("asteroid.png", randint(50, 650), 0, 50, 50, randint(1,5))
    asteroids.add(asteroid)

finish = False
lifes = 3
#While Game
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if count_fires >= 10:
                    timer.sleep(1)
                    count_fires = 0
                else:
                    player1.fire()
                    
    if not finish:

        window.blit(background, (0,0))

        player1.draw()
        player1.move()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
#collide monsters
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(50,650), 0, 50, 50, randint(1,2))
            monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets, True, True)
#collide asteroid
        for c in collides:
            score = score + 1
            asteroid = Enemy("asteroid.png", randint(50, 650), 0, 50, 50, randint(1,5))
            asteroids.add(asteroid)

        lost_txt = font.render(f"Пропущено: {str(lost)}", True, (255,255,255))
        score_txt = font.render(f"Збито: {str(score)}", True, (255,255,255))
        window.blit(lost_txt, (25,55))
        window.blit(score_txt, (25,15))

        if sprite.spritecollide(player1, monsters, False) or sprite.spritecollide(player1, asteroids, False):
            lifes = lifes - 1
            sprite.spritecollide(player1, monsters, True)
            sprite.spritecollide(player1, asteroids, True)            

        if lifes == 3:
            color = (0,255,0)

        elif lifes == 2:
            color = (255,255,0)

        elif lifes == 1:
            color = (255,0,0)

        if lifes == 0:
            finish = True    

        text = font.render(str(lifes), True, color)
        window.blit(text, (650,20))   
#win or defeat
        if score == 10:
            color = (255,255,255)
            text = font.render("You win!!!", True, color)
            window.blit(text, (250,250))   
            timer.sleep(5)
            finish = True
        if lost >= 3:
            text = font.render("You looses!!! pls replay", True, color)
            window.blit(text, (250,250))
            timer.sleep(2)
            game == False
            
    else:
        finish = False
        score = 0
        lost = 0
        lifes = 3
        max_m += 2
        max_a += 1
        
        for b in bullets:
            b.kill()

        for m in monsters:
            m.kill()
        
        for a in asteroids:
            a.kill()

        timer.sleep(3)
        
        for i in range(1, max_m):
            monster = Enemy('ufo.png', randint(50,650), 50, 50, 50, randint(1,2))
            monsters.add(monster)
        
        for i in range(1, max_a):
            asteroid = Enemy("asteroid.png", randint(50, 650), 0, 50, 50, randint(1,5))
            asteroids.add(asteroid)

    time.tick(fps)
    display.update()
    
    
    


