import pygame
from sys import exit
import time

from hyper.render_utils import SCALE
from hyper.transforms import PolarTransform, LatticeTransform
from hyper.system import LatticeSystem
from hyper.lattice import *

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('HyPyrion')

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
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    pygame.draw.circle(screen, (34, 139, 34), pygame.Vector2(SCALE, SCALE), SCALE)
    pygame.draw.circle(screen, 'red', pygame.Vector2(SCALE, SCALE), SCALE, 4)

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
    # time.sleep(1)