import pygame, sys, random

# HELPER FUNCTIONS
# Draws 2 floor surfaces and continually move them LEFT (hence the minus)
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576,900))

# Creates a new pipe
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

# Moves the pipes left
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Draws the pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


#Initiates pygame
pygame.init()

# Create a display surface, stored in a variable (screen by convention) and passed a tuple with the screen width and height
screen = pygame.display.set_mode((576,1024))
# Create a clock object so we can limit frame rate (defined later in clock.tick)
clock = pygame.time.Clock()

# GAME VARIABLES
gravity = 0.25
bird_movement = 0

#Create surfaces: import image, then scale it by 2
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, 512))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for user input and adjust bird movement if present (have to set movement to 0 first because of incremental movements)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
        
        # Spawn the pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    
    # Place the background surface, two arguments; the surface and coordinates (0,0 is TOP LEFT corner)
    screen.blit(bg_surface,(0,0))

    # Bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    # Pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # Draws the images
    pygame.display.update()
    clock.tick(120)