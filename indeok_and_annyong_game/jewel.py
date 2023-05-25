import pygame
import os

class Jewel(pygame.sprite.Sprite):
    def __init__(self, x = None, y = None, color = None):
        if x is not None and y is not None and color is not None:
            super().__init__()
            current_path = os.getcwd()
            jewel_image_orig = pygame.image.load(f"{current_path}/assets/images/jewel_{color}.png").convert_alpha()
            jewel_image = pygame.transform.smoothscale(jewel_image_orig, (40, int(jewel_image_orig.get_height() / jewel_image_orig.get_width() * 40)))
            self.image = jewel_image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.color = color
        else:
            self.image = None
            self.rect = None
            self.rect.x = None
            self.rect.y = None
            self.color = None