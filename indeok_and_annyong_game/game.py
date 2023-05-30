import sys
import pygame
import time
from pygame.locals import *
from indeok_and_annyong_game.sound import Sound

class Game:
    # game meta functions
    def __init__(self):
        self.initialize_window()

    def initialize_window(self):
        WINDOW_SIZE = (1024, 768)
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)
        pygame.display.set_caption("Indeok and Annyong")

        CHUNK_SIZE = 32
        DISPLAY_SIZE = (32 * CHUNK_SIZE, 24 * CHUNK_SIZE)
        self.display = pygame.Surface(DISPLAY_SIZE)

    def draw_level_screen(self, level_select):
        # display main level selectio screen background
        self.display.blit(level_select.screen, (0, 0))

        # display the 3 level titles
        for level in range(3):
            # get image from level_select titles dictionary
            image = level_select.titles[level + 1]
            # center title in x direction
            title_x = (self.display.get_width() - image.get_width()) / 2
            # move titles down so that they don't overlap
            title_y = 130 * level + 200
            self.display.blit(image, (title_x, title_y))

        # display the characters on the left and right of level titles
        left_cords = (50, 150)
        right_cords = (430, 150)
        # self.display.blit(level_select.left_player, left_cords)
        # self.display.blit(level_select.right_player, right_cords)

    def user_select_level(self, level_select, controller):
        # create current level selected index
        level_index = 0
        # create dictionary to map index to level name
        level_dict = {
            0: "level1",
            1: "level2",
            2: "level3",
        }
        while True:
            # draw the level selection screen
            self.draw_level_screen(level_select)
            # get all pygame inputs
            events = pygame.event.get()
            # if player presses <down>
            if controller.press_key(events, K_DOWN):
                # move index down one
                level_index += 1
                # wrap around if goes past end
                if level_index == 3:
                    level_index = 0
            # if player presses <up>
            if controller.press_key(events, K_UP):
                # move index up one
                level_index -= 1
                # wrap around if goes past end
                if level_index == -1:
                    level_index = 2
            # draw indicator around the currently selected level
            self.draw_level_select_indicator(level_select, level_index)

            # if user clicks enter
            if controller.press_key(events, K_RETURN):
                # return the name of the level using dict
                return level_dict[level_index]
            

    def draw_level_select_indicator(self, level_select, level_index):
        indicator = level_select.indicator_image
        # center indicator at the center of screen
        location_x = (self.display.get_width() - indicator.get_width()) / 2
        # move indicator down depending on level index
        location_y = level_index * 130 + 200
        # create tuple of cordinates
        indicator_location = (location_x, location_y)
        # draw indicator
        self.display.blit(level_select.indicator_image, indicator_location)
        self.refresh_window()

    def refresh_window(self):
        new_window_size, center_cords = self.adjust_scale()
        # scale internal display to match window)
        new_display = pygame.transform.smoothscale(self.display, new_window_size)
        self.screen.blit(new_display, center_cords)
        pygame.display.update()

    def adjust_scale(self):
        window_size = self.screen.get_size()

        # if window is longer than aspect ratio
        if window_size[0] / window_size[1] >= 1.5:
            display_size = (int(1.5 * window_size[1]), window_size[1])
        # if window is taller than aspect ratio
        else:
            display_size = (window_size[0], int(.75 * window_size[0]))
        # find cords so that display is centered
        cords = ((window_size[0] - display_size[0]) / 2,
                 (window_size[1] - display_size[1]) / 2)

        return display_size, cords

    # game mechanics

    def draw_level_background(self, board):
        self.display.blit(board.get_background(), (0, 0))

    def draw_board(self, board):
        CHUNK_SIZE = 32
        # draw the full background
        board_textures = board.get_board_textures()
        # draw the solid blocks and liquids
        for y, row in enumerate(board.get_game_map()):
            for x, tile in enumerate(row):
                if tile != "0":
                    self.display.blit(
                        board_textures[f"{tile}"], (x * CHUNK_SIZE, y * CHUNK_SIZE)
                    )

    def draw_gates(self, gates):
        for gate in gates:
            # dispaly gate
            self.display.blit(gate.gate_image, gate.gate_location)

            for location in gate.plate_locations:
                # display plate location
                self.display.blit(gate.plate_image, location)

    def draw_doors(self, doors):
        for door in doors:
            # draw door background
            self.display.blit(door.door_background, door.background_location)
            # draw door
            self.display.blit(door.door_image, door.door_location)
            # draw door frame
            self.display.blit(door.frame_image, door.frame_location)

    def draw_player(self, players):
        for player in players:
            if player.moving_right:
                player_image = player.side_image
            elif player.moving_left:
                player_image = pygame.transform.flip(
                    player.side_image, True, False)
            else:
                player_image = player.image
            player_image.set_colorkey((255, 0, 255))
            self.display.blit(player_image, (player.rect.x, player.rect.y))

    def move_player(self, board, gates, players):
        for player in players:
            # For each frame, calculate what it's motion is
            player.calc_movement()
            movement = player.get_movement()

            # create a list of solid blocks
            collide_blocks = board.get_solid_blocks()
            # add solid blocks from each gates
            for gate in gates:
                collide_blocks += gate.get_solid_blocks()

            # create dictionary for which side the player is coliding on
            collision_types = {
                'top': False,
                'bottom': False,
                'right': False,
                'left': False}

            # try movng the player laterally
            player.rect.x += movement[0]
            # get a list of all blocks that the player is colliding with.
            hit_list = self.collision_test(player.rect, collide_blocks)
            for tile in hit_list:
                # if player is moving right
                if movement[0] > 0:
                    # set right side of player to be left side of tile
                    player.rect.right = tile.left
                    collision_types['right'] = True
                # if player is moving left
                elif movement[0] < 0:
                    # set left side of plyaer to be right side of tile
                    player.rect.left = tile.right
                    collision_types['left'] = True

            # try moving the player vertically
            player.rect.y += movement[1]
            # get a list of all blocks that the player is colliding with.
            hit_list = self.collision_test(player.rect, collide_blocks)
            for tile in hit_list:
                # if player is moving down
                if movement[1] > 0:
                    # set bottom of player to top of tile
                    player.rect.bottom = tile.top
                    collision_types['bottom'] = True
                # if player is moving up
                elif movement[1] < 0:
                    # set top of player to bottom of tile
                    player.rect.top = tile.bottom
                    collision_types['top'] = True

            # if player hits ground, lose all y_velocity
            # if player hits ground, reset air_timer
            if collision_types['bottom']:
                player.y_velocity = 0
                player.air_timer = 0
            else:
                player.air_timer += 1

            # if player hit head, lose all y_velocity
            if collision_types['top']:
                player.y_velocity = 0

    def check_for_death(self, board, players):
        for player in players:
            # if the player is annyong
            if player.get_type() == "annyong":
                # see if she collides with annyong
                is_killed = self.collision_test(
                    player.rect, board.get_lava_pools())
            # if the player is indeok
            if player.get_type() == "indeok":
                # see if he collides wit indeok
                is_killed = self.collision_test(
                    player.rect, board.get_water_pools())
            # see if either collide with goo
            is_killed += self.collision_test(player.rect, board.get_goo_pools())

            # if the is_killed list is longer than 0, kill player
            if is_killed:
                dead_sound = Sound(name = "dead")
                dead_sound.play()
                time.sleep(0.01)
                player.kill_player()

    def check_for_gate_press(self, gates, players):
        for gate in gates:
            plate_collisions = []
            for player in players:
                # is player is colliding with plate, add to list
                plates = gate.get_plates()
                plate_collisions += self.collision_test(player.rect, plates)
            # if the collide list is longer than zero, set plate to pressed
            if plate_collisions:
                gate.plate_is_pressed = True
            # otherwise, set plate to not being pressed
            else:
                gate.plate_is_pressed = False
            # attempt to raise the gate. If plate is pressed, gate will raise,
            # otherwise, the gate will close
            gate.try_open_gate()

    def check_for_door_open(self, door, player):
        # check to see if the player is at the door
        door_collision = self.collision_test(player.rect, [door.get_door()])
        # if the collision list is greater than zero, player is at door
        if door_collision:
            door.player_at_door = True
        # otherwise, player is not at door
        else:
            door.player_at_door = False
        # attempt to raise door. If nobody is at door, try to close the door
        door.try_raise_door()

    @staticmethod
    def level_is_done(doors):
        # by default set win to true
        is_win = True
        for door in doors:
            # if either door are not open, set win to False
            if not door.is_door_open():
                is_win = False
        return is_win

    @staticmethod
    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
