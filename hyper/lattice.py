import pygame
from enum import Enum
import numpy as np
import copy
from typing import ForwardRef


from hyper.render_utils import SCALE, BRANCH_LENGTH, draw_line
from hyper.transforms import PolarTransform

class LatticeType(Enum):
    ORIGIN = 0
    BRANCH2 = 1
    BRANCH3 = 2
    INVALID = 4
    
class LatticeCoord(object):
    
    def __init__(self, d_coord: list) -> None:
        self.coord = d_coord
        self.type = self.find_type()
    
    def find_type(self) -> LatticeType:
        coord_len = len(self.coord)
        
        # If the list is empty, it is ORIGIN
        if coord_len == 0:
            return LatticeType.ORIGIN
        
        # Checking for validity
        if self.coord[0] > 4:
            return LatticeType.INVALID
        prev = 1
        for i in range(1, coord_len):
            if prev == 0 and self.coord[i] > 1:
                return LatticeType.INVALID
            if prev > 0 and self.coord[i] > 2:
                return LatticeType.INVALID
            prev=self.coord[i]
        
        # Checking whether BRANCH2 or BRANCH3
        if coord_len == 1:
            return LatticeType.BRANCH3
        if self.coord[-1] == 0:
            return LatticeType.BRANCH2
        return LatticeType.BRANCH3
    
    def coord_in_direction(self, direction: int) -> "LatticeCoord":
        direction %= 5
        if self.type == LatticeType.INVALID:
            return
        if self.type == LatticeType.ORIGIN:
            return LatticeCoord([direction])
        
        coord_copy = copy.deepcopy(self.coord)
        if direction == 0:
            coord_copy.pop()
            return LatticeCoord(coord_copy)
        if self.type == LatticeType.BRANCH2:
            if direction == 1:
                coord_copy.pop()
                coord_copy_len = len(coord_copy)
                index = coord_copy_len - 1
                while (coord_copy[index] == 0 and index > 0):
                    index -= 1
                branch2_rooted = False
                if (index >= 1 and coord_copy[index] > 1) or index == 0:
                    branch2_rooted = True
                coord_copy[index] = (coord_copy[index]-1+5) % 5
                index += 1
                if index < coord_copy_len:
                    if branch2_rooted:
                        coord_copy[index] = 2
                    else:
                        coord_copy[index] = 1
                    
                    index += 1
                    while index < coord_copy_len:
                        coord_copy[index] = 2
                        index += 1
                return LatticeCoord(coord_copy)
                    
            elif direction == 2:
                coord_copy.append(0)
                return LatticeCoord(coord_copy)
            elif direction == 3:
                coord_copy.append(1)
                return LatticeCoord(coord_copy)
            elif direction == 4:
                coord_copy.append(0)
                coord_copy[-2] = 1
                return LatticeCoord(coord_copy)
        if self.type == LatticeType.BRANCH3:
            if direction == 1:
                coord_copy.append(0)
                return LatticeCoord(coord_copy)
            elif direction == 2:
                coord_copy.append(1)
                return LatticeCoord(coord_copy)
            elif direction == 3:
                coord_copy.append(2)
                return LatticeCoord(coord_copy)
            elif direction == 4:
                if len(self.coord) == 1:
                    return LatticeCoord([(coord_copy[0]+1)%5, 0])
                coord_copy.append(2)
                index = len(coord_copy) - 1
                while coord_copy[index] == 2 and index > 1:
                    coord_copy[index] = 0
                    index -= 1
                if index == 0 or coord_copy[index - 1] != 0:
                    coord_copy[index] = (coord_copy[index]+1)%5
                    return LatticeCoord(coord_copy)
                coord_copy[index - 1] = 1
                coord_copy[index] = 0
                return LatticeCoord(coord_copy)
                
        return
        
    def direction_of_leaf(self) -> int:
        coord_len = len(self.coord)
        if coord_len == 0:
            return 0
        if coord_len == 1:
            return self.coord[0]
        branch3 = False
        if coord_len == 2 or self.coord[-2] != 0:
            branch3 = True
        if branch3:
            return self.coord[-1] + 1
        else:
            return self.coord[-1] + 2 
        
    def direction_after_travel(self, direction: int) -> int:
        direction %= 5
        if self.type == LatticeType.INVALID:
            return -1
        if self.type == LatticeType.ORIGIN:
            return 0
        if direction == 0:
            return self.direction_of_leaf()
        if self.type == LatticeType.BRANCH2:
            if direction == 1:
                return 4
            elif direction == 4:
                return 1
            else:
                return 0
        if self.type == LatticeType.BRANCH3:
            if direction == 4:
                return 1
            else:
                return 0 
        return -1 
    
    def angle_of_leaf(self) -> float:
        return self.direction_of_leaf() * 2*np.pi / 5
    
    def compare_to(self, obj: object) -> int:
        if isinstance(obj, LatticeCoord):
            C = obj
        elif isinstance(obj, LatticePoint):
            C = obj.coords
        else:
            return 2
        
        coord_len = len(self.coord)
        c_len = len(C.coord)
        
        if coord_len > c_len:
            return 1
        if coord_len < c_len:
            return -1
        for i in range(coord_len):
            if self.coord[i] < C.coord[i]:
                return -1
            elif self.coord[i] > C.coord[i]:
                return 1
        return 0
    
    def to_string(self) -> str:
        s = '<'
        for i in range(len(self.coord)):
            s += str(int(self.coord[i]))
            if i != len(self.coord) - 1:
                s += ','
        s += '>'
        return s
class LatticePoint(object):

    def __init__(self, d_coord: LatticeCoord, d_system: "LatticeSystem") -> None:
        self.coords = d_coord
        self.system = d_system
        self.attached_walker = None
    
    def compare_to(self, obj: object):
        return self.coords.compare_to(obj)
    
    def to_string(self) -> str:
        return self.coords.to_string()
    
    def render_point(self, p_transform: PolarTransform, graphic: pygame.Surface, font) -> None:
        transform = p_transform.get_matrix()
        if self.coords.type != LatticeType.ORIGIN:
            draw_line(graphic, transform, line_length=BRANCH_LENGTH)
            if self.coords.type == LatticeType.BRANCH2:
                draw_line(graphic, transform, angle=2*np.pi/5, line_length=BRANCH_LENGTH)

            screen_pos = p_transform.pos_on_screen()
            screen_pos_length = np.linalg.norm(np.array([(screen_pos[0]/SCALE)-1, (screen_pos[1]/SCALE)-1]))
            
            pygame.draw.circle(graphic, 'red', pygame.Vector2(screen_pos[0], screen_pos[1]), 20*(1.5 - screen_pos_length))
            
            text_render = font.render(self.to_string(), True, (255, 255, 255))
            graphic.blit(text_render, (screen_pos[0], screen_pos[1]))
    
    def update(self) -> None:
        pass
    
class LatticeCircularIterator(object):
    
    def __init__(self, d_radius: int) -> None:
        self.radius = d_radius
        self.this_coord = self.first_coord()
        self.first = True
        
    def first_coord(self) -> LatticeCoord:
        coord = np.zeros(self.radius, dtype=int).tolist()
        return LatticeCoord(coord)
    
    def has_next(self) -> bool:
        if self.first:
            return True
        
        for i in range(len(self.this_coord.coord)):
            if self.this_coord.coord[i] != 0:
                return True
        return False
    
    def next_coord(self) -> LatticeCoord:
        copy_coord = copy.deepcopy(self.this_coord.coord)
        i = len(copy_coord) - 1
        while i > 1:
            if copy_coord[i - 1] == 0:
                # BRANCH 2
                if copy_coord[i] < 1:
                    copy_coord[i] += 1
                    return LatticeCoord(copy_coord)
                copy_coord[i] = 0
            else:
                # BRANCH 3
                if copy_coord[i] < 2:
                    copy_coord[i] += 1
                    return LatticeCoord(copy_coord)
                copy_coord[i] = 0
            i -= 1
        
        # BRANCH 3
        i = 1
        if copy_coord[i] < 2:
            copy_coord[i] += 1
            return LatticeCoord(copy_coord)
        
        # ORIGIN
        copy_coord[i] = 0
        copy_coord[0] = (copy_coord[0]+1+5)%5
        return LatticeCoord(copy_coord)
    
    def next(self) -> LatticeCoord:
        self.first = False
        self.this_coord = self.next_coord()
        return self.this_coord
    
class LatticeWalker(object):
    
    def __init__(self, d_system: "LatticeSystem", d_coord_rel: LatticeCoord = None) -> None:
        
        self.system = d_system
        self.base_point: LatticePoint = None
        self.valid_positions = False
        self.absolute_position = None
        self.render_position = None
        self.direction_offset = 0
        
        if d_coord_rel is not None:
            self.coord_origin_rel = d_coord_rel
            self.rel_orient_parent = PolarTransform(d_coord_rel.angle_of_leaf(), BRANCH_LENGTH, np.pi)
        else:
            self.coord_origin_rel = LatticeCoord([])
            self.base_point = self.system.get_lattice_point(LatticeCoord([]))
            self.base_point.attached_walker = self
            
            self.direction_offset = 0
            self.absolute_position = PolarTransform(0, 0, 0)
            self.rel_orient_parent = PolarTransform(0, 0, 0)
            self.render_position = copy.deepcopy(self.absolute_position)
        
    def compare_to(self, obj: object):
        return self.coord_origin_rel.compare_to(obj)