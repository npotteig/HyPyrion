import numpy as np
import copy

from hyper.coord import LatticeCoord

class LatticeCircularIterator(object):
    
    def __init__(self, d_radius: int) -> None:
        self.radius = d_radius
        self.this_coord = self.first_coord()
        self.first = True
        
    def first_coord(self) -> LatticeCoord:
        coord = np.zeros(self.radius).tolist()
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