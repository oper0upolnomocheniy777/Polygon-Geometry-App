import math
import pygame
from src.polygon import Polygon

def multiply_matrices(a, b):
    """Умножение матриц 3x3"""
    result = [[0, 0, 0],
              [0, 0, 0], 
              [0, 0, 0]]
    
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += a[i][k] * b[k][j]
    
    return result

def multiply_matrix_vector(matrix, vector):
    """Умножение матрицы 3x3 на вектор [x, y, 1]"""
    x = matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * 1
    y = matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * 1
    return (x, y)

def translation_matrix(dx, dy):
    """Матрица смещения"""
    return [
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ]

def rotation_matrix(angle, cx=0, cy=0):
    """Матрица поворота вокруг точки (cx, cy)"""
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Матрица поворота вокруг начала координат
    rotation = [
        [cos_a, -sin_a, 0],
        [sin_a, cos_a, 0],
        [0, 0, 1]
    ]
    
    if cx == 0 and cy == 0:
        return rotation
    
    # Композиция преобразований: смещение в начало -> поворот -> обратное смещение
    translate_to_origin = translation_matrix(-cx, -cy)
    translate_back = translation_matrix(cx, cy)
    
    # Умножаем матрицы: translate_back * rotation * translate_to_origin
    temp = multiply_matrices(rotation, translate_to_origin)
    result = multiply_matrices(translate_back, temp)
    
    return result

def scaling_matrix(sx, sy, cx=0, cy=0):
    """Матрица масштабирования относительно точки (cx, cy)"""
    # Матрица масштабирования относительно начала координат
    scale = [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]
    
    if cx == 0 and cy == 0:
        return scale
    
    # Композиция преобразований: смещение в начало -> масштаб -> обратное смещение
    translate_to_origin = translation_matrix(-cx, -cy)
    translate_back = translation_matrix(cx, cy)
    
    temp = multiply_matrices(scale, translate_to_origin)
    result = multiply_matrices(translate_back, temp)
    
    return result

def get_polygon_center(polygon):
    """Вычисляет центр полигона (среднее арифметическое всех вершин)"""
    if not polygon.points:
        return (0, 0)
    
    sum_x = sum(point[0] for point in polygon.points)
    sum_y = sum(point[1] for point in polygon.points)
    
    center_x = sum_x / len(polygon.points)
    center_y = sum_y / len(polygon.points)
    
    return (center_x, center_y)

def apply_transform(polygon, matrix):
    """Применяет матрицу преобразования ко всем вершинам полигона"""
    transformed_points = []
    for point in polygon.points:
        transformed_point = multiply_matrix_vector(matrix, point)
        transformed_points.append(transformed_point)
    
    polygon.points = transformed_points

class TransformManager:
    """Менеджер для управления аффинными преобразованиями"""
    
    def __init__(self, polygon_manager):
        self.polygon_manager = polygon_manager
        self.transform_history = []
    
    def translate_selected(self, dx, dy):
        """Смещает выбранный полигон на dx, dy"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            matrix = translation_matrix(dx, dy)
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def rotate_around_point(self, angle, point):
        """Поворачивает выбранный полигон вокруг заданной точки"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            matrix = rotation_matrix(angle, point[0], point[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def rotate_around_center(self, angle):
        """Поворачивает выбранный полигон вокруг своего центра"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            center = get_polygon_center(selected_polygon)
            matrix = rotation_matrix(angle, center[0], center[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def scale_around_point(self, sx, sy, point):
        """Масштабирует выбранный полигон относительно заданной точки"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            matrix = scaling_matrix(sx, sy, point[0], point[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def scale_around_center(self, sx, sy):
        """Масштабирует выбранный полигон относительно своего центра"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            center = get_polygon_center(selected_polygon)
            matrix = scaling_matrix(sx, sy, center[0], center[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def get_selected_polygon(self):
        """Возвращает выбранный полигон"""
        for polygon in self.polygon_manager.polygons:
            if polygon.is_selected:
                return polygon
        return None