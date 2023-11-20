import pygame
import hyper.hyper_utils as hyper_utils
import numpy as np

SCALE = 400
BRANCH_LENGTH: float = 1.255
DEPTH: int = 3

def scale_to_screen(point: np.ndarray) -> np.ndarray:
    return point * SCALE + SCALE

def project_onto_screen(point: np.ndarray) -> np.ndarray:
    return scale_to_screen(hyper_utils.project_onto_poincare_disc(point))

def draw_line(screen, cur_transform: np.ndarray, angle: float = None, line_length: float = 0) -> None:
    transform_copy = cur_transform.copy()
    if angle is not None:
        transform_copy = transform_copy @ hyper_utils.rotation_mat(angle)
    inc = 0.3
    for i in np.arange(0, line_length, inc):
        next_point = hyper_utils.polar_vector(i, 0)
        next_point = transform_copy @ next_point
        next_point = project_onto_screen(next_point)
        if (i > 0):
            pygame.draw.line(screen, 'black', prev_point[:-1], next_point[:-1], width=4)
        prev_point = next_point
    

def draw_order5_tiling(screen, cur_transform: np.ndarray) -> None:
    transform_copy = cur_transform.copy()
    for i in range(5):
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw3_branch_sector(screen, transform_copy, 0)

def draw3_branch_sector(screen, cur_transform: np.ndarray, depth: int) -> None:
    draw_line(screen, cur_transform, 0, BRANCH_LENGTH)
    transform_copy = cur_transform.copy()
    transform_copy = transform_copy @ hyper_utils.translation_mat_z(BRANCH_LENGTH)
    transform_copy = transform_copy @ hyper_utils.rotation_mat(np.pi)

    if (depth < DEPTH):
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw2_branch_sector(screen, transform_copy, depth + 1)
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw3_branch_sector(screen, transform_copy, depth + 1)
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw3_branch_sector(screen, transform_copy, depth + 1)

def draw2_branch_sector(screen, cur_transform: np.ndarray, depth: int) -> None:
    draw_line(screen, cur_transform, 0, BRANCH_LENGTH)
    transform_copy = cur_transform.copy()
    transform_copy = transform_copy @ hyper_utils.translation_mat_z(BRANCH_LENGTH)
    transform_copy = transform_copy @ hyper_utils.rotation_mat(np.pi)

    if (depth < DEPTH):
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw_line(screen, transform_copy, 0, BRANCH_LENGTH)
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw2_branch_sector(screen, transform_copy, depth + 1)
        transform_copy = transform_copy @ hyper_utils.rotation_mat(2 * np.pi / 5)
        draw3_branch_sector(screen, transform_copy, depth + 1)
