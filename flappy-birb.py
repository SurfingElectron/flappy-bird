import pygame, sys, random

# HELPER FUNCTIONS
# Draws 2 floor surfaces and continually move them LEFT 
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

# Checks if any collisions between bird rect and pipes, and if bird rect is out of bounds
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    
    return True

#Initiates pygame, create a display surface, create a clock object so we can limit frame rate
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

# GAME VARIABLES
gravity = 0.25
bird_movement = 0
game_active = True

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

        # Check for user input
        if event.type == pygame.KEYDOWN:
            # Move bird when space bar pressed and game still running
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
        
            # Reset all variables and restart game if space bar pressed and game not running
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0


        # Spawn the pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    
    # Place the background surface, two arguments; the surface and coordinates (0,0 is TOP LEFT corner)
    screen.blit(bg_surface,(0,0))

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)


    # Updates the display, sets the max frame rate
    pygame.display.update()
    clock.tick(120)