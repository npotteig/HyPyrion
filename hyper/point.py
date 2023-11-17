from hyper.system import LatticeSystem
from hyper.coord import LatticeCoord

class LatticePoint(object):
    
    def __init__(self, d_coord: LatticeCoord, d_system: LatticeSystem) -> None:
        self.coords = d_coord
        self.system = d_system
        self.attached_walker = None
    
    def compare_to(self, obj: object):
        return self.coords.compare_to(obj)
    
    