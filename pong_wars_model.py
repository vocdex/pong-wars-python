"""
Model part for pong wars.
"""

import random
import math
import numpy


def calculate_scores(squares: numpy.ndarray):
    unique, counts = numpy.unique(squares, return_counts=True)
    return dict(zip(unique, counts))


def calculate_overwrite_area(position: numpy.ndarray, size: numpy.ndarray, width: int, height: int):
    position_int = numpy.floor(position).astype(int)
    position_top_left = numpy.clip(position_int, [0, 0], [width, height]).astype(int)
    position_bottom_right = numpy.clip(position_top_left + size, [0, 0], [width, height]).astype(int)
    return (position_top_left, (position_bottom_right - position_top_left))


def create_squares(width_square_num: int, height_square_num: int, player_num: int):
    squares = numpy.zeros((width_square_num, height_square_num))
    for i in range(width_square_num):
        for j in range(height_square_num):
            if player_num == 2:
                squares[i][j] = 1 if i < width_square_num / 2 else 2
            elif player_num == 4:
                if i < width_square_num / 2:
                    squares[i][j] = 1 if j < height_square_num / 2 else 3
                else:
                    squares[i][j] = 2 if j < height_square_num / 2 else 4
    return squares


def update_square_and_bounce(position: numpy.ndarray, direction: numpy.ndarray, player_index: int, squares: numpy.ndarray, square_size: int, pong_radius: int):
    updated_direction = direction
    for angle in range(0, 360, 90):
        rad = math.radians(angle)
        check_pos = position + numpy.array([math.cos(rad), math.sin(rad)]) * pong_radius
        i, j = (check_pos // square_size).astype(int)
        if 0 <= i < squares.shape[0] and 0 <= j < squares.shape[1]:
            if squares[i][j] != player_index:
                squares[i][j] = player_index
                if abs(math.cos(rad)) > abs(math.sin(rad)):
                    updated_direction[0] *= -1.0
                else:
                    updated_direction[1] *= -1.0
                updated_direction += random.uniform(-0.01, 0.01)
    updated_direction /= numpy.linalg.norm(updated_direction)
    return updated_direction


def overwrite_squares(player_index: int, top_left_position: numpy.ndarray, size: numpy.ndarray, squares: numpy.ndarray, square_size: int):
    i_start, j_start = top_left_position // square_size
    i_end, j_end = (top_left_position + size) // square_size
    for i in range(i_start, i_end):
        for j in range(j_start, j_end):
            squares[i][j] = player_index


def check_boundary_collision(position: numpy.ndarray, direction: numpy.ndarray, width: int, height: int, pong_radius: int, pong_speed: int):
    x, y = position
    dx, dy = direction
    if x + dx  * pong_speed > width - pong_radius // 2 or x + dx * pong_speed < pong_radius // 2:
        dx = -dx
    if y + dy * pong_speed > height - pong_radius // 2 or y + dy * pong_speed < pong_radius // 2:
        dy = -dy
    return numpy.array([dx, dy], dtype=float)

        