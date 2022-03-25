import pygame
from pygame.locals import *
import random

from Button import Button
from tombstone import Tombstone
from witch import Witch

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 870
screen_height = 940

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Witches Flight")

font = pygame.font.SysFont("Chiller", 60)

white = (255, 255, 255)

run = True

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
tomb_frequency = 1500
final_tomb = pygame.time.get_ticks() - tomb_frequency
score = 0
pass_tomb = False
lvl_up = 1
first_lvl = 5

bg = pygame.image.load("images/bg.png")
ground_img = pygame.image.load("images/ground.png")
button_img = pygame.image.load("images/restart.png")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    global score, lvl_up, tomb_frequency
    tomb_group.empty()
    tomb_frequency = 1500
    witch_girl.rect.x = 100
    witch_girl.rect.y = int(screen_height / 2)
    score = 0
    lvl_up = 1


witch_group = pygame.sprite.Group()
tomb_group = pygame.sprite.Group()

witch_girl = Witch(100, int(screen_height / 2))

witch_group.add(witch_girl)

button = Button(screen_width/2 - 95, screen_height/2 - 100, button_img)

while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    witch_group.draw(screen)
    witch_group.update()
    tomb_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, 770))

    draw_text(f"SCORE: {score}", font, white, int(screen_width / 2 - 100), 15)
    draw_text(f"LVL: {lvl_up}", font, white, int(10), 15)

    # check the score
    if len(tomb_group) > 0:
        if witch_group.sprites()[0].rect.left > tomb_group.sprites()[0].rect.left \
                and witch_group.sprites()[0].rect.right < tomb_group.sprites()[0].rect.right and not pass_tomb:
            pass_tomb = True
        if pass_tomb:
            if witch_group.sprites()[0].rect.left > tomb_group.sprites()[0].rect.right:
                score += 1
                pass_tomb = False

    # look for collision
    if pygame.sprite.groupcollide(witch_group, tomb_group, False, False) or witch_girl.rect.top < 0:
        game_over = True
        witch_girl.game_over = game_over

    # check if witch has hit the ground
    if witch_girl.rect.bottom >= 768:
        game_over = True
        witch_girl.game_over = game_over
        flying = False
        witch_girl.flying = flying
    if not game_over:
        #  generate new tombstones
        if flying:
            time_now = pygame.time.get_ticks()
            if time_now - final_tomb > tomb_frequency:
                tomb_length = random.randint(-100, 100)
                btm_tomb = Tombstone(screen_width, int(screen_height / 2) + tomb_length, -1)
                top_tomb = Tombstone(screen_width, int(screen_height / 2) + tomb_length, 1)
                tomb_group.add(btm_tomb)
                tomb_group.add(top_tomb)
                final_tomb = time_now
            if score == first_lvl:
                first_lvl += 5
                lvl_up += 1
                if tomb_frequency >= 200:
                    tomb_frequency -= 400
            for i in range(lvl_up):
                tomb_group.update()

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 30:
            ground_scroll = 0
        tomb_group.update()

    # check for game over and reset
    if game_over:
        screen.blit(button.image, (button.rect.x, button.rect.y))
        if button.collide_check():
            game_over = False
            witch_girl.game_over = game_over
            reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True
            witch_girl.flying = flying

    pygame.display.update()

pygame.quit()
