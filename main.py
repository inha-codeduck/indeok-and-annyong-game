import sys
import pygame
import time
from pygame.locals import *

# Import modules from the indeok_and_annyong_game package
from indeok_and_annyong_game.game import Game
from indeok_and_annyong_game.board import Board
from indeok_and_annyong_game.character import Indeok, Annyong
from indeok_and_annyong_game.controller import ArrowsController, WASDController, GeneralController
from indeok_and_annyong_game.gates import Gates
from indeok_and_annyong_game.doors import IndeokDoor, AnnyongDoor
from indeok_and_annyong_game.level_select import LevelSelect

def main():
    pygame.init()
    controller = GeneralController()
    game = Game()
    show_intro_screen(game, controller)


def show_intro_screen(game, controller):
    intro_screen = pygame.image.load('resources/screens/intro_screen.png')
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
    win_screen = pygame.image.load('resources/screens/win_screen.png')
    win_screen.set_colorkey((255, 0, 255))
    game.display.blit(win_screen, (0, 0))

    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_death_screen(game, controller, level):
    death_screen = pygame.image.load('resources/screens/death_screen.png')
    death_screen.set_colorkey((255, 0, 255))
    game.display.blit(death_screen, (0, 0))
    while True:
        game.refresh_window()
        events = pygame.event.get()
        if controller.press_key(events, K_RETURN):
            run_game(game, controller, level)
        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

def game_paused(game, elapsed_time):
    pygame.font.init()

    paused_time = elapsed_time

    # Pause 글씨 박스 만들기
    paused_message_object = pygame.image.load('resources/screens/paused.png')
    paused_message_rect = paused_message_object.get_rect()
    paused_message_rect.center = (512, 150)

    # Resume 글씨 박스 만들기(버튼용)
    resume_message_object = pygame.image.load('resources/screens/continue.png')
    resume_message_rect = resume_message_object.get_rect()
    resume_message_rect.center = (512, 300)

    # Restart 글씨 박스 만들기(버튼용)
    restart_message_object = pygame.image.load('resources/screens/restart.png')
    restart_message_rect = restart_message_object.get_rect()
    restart_message_rect.center = (512, 400)

    # Quit 글씨 박스 만들기(버튼용)
    quit_message_object = pygame.image.load('resources/screens/quit.png')
    quit_message_rect = quit_message_object.get_rect()
    quit_message_rect.center = (512, 500)
    
    #반투명 배경 생성
    background_surface = pygame.Surface((1280, 768))
    background_surface.set_alpha(2.5)  # 투명도 설정(set_alpha안에 숫자가 작을수록 투명해짐)
    background_surface.fill((255, 255, 255))

    # 선택된 버튼 초기화
    selected_button = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if resume_message_rect.collidepoint(mouse_pos):  # Resume 박스 클릭 시
                    return paused_time
                elif quit_message_rect.collidepoint(mouse_pos):  # Quit 박스 클릭 시
                    pygame.quit()
                    sys.exit()
                elif restart_message_rect.collidepoint(mouse_pos):
                    main()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:  # ESC 키를 누르면 Resume
                    return paused_time
                elif event.key == pygame.K_DOWN:  # 아래 방향키를 누르면 다음 버튼 선택
                    selected_button = (selected_button + 1) % 3
                elif event.key == pygame.K_UP:  # 위 방향키를 누르면 이전 버튼 선택
                    selected_button = (selected_button - 1) % 3
                elif event.key == pygame.K_RETURN:  # Enter 키 누르면 선택된 버튼 실행
                    if selected_button == 0:
                        return paused_time
                    elif selected_button == 1:
                        main()
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()

        # 스크린에 텍스트 넣은 박스, 투명배경 나타나게 하기
        game.screen.blit(background_surface,(0,0))
        game.screen.blit(paused_message_object, paused_message_rect)
        game.screen.blit(resume_message_object, resume_message_rect)
        game.screen.blit(restart_message_object, restart_message_rect)
        game.screen.blit(quit_message_object, quit_message_rect)

        # 선택된 버튼 표시
        if selected_button == 0:
            pygame.draw.rect(game.screen, (0, 0, 0), resume_message_rect, 4, border_radius = 15)
        elif selected_button == 1:
            pygame.draw.rect(game.screen, (0, 0, 0), restart_message_rect, 4, border_radius = 15)
        elif selected_button == 2:
            pygame.draw.rect(game.screen, (0, 0, 0), quit_message_rect, 4, border_radius = 15)

        pygame.display.update()

def run_game(game, controller, level="level1"):
    # load level data
    if level == "level1":
        start_time = time.time()
        board = Board('resources/level1.txt')
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
        start_time = time.time()
        board = Board('resources/level2.txt')
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
        start_time = time.time()
        board = Board('resources/level3.txt')
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
    font = pygame.font.Font(None, 40)

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
            # show_level_screen(game, controller)
            paused_time = game_paused(game, elapsed_time)
            start_time = time.time() - paused_time

        # close window is player clicks on [x]
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #게임경과시간 나타내기
        elapsed_time = time.time() - start_time

        text = font.render("{:02d}:{:02d}".format(int(elapsed_time//60),int(elapsed_time%60)), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (950,15)
        game.screen.blit(text, text_rect)

        pygame.display.flip()
        
if __name__ == '__main__':
    main()