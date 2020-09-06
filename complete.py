import pygame as pg
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1280
HEIGHT = 690
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)
OPPONENT_SPEED = 2.4

# initialize PyGame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PONG!')
clock = pg.time.Clock()

score_counter = 0
font_name = pg.font.match_font('arial')
pong_ball_speedx = [-5, -4.5, -4, -3.5, 3.5, 4, 4.5, 5]
pong_ball_speedy = [-5, -4.5, -4, -3.5, -3, -2.5, -2,
                    2, 2.5, 3, 3.5, 4, 4.5, 5]


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = int(HEIGHT / 2)
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.speedy = 7
        if keys[pg.K_w]:
            self.speedy = -7
        self.rect.y += self.speedy
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0


class Player2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 15
        self.rect.y = int(HEIGHT / 2)
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.speedy = 7
        if keys[pg.K_UP]:
            self.speedy = -7
        self.rect.y += self.speedy
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0


class Opponent(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 10
        self.rect.y = int(HEIGHT / 2)
        self.speedy = 0

    def update(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0

    def opponent_ai(self):
        if self.rect.top < pong_ball.rect.y:
            self.rect.top += OPPONENT_SPEED
        if self.rect.bottom > pong_ball.rect.y:
            self.rect.bottom -= OPPONENT_SPEED


class PongBall(pg.sprite.Sprite):
    def __init__(self, player, player2):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((36, 36))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = int(WIDTH / 2 - 15)
        self.rect.y = int(HEIGHT / 2 - 15)
        self.speedx = random.choice(pong_ball_speedx)
        self.speedy = random.choice(pong_ball_speedy)
        self.player = player
        self.player2 = player2
        self.bool_left = False
        self.bool_right = False
        self.bool_bounce_counter = False
        self.player1_top_collide = 0
        self.player2_top_collide = 0
        self.player1_bottom_collide = 0
        self.player2_bottom_collide = 0
        self.bounce_counter = 0

    def update(self):
        self.player1_top_collide = self.player.rect.top - self.rect.bottom
        self.player2_top_collide = self.player2.rect.top - self.rect.bottom
        self.player1_bottom_collide = self.player.rect.bottom - self.rect.top
        self.player2_bottom_collide = self.player2.rect.bottom - self.rect.top
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top <= 0:
            self.speedy = -self.speedy
        if self.rect.bottom >= HEIGHT:
            self.speedy = -self.speedy
        if self.rect.right <= -18:
            self.rect.x = int(WIDTH / 2 - 15)
            self.rect.y = int(HEIGHT / 2 - 15)
        if self.rect.left >= WIDTH + 18:
            self.rect.x = int(WIDTH / 2 - 15)
            self.rect.y = int(HEIGHT / 2 - 15)

        # this is so that the pong ball does not get stuck in the paddles
        if self.rect.right >= self.player2.rect.left:
            self.bool_right = True
        if self.rect.left <= self.player.rect.right:
            self.bool_left = True
        if self.rect.right <= self.player2.rect.left:
            self.bool_right = False
        if self.rect.left >= self.player.rect.right:
            self.bool_left = False

        if self.bool_left:
            if 0 >= self.player1_top_collide > - 120:
                self.rect.left = self.player.rect.right
                self.bounce()
                self.speedx *= 1.04
                self.speedy *= 1.04
                self.bounce_counter += 1
            if 0 >= self.player1_bottom_collide > + 120:
                self.rect.left = self.player.rect.right
                self.bounce()
                self.speedx *= 1.04
                self.speedy *= 1.04
                self.bounce_counter += 1

        if self.bool_right:
            if 0 >= self.player2_top_collide > - 120:
                self.rect.right = self.player2.rect.left
                self.bounce()
                self.speedx *= 1.04
                self.speedy *= 1.04
                self.bounce_counter += 1
            if 0 >= self.player2_bottom_collide > + 120:
                self.rect.right = self.player2.rect.left
                self.bounce()
                self.speedx *= 1.04
                self.speedy *= 1.04
                self.bounce_counter += 1

    def reset(self):
        self.bounce_counter = 0
        self.rect.x = int(WIDTH / 2 - 15)
        self.rect.y = int(HEIGHT / 2 - 15)
        self.speedx = random.choice(pong_ball_speedx)
        self.speedy = random.choice(pong_ball_speedy)

    def bounce(self):
        self.speedx = -self.speedx

    def bounce2(self):
        self.speedx = -self.speedx
        self.speedy = -self.speedy


def show_start_screen():
    draw_text(screen, "PONG!", 100, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "w and s keys move player 1, (left player)"
                      " and up and down arrow keys move player 2 (right player)", 27, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "First person to get 5 points wins!", 27, WIDTH / 2, HEIGHT / 2 + 50)
    draw_text(screen, "Press any key to begin", 27, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event2 in pg.event.get():
            if event2.type == pg.QUIT:
                pg.quit()
            if event2.type == pg.KEYUP:
                waiting = False


def show_go_screen():
    draw_text(screen, "Player 1 Wins!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press any key to play again", 22, WIDTH / 2, HEIGHT / 2)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event2 in pg.event.get():
            if event2.type == pg.QUIT:
                pg.quit()
            if event2.type == pg.KEYUP:
                waiting = False


def show_go_screen2():
    draw_text(screen, "Player 2 Wins!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press any key to play again", 22, WIDTH / 2, HEIGHT / 2)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event2 in pg.event.get():
            if event2.type == pg.QUIT:
                pg.quit()
            if event2.type == pg.KEYUP:
                waiting = False


# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_start_screen()
        game_over = False
        # load all game graphics
        all_sprites = pg.sprite.Group()
        pong_ball_group = pg.sprite.Group()
        player = Player()
        player2 = Player2()
        opponent = Opponent()
        pong_ball = PongBall(player, player2)
        all_sprites.add(player)
        all_sprites.add(player2)
        pong_ball_group.add(pong_ball)
        score = 0
        score2 = 0
    # process input (events)
    for event in pg.event.get():
        # check for closing windows
        if event.type == pg.QUIT:
            running = False
    if pong_ball.rect.left > WIDTH - 15:
        score = score + 1
        pong_ball.reset()
    if pong_ball.rect.right < 15:
        score2 = score2 + 1
        pong_ball.reset()
    if score == 5:
        score += 1
        game_over = True
        score = 0
        score2 = 0
        pong_ball.kill()
        player.kill()
        player2.kill()
        show_go_screen()
    if score2 == 5:
        score2 += 1
        game_over = True
        score = 0
        score2 = 0
        pong_ball.kill()
        player.kill()
        player2.kill()
        show_go_screen2()

    # updates
    all_sprites.update()
    pong_ball_group.update()

    # check to see if pong ball hit one of the pads
    hits = pg.sprite.spritecollide(pong_ball, all_sprites, False, pg.sprite.collide_circle)

    # draw and render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pong_ball_group.draw(screen)
    draw_text(screen, str(score), 50, WIDTH / 2 - 30, 10)
    draw_text(screen, str(score2), 50, WIDTH / 2 + 30, 10)
    draw_text(screen, "-", 50, WIDTH / 2, 10)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
