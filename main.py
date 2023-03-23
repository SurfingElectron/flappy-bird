import pygame, sys

# Helper function; draws 2 floor surfaces and continually move them LEFT (hence the minus)
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576,900))


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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for user input!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
    
    
    #Place the background surface, two arguments; the surface and coordinates (0,0 is TOP LEFT corner)
    screen.blit(bg_surface,(0,0))

    #Animate the birb
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    #Draws the images
    pygame.display.update()
    clock.tick(120)