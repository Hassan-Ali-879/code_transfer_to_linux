import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.acc = vec(0, 0)

    def get_keys(self):
        # controls
        keys = pg.key.get_pressed()
        right = keys[pg.K_RIGHT]
        left = keys[pg.K_LEFT]
        up = keys[pg.K_UP]
        down = keys[pg.K_DOWN]
        right2 = keys[pg.K_d]
        left2 = keys[pg.K_a]
        up2 = keys[pg.K_w]
        down2 = keys[pg.K_s]
        # move left
        if left or left2:
            self.acc.x = -PLAYER_ACC
        if right or right2:
            self.acc.x = PLAYER_ACC
        if up or up2:
            self.acc.y = -PLAYER_ACC
        if down or down2:
            self.acc.y = PLAYER_ACC
        if self.acc.x != 0 and self.acc.y != 0:
            self.acc.x *= 0.7071
            self.acc.y *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.acc.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.acc.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.acc.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        self.get_keys()
        self.collide_with_walls('x')
        self.collide_with_walls('y')

        # if player falling speed is too fast, falling speed is capped
        if self.vel.y >= 13:
            self.vel.y = 13

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
