import numpy as np
import hyper_utils

class PolarTransform(object):
    
    def __init__(self, dN: float, dS: float, dM: float) -> None:
        self.n, self.s, self.m = dN, dS, dM
    
    def get_matrix(self) -> np.ndarray:
        start_transform = hyper_utils.rotation_mat(self.n)
        start_transform = start_transform @ hyper_utils.translation_mat_z(self.s)
        start_transform = start_transform @ hyper_utils.rotation_mat(self.m)
        return start_transform
    
    def copy(self) -> "PolarTransform":
        return PolarTransform(self.n, self.s, self.m)
    
    def apply_rotation(self, a: float) -> None:
        self.m += a
    
    def apply_translation_z(self, l: float) -> None:
        self.n = np.arctan2((np.cos(self.n)*np.sin(self.m)+np.cos(self.m)*np.sin(self.n)*np.cosh(self.s))*np.sinh(l)+np.sin(self.n)*np.sinh(self.s)*np.cosh(l),
                       (np.cos(self.m)*np.cos(self.n)*np.cosh(self.s)-np.sin(self.m)*np.sin(self.n))*np.sinh(l)+np.cos(self.n)*np.cosh(l)*np.sinh(self.s))
        self.s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.cos(self.m)*np.sinh(l)*np.sinh(self.s))
        self.m = np.arctan2((np.sin(self.m)*np.sinh(self.s)),(np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.cos(self.m)))
    
    def apply_translation_y(self, l: float) -> None:
        self.n = np.arctan2((np.cos(self.n)*np.sin(self.m)-np.cosh(self.s)*np.sin(self.m)*np.sin(self.n))*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.sin(self.n),
                            (-np.cos(self.m)*np.cosh(self.s)*np.sin(self.n)-np.cos(self.m)*np.sin(self.n))*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.cos(self.n))
        self.s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.sin(self.m)*np.sinh(l)*np.sinh(self.s))
        self.m = np.arctan2(-(np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.sin(self.m)),(np.cos(self.m)*np.sinh(self.s)))
    
    def preapply_rotation(self, a: float) -> None:
        self.n += a
    
    def preapply_translation_z(self, l: float) -> None:
        self.n = np.arctan2(np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s)*np.sin(self.n),np.cos(self.n)*np.sinh(self.s))
        self.s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.sin(self.n)*np.sinh(l)*np.sinh(self.s))
        self.m = np.arctan2(-np.cos(self.m)*np.cos(self.n)*np.sinh(l)+np.sin(self.m)*(np.cosh(self.s)*np.sinh(l)*np.sin(self.n)+np.cosh(l)*np.sinh(self.s)),
                       np.cos(self.n)*np.sin(self.m)*np.sinh(l)+np.cos(self.m)*(np.cosh(self.s)*np.sinh(l)*np.sin(self.n)+np.cosh(l)*np.sinh(self.s)))
    
    def preapply_translation_y(self, l: float) -> None:
        self.n = np.arctan2(np.sin(self.n)*np.sinh(self.s),np.cosh(self.s)*np.sinh(l)+np.cos(self.n)*np.cosh(l)*np.sinh(self.s))
        self.s = np.arccosh(np.cosh(l)*np.cosh(self.s)+np.cos(self.n)*np.sinh(l)*np.sinh(self.s))
        self.m = np.arctan2(np.cos(self.m)*np.sin(self.n)*np.sinh(l)+np.sin(self.m)*(np.cos(self.n)*np.sinh(l)*np.cosh(self.s)+np.cosh(l)*np.sinh(self.s)),
                       np.cos(self.m)*(np.cos(self.n)*np.cosh(self.s)*np.sinh(l)+np.cosh(l)*np.sinh(self.s))-np.sin(self.m)*np.sin(self.n)*np.sinh(l))
    
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
            self.preapply_translation_z(pt.s)
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
    
            