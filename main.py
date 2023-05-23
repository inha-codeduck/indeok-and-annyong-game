import sys
import pygame
from pygame.locals import *

# import classes
from game import Game
from board import Board
from character import Indeok, Annyong
from controller import ArrowsController, WASDController, GeneralController
from gates import Gates
from doors import IndeokDoor, AnnyongDoor
from level_select import LevelSelect


def main():
    pygame.init()
    controller = GeneralController()
    game = Game()
    show_intro_screen(game, controller)


def show_intro_screen(game, controller):
    intro_screen = pygame.image.load('data/screens/intro_screen.png')
    game.display.blit(intro_screen, (0, 0))
    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_level_screen(game, controller):
    level_select = LevelSelect()
    level = game.user_select_level(level_select, controller)
    run_game(game, controller, level)


def show_win_screen(game, controller):
    win_screen = pygame.image.load('data/screens/win_screen.png')
    win_screen.set_colorkey((255, 0, 255))
    game.display.blit(win_screen, (0, 0))

    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_death_screen(game, controller, level):
    death_screen = pygame.image.load('data/screens/death_screen.png')
    death_screen.set_colorkey((255, 0, 255))
    game.display.blit(death_screen, (0, 0))
    while True:
        game.refresh_window()
        events = pygame.event.get()
        if controller.press_key(events, K_RETURN):
            run_game(game, controller, level)
        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)


def run_game(game, controller, level="level1"):
    # load level data
    if level == "level1":
        board = Board('data/level1.txt')
        gate_location = (285, 128)
        plate_locations = [(190, 168), (390, 168)]
        gate = Gates(gate_location, plate_locations)
        gates = [gate]

        indeok_door_location = (64, 48)
        indeok_door = IndeokDoor(indeok_door_location)
        annyong_door_location = (128, 48)
        annyong_door = AnnyongDoor(annyong_door_location)
        doors = [indeok_door, annyong_door]

        indeok_location = (16, 336)
        indeok = Indeok(indeok_location)
        annyong_location = (35, 336)
        annyong = Annyong(annyong_location)

    if level == "level2":
        board = Board('data/level2.txt')
        gates = []

        indeok_door_location = (390, 48)
        indeok_door = IndeokDoor(indeok_door_location)
        annyong_door_location = (330, 48)
        annyong_door = AnnyongDoor(annyong_door_location)
        doors = [indeok_door, annyong_door]

        indeok_location = (16, 336)
        indeok = Indeok(indeok_location)
        annyong_location = (35, 336)
        annyong = Annyong(annyong_location)

    if level == "level3":
        board = Board('data/level3.txt')
        gates = []

        indeok_door_location = (5 * 16, 4 * 16)
        indeok_door = IndeokDoor(indeok_door_location)
        annyong_door_location = (28 * 16, 4 * 16)
        annyong_door = AnnyongDoor(annyong_door_location)
        doors = [indeok_door, annyong_door]

        indeok_location = (28 * 16, 4 * 16)
        indeok = Indeok(indeok_location)
        annyong_location = (5 * 16, 4 * 16)
        annyong = Annyong(annyong_location)

    # initialize needed classes

    arrows_controller = ArrowsController()
    wasd_controller = WASDController()

    clock = pygame.time.Clock()

    # main game loop
    while True:
        # pygame management
        clock.tick(60)
        events = pygame.event.get()

        # draw features of level
        game.draw_level_background(board)
        game.draw_board(board)
        if gates:
            game.draw_gates(gates)
        game.draw_doors(doors)

        # draw player
        game.draw_player([indeok, annyong])

        # move player
        arrows_controller.control_player(events, indeok)
        wasd_controller.control_player(events, annyong)

        game.move_player(board, gates, [indeok, annyong])

        # check for player at special location
        game.check_for_death(board, [indeok, annyong])

        game.check_for_gate_press(gates, [indeok, annyong])

        game.check_for_door_open(indeok_door, indeok)
        game.check_for_door_open(annyong_door, annyong)

        # refresh window
        game.refresh_window()

        # special events
        if annyong.is_dead() or indeok.is_dead():
            show_death_screen(game, controller, level)

        if game.level_is_done(doors):
            show_win_screen(game, controller)

        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

        # close window is player clicks on [x]
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()