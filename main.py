import pygame
import render_utils
from render_utils import Scale
import hyper_utils
from transforms import PolarTransform
import numpy as np
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('HyPyrion')

screen_width, screen_height = screen.get_size()
scaled_centerpoint_x = (screen_width // 2) / Scale - 1
scaled_centerpoint_y = (screen_height // 2) / Scale - 1
# cam_transform = hyper_utils.translation_mat_y(scaled_centerpoint_y) @ hyper_utils.translation_mat_z(scaled_centerpoint_y)
cam_transform = PolarTransform(0, 0, 0)
speed = 0.04

# print(screen_width)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    

    # Draw a poincare disc background
    screen.fill('black')
    pygame.draw.circle(screen, 'gray', pygame.Vector2(Scale, Scale), Scale)
    pygame.draw.circle(screen, 'purple', pygame.Vector2(Scale, Scale), Scale, 4)

    # Render Tessalation
    render_utils.draw_order5_tiling(screen, cam_transform.get_matrix())
    
    # Draw mouse position
    pygame.draw.circle(screen, 'red', (mouse_x, mouse_y), 3)
    
    # Input and Update Tessallation Transform
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        # Translate Up (down b/c inverse A)
        cam_transform.preapply_translation_z(speed) 
    elif keys[pygame.K_DOWN]:
        # Translate Down
        cam_transform.preapply_translation_z(-speed)
    elif keys[pygame.K_RIGHT]:
        # Rotate Clockwise
        cam_transform.preapply_rotation(-speed) 
    elif keys[pygame.K_LEFT]:
        # Rotate counterclockwise
        cam_transform.preapply_rotation(speed) 
        
    pygame.display.update()