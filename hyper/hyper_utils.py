import numpy as np

def rotation_mat(theta: float) -> np.ndarray:
    P = np.array([[1, 0, 0, 0],
                  [0, np.cos(theta), -np.sin(theta), 0],
                  [0, np.sin(theta), np.cos(theta), 0],
                  [0, 0, 0, 0]])
    return P

def translation_mat_y(y_trans: float) -> np.ndarray:
    P = np.array([[np.cosh(y_trans), 0, np.sinh(y_trans), 0],
                 [0, 1, 0, 0],
                 [np.sinh(y_trans), 0, np.cosh(y_trans), 0],
                 [0, 0, 0, 0]])
    return P

def translation_mat_z(y_trans: float) -> np.ndarray:
    P = np.array([[np.cosh(y_trans), np.sinh(y_trans), 0, 0],
                  [np.sinh(y_trans), np.cosh(y_trans), 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 0]])
    return P

def polar_vector(r: float, theta: float) -> np.ndarray:
    return np.array([np.cosh(r),
                     np.sinh(r) * np.cos(theta),
                     np.sinh(r) * np.sin(theta),
                     0])

def project_onto_poincare_disc(point: np.ndarray) -> np.ndarray:
    scale = 1 / (point[0] + 1)
    return point[1:] * scale