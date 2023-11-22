import pygame
from sys import exit
import time
import numpy as np

from hyper.render_utils import SCALE
from hyper.transforms import PolarTransform, LatticeTransform
from hyper.system import LatticeSystem
from hyper.lattice import *

WIDTH, HEIGHT = 800, 800
MIDPOINT = np.array([WIDTH/2, HEIGHT/2])

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HyPyrion')

# Set up the clock
clock = pygame.time.Clock()

# Load the music file
bg_music = pygame.mixer.Sound('music/hr-domina-hunting.ogg')
bg_music.set_volume(0.2)

bg_music.play(loops=-1)

l_system = LatticeSystem()
start_transform = LatticeTransform(PolarTransform(0, 0, 0), LatticeCoord([]), l_system)

font = pygame.font.Font(None, 36)  # You can choose a font and size

speed = 0.04

use_mouse = True
mouse_pressed = False
print_text = False

while True:
    l_system.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    pygame.draw.circle(screen, (34, 139, 34), pygame.Vector2(SCALE, SCALE), SCALE)
    pygame.draw.circle(screen, 'red', pygame.Vector2(SCALE, SCALE), SCALE, 4)

    l_system.set_view_origin_lattrans(start_transform)
    shifted = start_transform.shift_to_nearer_basepoint(use_mouse)
    
    mouse_buttons = pygame.mouse.get_pressed()
    
    
    if use_mouse:
        # Tiling Traversal
        # Click in direction of point to travel to it (Similar to Hyperrogue)
        if mouse_buttons[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pos = np.array([mouse_x, mouse_y])
            p_trans = start_transform.step_in_mouse_direction(mouse_pos, MIDPOINT)
            i = 0
            mouse_pressed = True
            time.sleep(0.2)
        
        if not shifted and mouse_pressed:
            start_transform.rel_transform.preapply_polar_transform(p_trans)
            # i += 1
        else:
            mouse_pressed = False
        
    else:
        # Input and Update Tessallation Transform for Continuous Action Traversal
        keys = pygame.key.get_pressed()
        # print(start_transform.rel_transform.to_string())
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
    
        
    for lat_walker in l_system.lattice_walkers:
        lat_walker.base_point.render_point(lat_walker.render_position, screen, font, print_text)
        
        
        
    pygame.display.update()
    # time.sleep(1)
    
    clock.tick(60)