import pygame,sys,random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,632))
    screen.blit(floor_surface,(floor_x_pos + 432 ,632))

def create_pipe():
    random_pipe_pos= random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(600,random_pipe_pos))
    top_pipe= pipe_surface.get_rect(midbottom =(600,random_pipe_pos-200))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720:   
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if char_rect.colliderect(pipe):
            death_sound.play()
            return False
    
    if char_rect.top <= -100 or char_rect.bottom >= 632:
        death_sound.play()
        return False

    return True

def rotate_char(char):
    new_char = pygame.transform.rotozoom(char,-char_movement*3,1)
    return  new_char 

def char_animation():
    new_char= char_frames[char_index]
    new_char_rect = new_char.get_rect(center=(80,char_rect.centery))
    return new_char,new_char_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center=(216,80))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center=(216,80))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(216,600))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency= 44100,size=16,channels=1,buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.TTF',30)

# Game Variables
gravity =0.15
char_movement = 0
game_active=True
score = 0
high_score= 0



bg_surface = pygame.image.load('assets/sprites/background.png').convert()
bg_surface=pygame.transform.scale(bg_surface,(432,720))

floor_surface= pygame.image.load('assets/sprites/baseee.png').convert()
floor_surface= pygame.transform.scale(floor_surface,(432,144))
floor_x_pos = 0

char_downflap = pygame.transform.scale(pygame.image.load('assets/sprites/downflip.png').convert_alpha(),(41,44))
char_midflap = pygame.transform.scale(pygame.image.load('assets/sprites/midflip.png').convert_alpha(),(41,44))
char_upflap = pygame.transform.scale(pygame.image.load('assets/sprites/upflip.png').convert_alpha(),(41,44))
char_frames = [char_downflap,char_midflap,char_upflap]
char_index = 0
char_surface = char_frames[char_index]
char_rect = char_surface.get_rect(center=(80,360))

CHARFLAP = pygame.USEREVENT +1
pygame.time.set_timer(CHARFLAP,200)


pipe_surface= pygame.image.load('assets/sprites/black-pipe.png')
pipe_surface= pygame.transform.scale(pipe_surface,(67,441))
pipe_list=[]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1300)
pipe_height=[300,350,400,450,500,550]

game_over_surface = pygame.transform.scale(pygame.image.load('assets/sprites/1message.png').convert_alpha(),(236,343))
game_over_rect = game_over_surface.get_rect(center =(216,360))


flap_sound = pygame.mixer.Sound('assets/sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('assets/sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('assets/sounds/sfx_point.wav')
score_sound_countdown=100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                char_movement = 0
                char_movement -= 5.5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                char_rect.center = (80,360)
                char_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == CHARFLAP:
            if char_index < 2:
                char_index += 1
            else:
                char_index= 0
            char_surface,char_rect= char_animation()
    
    screen.blit(bg_surface,(0,0))

    if game_active:
        # Char
        char_movement += gravity
        rotated_char = rotate_char(char_surface)
        char_rect.centery += char_movement
        screen.blit(rotated_char,char_rect)
        game_active=check_collision(pipe_list)


        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown=100

    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')



    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    
 
    pygame.display.update()
    clock.tick(120)