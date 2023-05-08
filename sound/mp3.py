import pygame
class Sound:
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.file_name = pygame.mixer.Sound(f"./assets/sound/{self.name}.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.file_name)