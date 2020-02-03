import json
import sys

import pygame
from box import Box
from pygame.locals import *
from spritesheet import SpriteSheet, Origin


class PALLET:
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    TRANSWHITE = (255, 255, 255, 20)
    BACKGROUND = (71, 45, 60, 255)
    TRANSPARENT = (0, 0, 0, 0)


def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


def sprite_mapping():
    with open(SPRITE_LEGEND) as json_file:
        data = json.load(json_file)
    return Box(data)


def debug_room(room_width, room_height):
    starting_point = (SCREEN_CENTER[0] - (room_width * sprite_w) / 2, SCREEN_CENTER[1] - (room_height * sprite_h) / 2)
    index = 1
    sprite_index = None
    for y in range(0, room_height):
        for x in range(0, room_width):
            square = (starting_point[0] + (sprite_w * x), starting_point[1] + (sprite_h * y))

            if x == 0 and y > 0:
                sprite_index = sprite_map.dungeon.walls.left
            if x == room_width - 1 and y > 0:
                sprite_index = sprite_map.dungeon.walls.right
            if y == 0 and x > 0:
                sprite_index = sprite_map.dungeon.walls.top
            if y == room_height - 1 and x > 0:
                sprite_index = sprite_map.dungeon.walls.bottom

            if x == 0 and y == 0:
                sprite_index = sprite_map.dungeon.corners.top.left
            if x == room_width - 1 and y == 0:
                sprite_index = sprite_map.dungeon.corners.top.right
            if y == room_height - 1 and x == 0:
                sprite_index = sprite_map.dungeon.corners.bottom.left
            if y == room_height - 1 and x == room_width - 1:
                sprite_index = sprite_map.dungeon.corners.bottom.right

            if sprite_index:
                SPRITES.blit(DS, sprite_index, position=square, origin=Origin.Center)
            index += 1

            sprite_index = None


def draw_grid():
    y_adjustment = (HEIGHT % sprite_h) / 2 if HEIGHT % sprite_h > 0 else 0
    x_adjustment = (WIDTH % sprite_w) / 2 if WIDTH % sprite_w > 0 else 0
    exclude_bottom = 3

    for y in range(0, int(HEIGHT / sprite_h) - exclude_bottom + 1):
        pygame.draw.line(DS, PALLET.TRANSWHITE, (x_adjustment, y_adjustment), (WIDTH - x_adjustment, y_adjustment), 1)
        y_adjustment += sprite_h
    for x in range(0, int(WIDTH / sprite_w) + 1):
        pygame.draw.line(DS, PALLET.TRANSWHITE, (x_adjustment, 0), (x_adjustment, HEIGHT - (sprite_h * exclude_bottom)),
                         1)
        x_adjustment += sprite_w


def draw_ui():
    horizontal_adjustment = (WIDTH % sprite_w) / 2
    starting_point = ((horizontal_adjustment + sprite_w / 2), HEIGHT - (4 * (sprite_h / 2)))

    # HP:
    SPRITES.blit(DS, sprite_map.text.letters.h, position=starting_point, origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.letters.p, position=(starting_point[0] + sprite_w, starting_point[1]),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.characters.colon, position=(starting_point[0] + sprite_w * 2, starting_point[1]),
                 origin=Origin.Center)
    # 000
    SPRITES.blit(DS, sprite_map.text.numbers.six, position=(starting_point[0] + sprite_w * 3, starting_point[1]),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.numbers.six, position=(starting_point[0] + sprite_w * 4, starting_point[1]),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.numbers.six, position=(starting_point[0] + sprite_w * 5, starting_point[1]),
                 origin=Origin.Center)
    # MP:
    SPRITES.blit(DS, sprite_map.text.letters.m, position=(starting_point[0], starting_point[1] + sprite_h),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.letters.p, position=(starting_point[0] + sprite_w, starting_point[1] + sprite_h),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.characters.colon,
                 position=(starting_point[0] + sprite_w * 2, starting_point[1] + sprite_h),
                 origin=Origin.Center)
    # 000
    SPRITES.blit(DS, sprite_map.text.numbers.six,
                 position=(starting_point[0] + sprite_w * 3, starting_point[1] + sprite_h),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.numbers.six,
                 position=(starting_point[0] + sprite_w * 4, starting_point[1] + sprite_h),
                 origin=Origin.Center)
    SPRITES.blit(DS, sprite_map.text.numbers.six,
                 position=(starting_point[0] + sprite_w * 5, starting_point[1] + sprite_h),
                 origin=Origin.Center)


if __name__ == '__main__':
    pygame.init()
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("H E C K")

    FPS = 120
    WIDTH = 800
    HEIGHT = 600
    SCREEN_CENTER = (WIDTH / 2, HEIGHT / 2)
    DS = pygame.display.set_mode((WIDTH, HEIGHT))

    SPRITE_SHEET = "Assets\\Tilesheet\\remap_jd_colored.png"
    SPRITE_LEGEND = "Assets\\forestsprite.json"
    SPRITES = SpriteSheet(SPRITE_SHEET, columns=32, rows=32)
    sprite_h = SPRITES.sprite_height()
    sprite_w = SPRITES.sprite_width()
    sprite_map = sprite_mapping()

    while True:
        events()
        pygame.display.update()
        CLOCK.tick(FPS)
        DS.fill(PALLET.BACKGROUND)

        debug_room(16, 16)
        draw_grid()
        draw_ui()
