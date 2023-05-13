import pygame
import sys
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from sound.mp3 import Sound
import time

=======
<<<<<<< HEAD
=======
from sound.mp3 import Sound
>>>>>>> 2b3566ab3f7a872571fd95d61a4a583089d5d61f
>>>>>>> c2b311c (Revert "no file error resolved")
=======
from sound.mp3 import Sound
>>>>>>> 4b80dbe (fix: [minseok] revert1)
=======
from sound.mp3 import Sound
>>>>>>> 9dbf528 (develop commit error and revert recent commit )

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
jump_sound = Sound(name="jump")
=======
<<<<<<< HEAD
#jump_sound = pygame.mixer.Sound("./sound/jump.mp3")

=======
jump_sound = Sound(name="jump")
>>>>>>> 2b3566ab3f7a872571fd95d61a4a583089d5d61f
>>>>>>> c2b311c (Revert "no file error resolved")
=======
jump_sound = Sound(name="jump")
>>>>>>> 4b80dbe (fix: [minseok] revert1)
=======
jump_sound = Sound(name="jump")
>>>>>>> 9dbf528 (develop commit error and revert recent commit )

VELOCITY = 7
MASS = 2
paused_time = 0 #일시정지 시 현재 경과시간 받아오는 변수
paused = 0 #일시정지 여부


# Making Paused
def game_paused(time_elapsed):
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
                paused_time = time_elapsed
                return paused_time
            
        paused_screen.fill((255,255,255))
        paused_screen.blit(paused_message_object, paused_message_rect)
        pygame.display.update()

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD

=======
>>>>>>> 2b3566ab3f7a872571fd95d61a4a583089d5d61f
>>>>>>> c2b311c (Revert "no file error resolved")
=======
>>>>>>> 4b80dbe (fix: [minseok] revert1)
=======
>>>>>>> 9dbf528 (develop commit error and revert recent commit )
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
            #pygame.mixer.Sound.play(jump_sound)
=======
>>>>>>> 2b3566ab3f7a872571fd95d61a4a583089d5d61f
>>>>>>> c2b311c (Revert "no file error resolved")
=======
>>>>>>> 4b80dbe (fix: [minseok] revert1)
=======
>>>>>>> 9dbf528 (develop commit error and revert recent commit )
            if self.v > 0:
                F = (0.5 * self.m * (self.v * self.v))
            else:
                F = -(0.5 * self.m * (self.v * self.v))
            self.rect.y -= round(F)
            self.v -= 1
            if self.rect.bottom > HEIGHT:
                jump_sound.play()
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
        #initializing paused screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused_time = game_paused(time_elapsed)
            paused = 1

    keys = pygame.key.get_pressed()

    for character in characters:
        character.move(keys)
        character.update()

    screen.fill(WHITE)
    characters.draw(screen)

    # Display time elapsed
    if paused == 0:
        time_elapsed = pygame.time.get_ticks() - start_time
        
    else:
        time_elapsed = pygame.time.get_ticks() - (start_time + paused_time)
    time_elapsed_str = f"{time_elapsed // 60000 % 60:02d}:{time_elapsed // 1000 % 60:02d}"
    time_text = font.render(time_elapsed_str, True, (0, 0, 0))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)
