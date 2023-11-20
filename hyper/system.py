import copy
import numpy as np

from hyper.lattice import *
from hyper.transforms import PolarTransform, LatticeTransform


class LatticeSystem(object):
    
    def __init__(self) -> None:
        self.lattice_points = []
        self.generate_lattice_points(2)
        self.walker_origin = LatticeWalker(self)
        self.walker_origin.direction_offset = 0
        self.walker_origin.base_point = self.get_lattice_point(LatticeCoord([]))
        self.walker_origin.absolute_position = PolarTransform(0, 0, 0)
        self.walker_origin.render_position = copy.deepcopy(self.walker_origin.absolute_position)
        
        self.lattice_walkers = [self.walker_origin]
        self.generate_lattice_walkers(3)   
    
    def validate_walker_positions(self, walker: LatticeWalker) -> None:
        if not walker.valid_positions:
            parent = self.generate_lattice_walker(walker.coord_origin_rel.coord_in_direction(0))
            if parent.coord_origin_rel.type != LatticeType.ORIGIN:
                self.validate_walker_positions(parent)
                
            
            walker.absolute_position = parent.absolute_position.copy()
            walker.absolute_position.apply_polar_transform(walker.rel_orient_parent)
            walker.render_position = walker.absolute_position.copy()
            walker.render_position.apply_rotation(-walker.direction_offset*2*np.pi/5)
            walker.valid_positions = True
    
    def set_view_origin(self, coord: LatticeCoord, transform: PolarTransform) -> None:
        if self.walker_origin.base_point.coords.compare_to(coord) == 0:
            # recalculate positions
            for lat_walker in self.lattice_walkers:
                lat_walker.valid_positions = False
            
            self.walker_origin.absolute_position = copy.deepcopy(transform)
            self.walker_origin.render_position = copy.deepcopy(self.walker_origin.absolute_position)
            self.walker_origin.valid_positions = True
            
            for walker in self.lattice_walkers:
                self.validate_walker_positions(walker)
        else:
            # regen walkers
            self.walker_origin.direction_offset = 0
            self.walker_origin.base_point = self.get_lattice_point(coord)
            self.walker_origin.base_point.attached_walker=self.walker_origin
            
            self.walker_origin.absolute_position = copy.deepcopy(transform)
            self.walker_origin.render_position = copy.deepcopy(self.walker_origin.absolute_position)
            self.lattice_walkers = [self.walker_origin]
            self.generate_lattice_walkers(3)
        pass
    
    def set_view_origin_lattrans(self, transform: LatticeTransform) -> None:
        self.set_view_origin(transform.base_point.coords, transform.rel_transform)
            
    def get_lattice_point(self, coord: LatticeCoord) -> LatticePoint:
        index = self.find_viable_point_index(coord)
        if index >= len(self.lattice_points):
            L = self.generate_lattice_point(coord)
        else:
            if self.lattice_points[index].coords.compare_to(coord) == 0:
                L = self.lattice_points[index]
            else:
                L = self.generate_lattice_point(coord)
        
        if L.coords.compare_to(coord) == 0:
            return L
        return
    
    def get_lattice_point_if_exists(self, coord: LatticeCoord) -> LatticePoint:
        index = self.find_viable_point_index(coord)
        if index >= len(self.lattice_points):
            return
        else:
            if self.lattice_points[index].coords.compare_to(coord) == 0:
                return self.lattice_points[index]
        return
    
    def find_viable_point_index(self, coord: LatticeCoord) -> int:
        """Finds the index where a lattice point of a given coord should be placed.
        If the lattice point with the given coord exists, it gives the index of it. BINARY SEARCH

        Args:
            coord (LatticeCoord): _description_

        Returns:
            int: _description_
        """
        if coord.type == LatticeType.INVALID:
            print("INVALID LATTICECOORD")
            print(coord.to_string())
            return -1
        min_index = 0
        max_index = len(self.lattice_points) - 1
        if max_index < 0:
            return 0
        
        compare_to_min_index = self.lattice_points[min_index].compare_to(coord)
        compare_to_max_index = self.lattice_points[max_index].compare_to(coord)
        while True:
            if compare_to_min_index >= 0:
                # If the min index is the same or greater than the search coord, return min_index
                # Because if coord==min_index, we would want to return min_index
                # If coord < min_index, we would want to give the index to insert the coord, which is still min_index
                return min_index
            if compare_to_max_index == 0:
                # If coord == max_index, we would want to return the index max_index
                return max_index
            if compare_to_max_index < 0:
                # If coord > max_index, we would want to return the index just after max_index
                return max_index + 1
            if max_index - min_index == 1:
                return max_index
            
            mid_index = (min_index + max_index) // 2
            compare_to_midpoint = self.lattice_points[mid_index].compare_to(coord)
            if compare_to_midpoint < 0:
                min_index = mid_index
                compare_to_min_index = compare_to_midpoint
            else:
                max_index = mid_index
                compare_to_max_index = compare_to_midpoint
            
    def generate_lattice_point(self, coord: LatticeCoord) -> LatticePoint:
        """Generate the lattice point at a given coordinate, also generates all the lattice points 
        below it in the tree (so that it is connected)

        Args:
            coord (LatticeCoord): _description_

        Returns:
            LatticePoint: _description_
        """
        
        if coord.type != LatticeType.INVALID:
            index = self.find_viable_point_index(coord)
            
            if len(self.lattice_points) > 0:
                try:
                    if self.lattice_points[index].compare_to(coord) == 0:
                        return self.lattice_points[index]
                except:
                    pass
            
            L = LatticePoint(coord, self)
            index = self.find_viable_point_index(coord)
            self.lattice_points.insert(index, L)
            return L
        return
    
    def generate_lattice_points(self, radius: int) -> None:
        """Generate and validate all lattice points with a tree of a specified radius

        Args:
            radius (int): _description_
        """
        iter = LatticeCircularIterator(radius)
        while iter.has_next():
            self.generate_lattice_point(iter.this_coord)
            iter.next()
    
    def find_viable_walker_index(self, coord: LatticeCoord) -> int:
        """Finds the index where a lattice walker of a given coord should be placed.
        If the lattice walker with the given coord exists, it gives the index of it. BINARY SEARCH

        Args:
            coord (LatticeCoord): _description_

        Returns:
            int: _description_
        """
        if coord.type == LatticeType.INVALID:
            return -1
        min_index = 0
        max_index = len(self.lattice_walkers) - 1
        if max_index < 0:
            return 0
        
        compare_to_min_index = self.lattice_walkers[min_index].compare_to(coord)
        compare_to_max_index = self.lattice_walkers[max_index].compare_to(coord)
        
        while True:
            if compare_to_min_index >= 0:
                # If the min index is the same or greater than the search coord, return min_index
                # Because if coord==min_index, we would want to return min_index
                # If coord < min_index, we would want to give the index to insert the coord, which is still min_index
                return min_index
            if compare_to_max_index == 0:
                # If coord == max_index, we would want to return the index max_index
                return max_index
            if compare_to_max_index < 0:
                # If coord > max_index, we would want to return the index just after max_index
                return max_index + 1
            if max_index - min_index == 1:
                return max_index
            
            mid_index = (min_index + max_index) // 2
            compare_to_midpoint = self.lattice_walkers[mid_index].compare_to(coord)
            if compare_to_midpoint < 0:
                min_index = mid_index
                compare_to_min_index = compare_to_midpoint
            else:
                max_index = mid_index
                compare_to_max_index = compare_to_midpoint
    
    def generate_lattice_walker(self, coord: LatticeCoord) -> LatticeWalker:
        """Generate the lattice walker at a given coordinate (walker origin relative),
        also generates all the lattice walkers below it in the tree (so that it is connected)

        Args:
            coord (LatticeCoord): _description_

        Returns:
            LatticeWalker: _description_
        """
        if coord.type != LatticeType.INVALID:
            index = self.find_viable_walker_index(coord)
            if len(self.lattice_walkers) > 0:
                try:
                    if self.lattice_walkers[index].compare_to(coord) == 0:
                        return self.lattice_walkers[index]
                except:
                    pass    
            
            
            temp = LatticeWalker(d_coord_rel=coord, d_system=self)
            
            if coord.type != LatticeType.ORIGIN:
                parent = self.generate_lattice_walker(coord.coord_in_direction(0))
                temp.absolute_position = temp.rel_orient_parent.copy()
                temp.absolute_position.preapply_polar_transform(parent.absolute_position)
                temp.base_point = self.get_lattice_point(parent.base_point.coords.coord_in_direction(parent.direction_offset + coord.direction_of_leaf()))
                temp.base_point.attached_walker = temp
                temp.direction_offset = parent.base_point.coords.direction_after_travel(parent.direction_offset + coord.direction_of_leaf())
                
                # if len(coord.coord) == 1:
                #     # print(temp.absolute_position.to_string())
                #     temp.absolute_position.m *= -1
                #     # print(temp.absolute_position.to_string())
                #     # print(parent.absolute_position.to_string())
                #     # asdf
                temp.render_position = copy.deepcopy(temp.absolute_position)
                temp.render_position.apply_rotation(-(temp.direction_offset) * 2*np.pi/5)
            temp.valid_positions = True
            index = self.find_viable_walker_index(coord)
            self.lattice_walkers.insert(index, temp)
            return temp
        return
    
    def generate_lattice_walkers(self, radius: int) -> None:
        """Generate and validate all lattice points with a tree of a specified radius

        Args:
            radius (int): _description_
        """
        iter = LatticeCircularIterator(radius)
        while iter.has_next():
            self.generate_lattice_walker(iter.this_coord)
            iter.next()
    
    def get_lattice_walker(self, coord: LatticeCoord) -> LatticeWalker:
        index = self.find_viable_walker_index(coord)
        temp = self.lattice_walkers[index]
        
        if temp.coord_origin_rel.compare_to(coord) == 0:
            return temp
        return
    
    def update(self) -> None:
        for lat_pt in self.lattice_points:
            lat_pt.update()