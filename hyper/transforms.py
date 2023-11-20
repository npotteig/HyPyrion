import numpy as np
import copy 
from typing import ForwardRef

import hyper.hyper_utils as hyper_utils
from hyper.render_utils import BRANCH_LENGTH, project_onto_screen


class PolarTransform(object):
    
    def __init__(self, dN: float, dS: float, dM: float) -> None:
        self.n, self.s, self.m = dN, dS, dM
        
    def to_string(self) -> str:
        return str(self.n) + ", " + str(self.s) + ", " + str(self.m)
    
    def get_matrix(self) -> np.ndarray:
        start_transform = hyper_utils.rotation_mat(self.n)
        P = hyper_utils.translation_mat_y(0)
        P = P @ hyper_utils.translation_mat_z(self.s)
        start_transform = start_transform @ P
        start_transform = start_transform @ hyper_utils.rotation_mat(self.m)
        return start_transform
    
    def copy(self) -> "PolarTransform":
        return PolarTransform(self.n, self.s, self.m)
    
    def apply_rotation(self, a: float) -> None:
        self.m += a
    
    def apply_translation_z(self, l: float) -> None:
        temp_n = np.arctan2((np.cos(self.n)*np.sin(self.m)+np.cos(self.m)*np.sin(self.n)*np.cosh(self.s))*np.sinh(l)+np.sin(self.n)*np.sinh(self.s)*np.cosh(l),
                       (np.cos(self.m)*np.cos(self.n)*np.cosh(self.s)-np.sin(self.m)*np.sin(self.n))*np.sinh(l)+np.cos(self.n)*np.cosh(l)*np.sinh(self.s))
        temp_s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.cos(self.m)*np.sinh(l)*np.sinh(self.s))
        temp_m = np.arctan2((np.sin(self.m)*np.sinh(self.s)),(np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.cos(self.m)))
        
        self.n = temp_n
        self.s = temp_s
        self.m = temp_m    
    
    def apply_translation_y(self, l: float) -> None:
        temp_n = np.arctan2((np.cos(self.n)*np.sin(self.m)-np.cosh(self.s)*np.sin(self.m)*np.sin(self.n))*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.sin(self.n),
                            (-np.cos(self.m)*np.cosh(self.s)*np.sin(self.n)-np.cos(self.m)*np.sin(self.n))*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.cos(self.n))
        temp_s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.sin(self.m)*np.sinh(l)*np.sinh(self.s))
        temp_m = np.arctan2(-(np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.sin(self.m)),(np.cos(self.m)*np.sinh(self.s)))
    
        self.n = temp_n
        self.s = temp_s
        self.m = temp_m
    
    def preapply_rotation(self, a: float) -> None:
        self.n += a
    
    def preapply_translation_z(self, l: float) -> None:
        temp_n = np.arctan2(np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.sin(self.n),np.cos(self.n)*np.sinh(self.s))
        temp_s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.sin(self.n)*np.sinh(l)*np.sinh(self.s))
        temp_m = np.arctan2(-np.cos(self.m)*np.cos(self.n)*np.sinh(l)+np.sin(self.m)*(np.cosh(self.s)*np.sinh(l)*np.sin(self.n)+np.cosh(l)*np.sinh(self.s)),
                       np.cos(self.n)*np.sin(self.m)*np.sinh(l)+np.cos(self.m)*(np.cosh(self.s)*np.sinh(l)*np.sin(self.n)+np.cosh(l)*np.sinh(self.s)))
        
        self.n = temp_n
        self.s = temp_s
        self.m = temp_m
        
    def preapply_translation_y(self, l: float) -> None:
        temp_n = np.arctan2(np.sin(self.n)*np.sinh(self.s),np.cosh(self.s)*np.sinh(l)+np.cos(self.n)*np.cosh(l)*np.sinh(self.s))
        temp_s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.cos(self.n)*np.sinh(l)*np.sinh(self.s))
        temp_m = np.arctan2(np.cos(self.m)*np.sin(self.n)*np.sinh(l)+np.sin(self.m)*(np.cos(self.n)*np.sinh(l)*np.cosh(self.s)+np.cosh(l)*np.sinh(self.s)),
                       np.cos(self.m)*(np.cos(self.n)*np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s))-np.sin(self.m)*np.sin(self.n)*np.sinh(l))
        
        self.n = temp_n
        self.s = temp_s
        self.m = temp_m
    
    def apply_polar_transform(self, pt: "PolarTransform") -> None:
        if isinstance(pt, PolarTransform):
            self.apply_rotation(pt.n)
            self.apply_translation_z(pt.s)
            self.apply_rotation(pt.m)
        else:
            raise TypeError("Unsuppported Type")
    
    def preapply_polar_transform(self, pt: "PolarTransform") -> None:
        if isinstance(pt, PolarTransform):
            self.preapply_rotation(pt.m)
            self.preapply_translation_y(pt.s)
            self.preapply_rotation(pt.n)
        else:
            raise TypeError("Unsuppported Type")

    def inverse(self) -> "PolarTransform":
        return PolarTransform(-self.m, -self.s, -self.n)
    
    def distance_to(self, p: "PolarTransform") -> float:
        """
        Calculate geodesic distance between two points

        Args:
            p (PolarTransform): PolarTransform of second point

        Returns:
            float: geodesic distance
        """
        copy_transform = self.copy()
        copy_transform.apply_polar_transform(p.inverse())
        return copy_transform.s
    
    def pos_on_screen(self) -> np.ndarray:
        transfrom = self.get_matrix()
        p = np.array([1, 0, 0, 0])
        p = transfrom @ p
        p = project_onto_screen(p)
        return p


class LatticeTransform(object):
    
    from hyper.lattice import LatticeCoord, LatticePoint
    
    def __init__(self, transform: PolarTransform, coord: LatticeCoord, d_system: "LatticeSystem") -> None:
        self.rel_transform = transform
        self.system = d_system
        
        self.base_point = d_system.get_lattice_point(coord)
        
    def relative_transform_in_direction(self, direction: int) -> PolarTransform:
        p = copy.deepcopy(self.rel_transform)
        p.apply_polar_transform(PolarTransform(direction*2*np.pi/5, BRANCH_LENGTH, np.pi))
        # print(p.to_string())
        return p
    
    def get_lattice_point_in_direction_if_exists(self, direction: int) -> LatticePoint:
        return self.system.get_lattice_point_if_exists(self.base_point.coords.coord_in_direction(direction))
    
    def step_basepoint_in_direction(self, direction: int) -> None:
        """Steps the basepoint in a direction, without changing
        the actual transformation

        Args:
            direction (int): _description_
        """
        new_base_point = self.system.get_lattice_point(self.base_point.coords.coord_in_direction(direction))
        # new_walker = self.system.get_lattice_walker(self.base_point.coords.coord_in_direction(direction))
        turn_amount = self.base_point.coords.direction_after_travel(direction)
        self.base_point = new_base_point
        self.rel_transform.apply_polar_transform(PolarTransform(direction*2*np.pi/5, BRANCH_LENGTH, np.pi-turn_amount*2*np.pi/5))
        print(self.rel_transform.to_string())
    
    def shift_to_nearer_basepoint(self) -> None:
        """Changes base point so that the rel_transform has a shorter magnitude.
        If there is no shorter one, it does nothing
        """
        transform_len = np.abs(self.rel_transform.s)
        for i in range(5):
            if np.abs(self.relative_transform_in_direction(i).s) < transform_len:
                self.step_basepoint_in_direction(i)
                return
        return
    
    def resolve_base_point(self) -> None:
        stepped = True
        while stepped:
            stepped = False
            transform_len = np.abs(self.rel_transform.s)
            for i in range(5):
                if np.abs(self.relative_transform_in_direction(i).s) < transform_len:
                    self.step_basepoint_in_direction(i)
                    stepped = True
    
    def try_resolve_base_point(self) -> bool:
        stepped = True
        while stepped:
            stepped = False
            transform_len = np.abs(self.rel_transform.s)
            for i in range(5):
                if np.abs(self.relative_transform_in_direction(i).s) < transform_len:
                    if self.get_lattice_point_in_direction_if_exists(i) is not None:
                        self.step_basepoint_in_direction(i)
                        stepped = True
                    else:
                        return False
        return True
    
    def apply_polar_transform(self, T: PolarTransform) -> None:
        self.rel_transform.apply_polar_transform(T)
        self.resolve_base_point()
    
    def try_apply_polar_transform(self, T: PolarTransform) -> bool:
        self.rel_transform.apply_polar_transform(T)
        return self.try_resolve_base_point()
    
    
        