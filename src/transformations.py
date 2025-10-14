import math
import pygame
from src.polygon import Polygon

def multiply_matrices(a, b):
    """Multiply 3x3 matrices"""
    result = [[0, 0, 0],
              [0, 0, 0], 
              [0, 0, 0]]
    
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += a[i][k] * b[k][j]
    
    return result

def multiply_matrix_vector(matrix, vector):
    """Multiply 3x3 matrix by vector [x, y, 1]"""
    x = matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * 1
    y = matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * 1
    return (x, y)

def translation_matrix(dx, dy):
    """Translation matrix"""
    return [
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ]

def rotation_matrix(angle, cx=0, cy=0):
    """Rotation matrix around point (cx, cy)"""
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Rotation matrix around origin
    rotation = [
        [cos_a, -sin_a, 0],
        [sin_a, cos_a, 0],
        [0, 0, 1]
    ]
    
    if cx == 0 and cy == 0:
        return rotation
    
    # Composition: translate to origin -> rotate -> translate back
    translate_to_origin = translation_matrix(-cx, -cy)
    translate_back = translation_matrix(cx, cy)
    
    # Multiply matrices: translate_back * rotation * translate_to_origin
    temp = multiply_matrices(rotation, translate_to_origin)
    result = multiply_matrices(translate_back, temp)
    
    return result

def scaling_matrix(sx, sy, cx=0, cy=0):
    """Scaling matrix relative to point (cx, cy)"""
    # Scaling matrix relative to origin
    scale = [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]
    
    if cx == 0 and cy == 0:
        return scale
    
    # Composition: translate to origin -> scale -> translate back
    translate_to_origin = translation_matrix(-cx, -cy)
    translate_back = translation_matrix(cx, cy)
    
    temp = multiply_matrices(scale, translate_to_origin)
    result = multiply_matrices(translate_back, temp)
    
    return result

def get_polygon_center(polygon):
    """Calculate polygon center (average of all vertices)"""
    if not polygon.points:
        return (0, 0)
    
    sum_x = sum(point[0] for point in polygon.points)
    sum_y = sum(point[1] for point in polygon.points)
    
    center_x = sum_x / len(polygon.points)
    center_y = sum_y / len(polygon.points)
    
    return (center_x, center_y)

def apply_transform(polygon, matrix):
    """Apply transformation matrix to all polygon vertices"""
    transformed_points = []
    for point in polygon.points:
        transformed_point = multiply_matrix_vector(matrix, point)
        transformed_points.append(transformed_point)
    
    polygon.points = transformed_points

class TransformManager:
    """Manager for affine transformations"""
    
    def __init__(self, polygon_manager):
        self.polygon_manager = polygon_manager
        self.transform_history = []
    
    def translate_selected(self, dx, dy):
        """Translate selected polygon by dx, dy"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            matrix = translation_matrix(dx, dy)
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def rotate_around_point(self, angle, point):
        """Rotate selected polygon around given point"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            matrix = rotation_matrix(angle, point[0], point[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def rotate_around_center(self, angle):
        """Rotate selected polygon around its center"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            center = get_polygon_center(selected_polygon)
            matrix = rotation_matrix(angle, center[0], center[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def scale_around_point(self, sx, sy, point):
        """Scale selected polygon relative to given point"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            matrix = scaling_matrix(sx, sy, point[0], point[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def scale_around_center(self, sx, sy):
        """Scale selected polygon relative to its center"""
        selected_polygon = self.get_selected_polygon()
        if selected_polygon:
            center = get_polygon_center(selected_polygon)
            matrix = scaling_matrix(sx, sy, center[0], center[1])
            apply_transform(selected_polygon, matrix)
            return True
        return False
    
    def get_selected_polygon(self):
        """Return selected polygon"""
        for polygon in self.polygon_manager.polygons:
            if polygon.is_selected:
                return polygon
        return None