import pygame, sys, random

# HELPER FUNCTIONS
# Draw 2 floor surfaces and continually move them LEFT 
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
    # Only copies over pipes still on the screen, ensures pipes_list doesn't get too big if player does well
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

# Draws the pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Rotates the bird surface
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Animates the flapping wings
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

# Checks if any collisions between bird rect and pipes, and if bird rect is out of bounds
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            collision_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        collision_sound.play()
        return False
    
    return True

# Shows the individual game score
def score_display(game_active):
    if game_active:
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

# Checks the score against the high score, updates as appropriate
def update_scores(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Checks if the bird has passed a pipe, updates the score
def score_increment():
    global score, scoring_enabled
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and scoring_enabled:
                score += 1
                score_sound.play()
                scoring_enabled = False
            if pipe.centerx < 0:
                scoring_enabled = True

# LET'S GOOOOOO
# Initiates pygame, create a display surface, create a clock object so we can limit frame rate

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# GAME VARIABLES
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
scoring_enabled = True

# SPRITES
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_pos = 0

pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
pipe_list = []
pipe_height = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512)) 
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

# SOUNDS
flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
collision_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')
score_sound_countdown = 100

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
                flap_sound.play()
        
            # Reset all variables and restart game if space bar pressed and game not running
            if event.key == pygame.K_SPACE and not game_active:
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
                scoring_enabled = True
                game_active = True
                
        # Make the bird flap its wings
        if event.type == BIRDFLAP:
            if bird_index < 2: 
                bird_index += 1 
            else: 
                bird_index = 0
        bird_surface, bird_rect = bird_animation()


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
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score_increment()
        score_display(game_active)

    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_scores(score, high_score)
        score_display(game_active)

    # Updates the display, sets the max frame rate
    pygame.display.update()
    clock.tick(120)