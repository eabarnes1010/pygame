import pygame as pg
from random import randrange

WINDOW = 700
TILE_SIZE = 50
RANGE=(TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

pg.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pg.font.SysFont('Arial', 30)

snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0,0)

food = snake.copy()
food.center = get_random_position()

screen = pg.display.set_mode([WINDOW]*2)
clock = pg.time.Clock()
time, time_step = 0, 200

dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 1}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirs[pg.K_UP]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_RIGHT: 1, pg.K_LEFT: 1}
            if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 1}
            if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 0, pg.K_LEFT: 1}
            if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1, pg.K_LEFT: 0}
    screen.fill('gainsboro')

    # check borders and self eating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        
        # stop game for 2 seconds
        screen.fill('red')
        end_game_text = 'Snake Length = ' + str(length)
        text_surface = my_font.render(end_game_text, False, (0, 0, 0))
        screen.blit(text_surface, (0, WINDOW / 2.2))
        pg.display.flip()
        pg.time.delay(4000)

        # start the game again
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0) 
        segments = [snake.copy()]


    # check for food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1

    # draw the snake
    [pg.draw.rect(screen, "black", segment) for segment in segments]

    # draw food
    pg.draw.rect(screen, 'purple', food)

    # move the snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    pg.display.flip()
    clock.tick(60)
