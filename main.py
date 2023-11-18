import pygame
import hyper.render_utils as render_utils
from hyper.render_utils import SCALE
import hyper.hyper_utils as hyper_utils
from hyper.transforms import PolarTransform, LatticeTransform
from hyper.system import LatticeSystem
from hyper.lattice import *
import numpy as np
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('HyPyrion')

# screen_width, screen_height = screen.get_size()
# scaled_centerpoint_x = (screen_width // 2) / Scale - 1
# scaled_centerpoint_y = (screen_height // 2) / Scale - 1

l_system = LatticeSystem()
start_transform = LatticeTransform(PolarTransform(0, 0, 0), LatticeCoord([]), l_system)

font = pygame.font.Font(None, 36)  # You can choose a font and size

speed = 0.04

# print(screen_width)

while True:
    l_system.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    pygame.draw.circle(screen, 'gray', pygame.Vector2(SCALE, SCALE), SCALE)
    pygame.draw.circle(screen, 'purple', pygame.Vector2(SCALE, SCALE), SCALE, 4)

    l_system.set_view_origin_lattrans(start_transform)
    start_transform.shift_to_nearer_basepoint()
    
    
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
        
    for lat_walker in l_system.lattice_walkers:
        lat_walker.base_point.render_point(lat_walker.render_position, screen, font)
        
        
        
    pygame.display.update()