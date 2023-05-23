from board import Board
from gates import Gates
from character import Annyong
import pytest

# import pygame and orther needed libraries
import sys
import pygame
from pygame.locals import *

# import classes
from game import Game
from doors import IndeokDoor, AnnyongDoor
from controller import ArrowsController, WASDController, GeneralController
from level_select import LevelSelect

"""
Collision unit tests
"""

# characters at start
indeok = pygame.Rect(16, 350, 16, 32)
annyong = pygame.Rect(16, 350, 16, 32)
# characters in goo
indeok_goo = pygame.Rect(272, 80, 16, 32)
annyong_goo = pygame.Rect(272, 80, 16, 32)
# characters in lava
indeok_lava = pygame.Rect(19 * 16, 23 * 16, 16, 32)
annyong_lava = pygame.Rect(19 * 16, 23 * 16, 16, 32)
# characters in water
indeok_water = pygame.Rect(11 * 16, 23 * 16, 16, 32)
annyong_water = pygame.Rect(11 * 16, 23 * 16, 16, 32)
# characters at gates
indeok_gates = pygame.Rect(285, 128, 16, 32)
annyong_gates = pygame.Rect(285, 128, 16, 32)
# characters at fire door
indeok_fired = pygame.Rect(64, 48, 16, 32)
annyong_fired = pygame.Rect(64, 48, 16, 32)
# characters at water door
indeok_waterd = pygame.Rect(128, 48, 16, 32)
annyong_waterd = pygame.Rect(128, 48, 16, 32)


collision_cases = [
    # Check that if there is nothing, there is no collisions
    (indeok, [], []),
    (annyong, [], []),
    # Check for player collisions on floor
    (indeok, [pygame.Rect(16, 350, 16, 16)], [pygame.Rect(16, 350, 16, 16)]),
    (annyong, [pygame.Rect(16, 350, 16, 16)],
     [pygame.Rect(16, 350, 16, 16)]),
    # Check for player collisions on goo
    (indeok_goo, [pygame.Rect(272, 80, 16, 16)],
     [pygame.Rect(272, 80, 16, 16)]),
    (annyong_goo, [pygame.Rect(272, 80, 16, 16)],
     [pygame.Rect(272, 80, 16, 16)]),
    # Check for player collisions on lava
    (indeok_lava, [pygame.Rect(19 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(19 * 16, 23 * 16, 16, 16)]),
    (annyong_lava, [pygame.Rect(19 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(19 * 16, 23 * 16, 16, 16)]),
    # Check for player collisions on water
    (indeok_water, [pygame.Rect(11 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(11 * 16, 23 * 16, 16, 16)]),
    (annyong_water, [pygame.Rect(11 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(11 * 16, 23 * 16, 16, 16)]),
    # Check for player collisions on gates
    (indeok_gates, [pygame.Rect(285, 128, 16, 16)],
     [pygame.Rect(285, 128, 16, 16)]),
    (annyong_gates, [pygame.Rect(285, 128, 16, 16)],
     [pygame.Rect(285, 128, 16, 16)]),
    # Check for player collisions on fire doors
    (indeok_fired, [pygame.Rect(64, 48, 16, 16)],
     [pygame.Rect(64, 48, 16, 16)]),
    (annyong_fired, [pygame.Rect(64, 48, 16, 16)],
     [pygame.Rect(64, 48, 16, 16)]),
    # Check for player collisions on water doors
    (indeok_waterd, [pygame.Rect(128, 48, 16, 16)],
     [pygame.Rect(128, 48, 16, 16)]),
    (annyong_waterd, [pygame.Rect(128, 48, 16, 16)],
     [pygame.Rect(128, 48, 16, 16)]),
]

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.


@pytest.mark.parametrize("player,tile,hit_list", collision_cases)
def test_collision(player, tile, hit_list):
    assert Game.collision_test(player, tile) == hit_list


"""
Win Status unit tests
"""

# both doors closed
indeok_door = IndeokDoor((64, 48))
annyong_door = AnnyongDoor((128, 48))

# both doors open
indeok_door_both = IndeokDoor((16, 350))
indeok_door_both._door_open = True
annyong_door_both = AnnyongDoor((16, 350))
annyong_door_both._door_open = True

# fire door open, water door closed
indeok_door_magma = IndeokDoor((16, 350))
indeok_door_magma._door_open = True
annyong_door_magma = AnnyongDoor((128, 48))

# water door open, fire door closed
indeok_door_hydro = IndeokDoor((64, 48))
annyong_door_hydro = AnnyongDoor((16, 350))
annyong_door_hydro._door_open = True

level_done_cases = [
    # players not in front of door
    ([indeok_door, annyong_door], False),
    # both players in front of door
    ([indeok_door_both, annyong_door_both], True),
    # only indeok in front of door
    # players not in front of door
    ([indeok_door_magma, annyong_door_magma], False),
    # both only annyong in front of door
    ([indeok_door_hydro, annyong_door_hydro], False),
]


@pytest.mark.parametrize("doors, win_status", level_done_cases)
def test_level_is_done(doors, win_status):
    assert Game.level_is_done(doors) == win_status


"""
Motion unit tests
"""

motion_test_cases = [
    # player is moving right, player moved right
    (True, False, False, True, False, False),
    # player is moving left, player moved left
    (False, True, False, False, True, False),
    # player is jumping, player height increased
    (False, False, True, False, False, True),
    # player is moving right and jumping, player moved right and height incrased
    (True, False, True, True, False, True),
    # player is moving left and jumping, player moved left and height incrased
    (False, True, True, False, True, True),
]


@pytest.mark.parametrize("moving_right, moving_left, jumping, \
                         moved_right, moved_left, jumped", motion_test_cases)
def test_movement(moving_right, moving_left, jumping,
                  moved_right, moved_left, jumped):
    # initialize everything
    controller = GeneralController()
    player_cords = (32, 336)
    player = Annyong(player_cords)

    gates = Gates((285, 128), [(190, 168), (390, 168)])
    board = Board('data/level1.txt')

    # inital locaton
    init_x = player.rect.x
    init_y = player.rect.y

    # set player movement
    player.moving_right = moving_right
    player.moving_left = moving_left
    player.jumping = jumping

    Game.move_player(Game(), board, [gates], [player])

    assert (player.rect.x > init_x) == moved_right
    assert (player.rect.x < init_x) == moved_left
    assert (player.rect.y < init_y) == jumped
