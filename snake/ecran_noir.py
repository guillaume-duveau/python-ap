import pygame as pg

COLOR,SCREEN_WIDTH,SCREEN_HEIGHT,CLOCK_FREQUENCY=(0,0,0),400,300,3
pygame.init()

clock=pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
while True:
    clock.tick(CLOCK_FREQUENCY)

    for event in pg.event.get():


    screen.fill(COLOR)
    pg.display.update()
