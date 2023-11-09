import pygame as pg

COLOR,SCREEN_WIDTH,SCREEN_HEIGHT,CLOCK_FREQUENCY=(255,255,255),400,300,3
pg.init()


screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

while True:
    screen.fill(COLOR)
    x=0
    y=0
    pg.Rect(x,y,20,20)          
    pg.display.update()

