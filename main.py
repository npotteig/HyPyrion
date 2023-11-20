import pygame
import numpy as np
from sys import exit

import hyper.render_utils as render_utils
from hyper.render_utils import SCALE
import hyper.hyper_utils as hyper_utils
from hyper.transforms import PolarTransform, LatticeTransform
from hyper.system import LatticeSystem
from hyper.lattice import *

# pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('HyPyrion')


# Initialize the mixer
# pygame.mixer.init()

# Load the music file
bg_music = pygame.mixer.Sound('music/hr-domina-hunting.ogg')
bg_music.set_volume(0.2)

bg_music.play(loops=-1)

l_system = LatticeSystem()
start_transform = LatticeTransform(PolarTransform(0, 0, 0), LatticeCoord([]), l_system)

font = pygame.font.Font(None, 36)  # You can choose a font and size

speed = 0.04

music_played = False

while True:
    l_system.update()
    
    # Play the music in an infinite loop
    # bg_music.play(loops=-1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # if not music_played:
    #     music_played = True
    #     print('here')
    #     bg_music.play(loops = -1)
    
    screen.fill('black')
    pygame.draw.circle(screen, (34, 139, 34), pygame.Vector2(SCALE, SCALE), SCALE)
    pygame.draw.circle(screen, 'red', pygame.Vector2(SCALE, SCALE), SCALE, 4)

    l_system.set_view_origin_lattrans(start_transform)
    start_transform.shift_to_nearer_basepoint()
    # render_utils.draw_order5_tiling(screen, start_transform.rel_transform)
    
    
    # Input and Update Tessallation Transform
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        # Translate Up (down b/c inverse A)
        start_transform.rel_transform.preapply_translation_z(speed) 
    elif keys[pygame.K_DOWN]:
        # Translate Down
        start_transform.rel_transform.preapply_translation_z(-speed)
    elif keys[pygame.K_RIGHT]:
        # Rotate Clockwise
        start_transform.rel_transform.preapply_rotation(-speed) 
    elif keys[pygame.K_LEFT]:
        # Rotate counterclockwise
        start_transform.rel_transform.preapply_rotation(speed) 
        
    # print(len(l_system.lattice_walkers))
    for lat_walker in l_system.lattice_walkers:
        # if len(lat_walker.base_point.coords.coord) == 1:
        #     print(lat_walker.render_position.get_matrix())
        #     time.sleep(1)
        # print(lat_walker.base_point.coords.coord)
        lat_walker.base_point.render_point(lat_walker.render_position, screen, font)
    # afdssaf
        
        
        
    pygame.display.update()