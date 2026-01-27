"""
Вспомогательные функции
"""

import math
import random
import arcade

def get_distance(point1, point2):
    """Вычисление расстояния между двумя точками"""
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def get_direction(point1, point2):
    """Получение направления от точки к точке"""
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    distance = max(0.1, math.sqrt(dx**2 + dy**2))
    return dx/distance, dy/distance

def get_angle_between_points(point1, point2):
    """Получение угла между двумя точками"""
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.degrees(math.atan2(dy, dx))

def random_position_in_rect(rect):
    """Случайная позиция внутри прямоугольника"""
    x = random.randint(rect[0], rect[0] + rect[2])
    y = random.randint(rect[1], rect[1] + rect[3])
    return x, y

def is_point_in_rect(point, rect):
    """Проверка, находится ли точка внутри прямоугольника"""
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh
