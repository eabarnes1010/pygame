import pygame as pg
import random
import numpy as np

random.seed(4746)
time, TIME_STEP = 0, 300
TILE_SIZE = 40
WINDOW = TILE_SIZE * 30
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)


def get_random_position():
    return [random.randrange(*RANGE), random.randrange(*RANGE)]


def out_of_window(object):
    if object.left < 0:
        return True, "west"
    if object.right > WINDOW:
        return True, "east"
    if object.top < 0:
        return True, "north"
    if object.bottom > WINDOW:
        return True, "south"

    return False, None


def place_object_randomly(object):
    object.center = get_random_position()


def place_dict_object_randomly(d, wall_dict):
    for key in d:
        place_object_randomly(d[key], wall_dict)


def button_clicked(button_dict):
    mouse = pg.mouse.get_pos()
    for key in button_dict:
        if button_dict[key].collidepoint(mouse):
            return True
    return False


# ------------------------------------------
# MAIN GAME CODE

pg.font.init()  # you have to call this at the start,
# if you want to use this module.
my_font = pg.font.SysFont("Arial", 30)

points = 0
pts_text = str(points)
text_surface = my_font.render(pts_text, False, (255, 255, 255))

panda_img = pg.image.load("images/panda.png")
panda = pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])
panda_dir = (0, 0)
place_object_randomly(panda)

food_img = pg.image.load("images/apple.bmp")
food = pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])
place_object_randomly(food)

# make buttons
button_dict = {
    "button_1": pg.rect.Rect([0, 0, TILE_SIZE * 2, TILE_SIZE * 1]),
    "button_2": pg.rect.Rect([0, 0, TILE_SIZE * 2, TILE_SIZE * 1]),
}
for i, key in enumerate(button_dict):
    button_dict[key].center = (WINDOW // 2, WINDOW // 2 + i * TILE_SIZE * 2)

screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()

dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 1}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            if button_clicked(button_dict):
                place_object_randomly(panda)
                place_object_randomly(food)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirs[pg.K_UP]:
                panda_dir = (0, -TILE_SIZE)
            if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                panda_dir = (0, TILE_SIZE)
            if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                panda_dir = (-TILE_SIZE, 0)
            if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                panda_dir = (TILE_SIZE, 0)
    screen.fill("white")

    # check if out of window
    window_escape, _ = out_of_window(panda)

    if window_escape:

        # stop game for 2 seconds
        screen.fill("red")
        end_game_text = "Pac Points = " + str(points)
        text_surface = my_font.render(end_game_text, False, (0, 0, 0))
        screen.blit(text_surface, (0, WINDOW / 2.2))
        pg.display.flip()
        pg.time.delay(2000)

        # start the game again
        screen.fill("white")
        points = 0
        panda_dir = (0, 0)

    # check for food
    if panda.center == food.center:
        points += 1
        place_object_randomly(food)

    pts_text = str(points)
    text_surface = my_font.render(pts_text, False, (255, 255, 255))

    # draw the button
    for key in button_dict:
        pg.draw.rect(screen, (255, 0, 0), button_dict[key])

    # draw the panda
    screen.blit(
        panda_img,
        (
            panda.center[0] - panda_img.get_width() / 2,
            panda.center[1] - panda_img.get_height() / 2,
        ),
    )

    # draw food
    screen.blit(
        food_img,
        (
            food.center[0] - food_img.get_width() / 2,
            food.center[1] - food_img.get_height() / 2,
        ),
    )

    # print points
    screen.blit(text_surface, (0, 0))

    # move the panda
    time_now = pg.time.get_ticks()
    if time_now - time > TIME_STEP:
        time = time_now
        panda.move_ip(panda_dir)

    pg.display.flip()
    clock.tick(60)
