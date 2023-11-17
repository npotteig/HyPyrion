from enum import Enum
import numpy as np
import copy

from hyper.point import LatticePoint

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
        return self.direction_of_leaf * 2*np.pi / 5
    
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