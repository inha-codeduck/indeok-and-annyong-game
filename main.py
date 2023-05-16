import pygame
import sys
from sound.mp3 import Sound
import time

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
jump_sound = Sound(name="jump")

VELOCITY = 7
MASS = 2
paused_time = 0 #일시정지 시 현재 경과시간 받아오는 변수
paused = 0 #일시정지 여부


# Making Paused
def game_paused(time_elapsed):
    paused_screen = pygame.display.set_mode((1200,800))

    pygame.font.init()

    #Pause 글씨 박스 만들기
    paused_font = pygame.font.SysFont('Arial', 40, True, True)
    paused_message = 'Paused'
    paused_message_object = paused_font.render(paused_message, True, (0,0,0))
    paused_message_rect = paused_message_object.get_rect()
    paused_message_rect.center = (600,200)

    #Resume 글씨 박스 만들기(버튼용)
    resume_font = pygame.font.SysFont('Arial', 20, True, True)
    resume_message = 'Resume'
    resume_message_object = resume_font.render(resume_message, True, (0,0,0))
    resume_message_rect = resume_message_object.get_rect()
    resume_message_rect.center = (600,300)

    #Quit 글씨 박스 만들기(버튼용)
    quit_font = pygame.font.SysFont('Arial', 20, True, True)
    quit_message = 'Quit'
    quit_message_object = quit_font.render(quit_message, True, (0,0,0))
    quit_message_rect = quit_message_object.get_rect()
    quit_message_rect.center = (600,350)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_message_rect.collidepoint(mouse_pos): #Resume 박스 클릭 시
                    paused_time = time_elapsed
                    return paused_time
                elif quit_message_rect.collidepoint(mouse_pos): #Quit 박스 클릭 시
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused_time = time_elapsed
                return paused_time
            
        #스크린에 텍스트 넣은 박스 나타나게 하기
        paused_screen.fill((255,255,255))
        paused_screen.blit(paused_message_object, paused_message_rect)
        paused_screen.blit(resume_message_object, resume_message_rect)
        paused_screen.blit(quit_message_object, quit_message_rect)
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
