import pygame
import os

current_path = os.getcwd()

class Sound:
    def __init__(self, name = None):
        if name is not None:
            self.name = name
            self.file_name = pygame.mixer.Sound(f"resources/assets/sounds/{self.name}.mp3")
        else:
            self.name = None
            self.file_name = None

    def play(self):
        if self.file_name is not None:
            self.file_name.play()
