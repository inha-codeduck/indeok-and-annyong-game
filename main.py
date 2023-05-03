import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Annyong and Indeok")

# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image, control_keys):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.control_keys = control_keys

    def move(self, keys):
        if keys[self.control_keys['left']] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[self.control_keys['right']] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += 5
        if keys[self.control_keys['up']] and self.rect.y > 0:
            self.rect.y -= 5
        if keys[self.control_keys['down']] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += 5

# Load and resize image with smoothscale algorithm
annyong_image_orig = pygame.image.load("annyong.png").convert_alpha()
annyong_image = pygame.transform.smoothscale(annyong_image_orig, (80, int(annyong_image_orig.get_height() / annyong_image_orig.get_width() * 80)))

indeok_image_orig = pygame.image.load("indeok.png").convert_alpha()
indeok_image = pygame.transform.smoothscale(indeok_image_orig, (80, int(indeok_image_orig.get_height() / indeok_image_orig.get_width() * 80)))

# Create characters
annyong = Character(100, 100, annyong_image, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
indeok = Character(200, 100, indeok_image, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN})

# Add characters to sprite group
characters = pygame.sprite.Group()
characters.add(annyong, indeok)

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Font for displaying time
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    for character in characters:
        character.move(keys)

    screen.fill(WHITE)
    characters.draw(screen)

    # Display time elapsed
    time_elapsed = pygame.time.get_ticks() - start_time
    time_elapsed_str = f"{time_elapsed // 60000 % 60:02d}:{time_elapsed // 1000 % 60:02d}"
    time_text = font.render(time_elapsed_str, True, (0, 0, 0))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)
