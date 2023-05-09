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

# Game sound effect
jump_sound = pygame.mixer.Sound("./assets/sound/jump.mp3")


VELOCITY = 7
MASS = 2

# Making Paused
def game_paused():
    paused_screen = pygame.display.set_mode((1200,800))

    pygame.font.init()
    paused_font = pygame.font.SysFont('Arial', 40, True, True)
    paused_message = 'Paused'
    paused_message_object = paused_font.render(paused_message, True, (0,0,0))
    paused_message_rect = paused_message_object.get_rect()
    paused_message_rect.center = (600,200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        paused_screen.fill((255,255,255))
        paused_screen.blit(paused_message_object, paused_message_rect)
        pygame.display.update()


# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image, control_keys):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.control_keys = control_keys
        self.is_jump = False
        self.v = VELOCITY
        self.m = MASS

    def update(self):
        if self.is_jump:
            pygame.mixer.Sound.play(jump_sound)
            if self.v > 0:
                F = (0.5 * self.m * (self.v * self.v))
            else:
                F = -(0.5 * self.m * (self.v * self.v))
            self.rect.y -= round(F)
            self.v -= 1
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.is_jump = False
                self.v = VELOCITY

    def move(self, keys):
        if keys[self.control_keys['left']] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[self.control_keys['right']] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += 5
        if keys[self.control_keys['up']] and self.rect.y > 0:
            self.is_jump = True


# Load and resize image with smoothscale algorithm
annyong_image_orig = pygame.image.load("./assets/images/annyong.png").convert_alpha()
annyong_image = pygame.transform.smoothscale(annyong_image_orig, (80, int(annyong_image_orig.get_height() / annyong_image_orig.get_width() * 80)))

indeok_image_orig = pygame.image.load("./assets/images/indeok.png").convert_alpha()
indeok_image = pygame.transform.smoothscale(indeok_image_orig, (80, int(indeok_image_orig.get_height() / indeok_image_orig.get_width() * 80)))

# Create characters
annyong = Character(0, 690, annyong_image, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w})
indeok = Character(1000, 660, indeok_image, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP})

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
        #ESC입력 시 paused 화면 구현
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_paused()

    keys = pygame.key.get_pressed()

    for character in characters:
        character.move(keys)

    character.update()

    screen.fill(WHITE)
    characters.draw(screen)

    # Display time elapsed
    time_elapsed = pygame.time.get_ticks() - start_time
    time_elapsed_str = f"{time_elapsed // 60000 % 60:02d}:{time_elapsed // 1000 % 60:02d}"
    time_text = font.render(time_elapsed_str, True, (0, 0, 0))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)
