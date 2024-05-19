import pygame as pg
import random
import numpy as np

random.seed(4746)
time, TIME_STEP = 0, 300
TILE_SIZE = 30
WINDOW = TILE_SIZE * 20
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
NUM_WALLS = 4


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


def place_object_randomly(object, wall_dict):
    object.center = get_random_position()
    while check_in_wall(object, wall_dict):
        object.center = get_random_position()


def place_dict_object_randomly(d, wall_dict):
    for key in d:
        place_object_randomly(d[key], wall_dict)


def check_in_wall(object, wall_dict):
    in_wall = []
    for key in wall_dict:
        in_wall.append(pg.Rect.colliderect(object, wall_dict[key]))
    if any(in_wall):
        return True
    else:
        return False


def build_walls():
    wall_dict = {}
    for n in np.arange(0, NUM_WALLS):
        if n % 2 == 0:
            wall_dict["wall_" + str(n)] = pg.rect.Rect(
                [0, 0, TILE_SIZE * 10, TILE_SIZE]
            )
            wall_dict["wall_" + str(n)].center = get_random_position()
        else:
            wall_dict["wall_" + str(n)] = pg.rect.Rect(
                [0, 0, TILE_SIZE, TILE_SIZE * 10]
            )
            wall_dict["wall_" + str(n)].center = get_random_position()
    return wall_dict


def materialize_ghosts():
    ghost_dict = {}
    for n in np.arange(0, points + 1):
        ghost_dict["ghost_" + str(n)] = pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])
    place_dict_object_randomly(ghost_dict, wall_dict)
    return ghost_dict


def check_if_spooked(object, ghost_dict):
    for key in ghost_dict:
        # if object.center == ghost_dict[key].center:
        if pg.Rect.colliderect(object, ghost_dict[key]):
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

wall_dict = build_walls()

ghost_image = pg.image.load("figures/ghost.bmp")
ghost_dict = materialize_ghosts()

pacman_img = pg.image.load("figures/pacman.bmp")
snake = pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])
snake_dir = (0, 0)
place_object_randomly(snake, wall_dict)

food_img = pg.image.load("figures/apple.bmp")
food = pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])
place_object_randomly(food, wall_dict)

screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()

dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 1}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirs[pg.K_UP]:
                snake_dir = (0, -TILE_SIZE)
                # dirs = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_RIGHT: 1, pg.K_LEFT: 1}
            if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                snake_dir = (0, TILE_SIZE)
                # dirs = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 1}
            if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                snake_dir = (-TILE_SIZE, 0)
                # dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 0, pg.K_LEFT: 1}
            if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                snake_dir = (TILE_SIZE, 0)
                # dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 0}
    screen.fill("black")

    # check borders and wall bashing
    wall_bash = check_in_wall(snake, wall_dict)

    # check if spooked (hit a ghost)
    ghost_bash = check_if_spooked(snake, ghost_dict)

    # check if out of window
    window_escape, _ = out_of_window(snake)

    if window_escape or wall_bash or ghost_bash:

        # stop game for 2 seconds
        screen.fill("red")
        end_game_text = "Pac Points = " + str(points)
        text_surface = my_font.render(end_game_text, False, (0, 0, 0))
        screen.blit(text_surface, (0, WINDOW / 2.2))
        pg.display.flip()
        pg.time.delay(2000)

        # start the game again
        screen.fill("black")
        points = 0
        for key in wall_dict:
            wall_dict[key].center = get_random_position()
        place_object_randomly(snake, wall_dict)
        place_object_randomly(food, wall_dict)
        ghost_dict = materialize_ghosts()
        snake_dir = (0, 0)

    # check for food
    if snake.center == food.center:
        points += 1
        place_object_randomly(food, wall_dict)
        ghost_dict = materialize_ghosts()

    pts_text = str(points)
    text_surface = my_font.render(pts_text, False, (255, 255, 255))

    # draw wall
    for key in wall_dict:
        pg.draw.rect(screen, "darkorchid", wall_dict[key])

    # draw the snake
    screen.blit(
        pacman_img,
        (
            snake.center[0] - pacman_img.get_width() / 2,
            snake.center[1] - pacman_img.get_height() / 2,
        ),
    )

    # draw food
    pg.draw.rect(screen, "aquamarine", food)
    # screen.blit(
    #     food_img,
    #     (
    #         food.center[0] - food_img.get_width() / 2,
    #         food.center[1] - food_img.get_height() / 2,
    #     ),
    # )

    # draw ghosts
    for key in ghost_dict:
        screen.blit(
            ghost_image,
            (
                ghost_dict[key].center[0] - ghost_image.get_width() / 2,
                ghost_dict[key].center[1] - ghost_image.get_height() / 2,
            ),
        )

    # print points
    screen.blit(text_surface, (0, 0))

    # move the snake
    time_now = pg.time.get_ticks()
    if time_now - time > TIME_STEP:
        time = time_now

        for key in ghost_dict:
            r = random.choice([0, 1, 2, 3])
            if r == 0:
                ghost_dir = (0, TILE_SIZE / 2)
            elif r == 1:
                ghost_dir = (0, -TILE_SIZE / 2)
            elif r == 2:
                ghost_dir = (TILE_SIZE / 2, 0)
            else:
                ghost_dir = (-TILE_SIZE / 2, 0)

            ghost_escape, escape_side = out_of_window(ghost_dict[key])
            if ghost_escape:
                if escape_side == "north":
                    ghost_dir = (0, TILE_SIZE / 2)
                elif escape_side == "south":
                    ghost_dir = (0, -TILE_SIZE / 2)
                elif escape_side == "east":
                    ghost_dir = (-TILE_SIZE / 2, 0)
                elif escape_side == "west":
                    ghost_dir = (TILE_SIZE / 2, 0)
                else:
                    raise ValueError
            ghost_dict[key].move_ip(ghost_dir)
        snake.move_ip(snake_dir)

    # check if spooked (hit a ghost)
    # ghost_bash = check_if_spooked(snake, ghost_dict)
    # if ghost_bash:
    #     print("GAME OVER")
    #     pg.time.delay(4000)

    pg.display.flip()
    clock.tick(60)
