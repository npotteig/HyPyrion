import numpy as np
import copy

from hyper.system import LatticeSystem
from hyper.coord import LatticeCoord
from hyper.render_utils import BRANCH_LENGTH
from hyper.transforms import PolarTransform


class LatticeWalker(object):
    
    def __init__(self, d_system: LatticeSystem, d_coord_rel: LatticeCoord = None) -> None:
        
        self.system = d_system
        self.base_point = None
        self.valid_positions = False
        self.absolute_position = None
        self.render_position = None
        self.direction_offset = None
        
        if d_coord_rel is not None:
            self.coord_origin_rel = d_coord_rel
            self.rel_orient_parent = PolarTransform(d_coord_rel.angle_of_leaf(), BRANCH_LENGTH, np.pi)
        else:
            self.coord_origin_rel = LatticeCoord([])
            self.base_point = self.system.get_lattice_point(LatticeCoord([]))
            self.base_point.attached_walker = self
            
            self.direction_offset = 0
            self.absolute_position = PolarTransform(0, 0.2, 0.3)
            self.rel_orient_parent = PolarTransform(0, 0, 0)
            self.render_position = copy.deepcopy(self.absolute_position)
        
    def compare_to(self, obj: object):
        return self.coord_origin_rel.compare_to(obj)