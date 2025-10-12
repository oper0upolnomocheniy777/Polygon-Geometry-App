import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.transformations import *
from src.polygon import Polygon

def test_translation():
    """Тест смещения"""
    poly = Polygon(points=[(0, 0), (10, 0), (10, 10)])
    matrix = translation_matrix(5, 5)
    apply_transform(poly, matrix)
    
    expected = [(5, 5), (15, 5), (15, 15)]
    assert poly.points == expected, f"Expected {expected}, got {poly.points}"

def test_rotation():
    """Тест поворота"""
    poly = Polygon(points=[(0, 0), (10, 0)])
    matrix = rotation_matrix(90, 0, 0)
    apply_transform(poly, matrix)
    
    # Поворот на 90 градусов вокруг начала координат
    # (0,0) -> (0,0), (10,0) -> (0,10)
    expected_x1, expected_y1 = 0, 0
    expected_x2, expected_y2 = 0, 10
    
    x1, y1 = poly.points[0]
    x2, y2 = poly.points[1]
    
    assert abs(x1 - expected_x1) < 0.001 and abs(y1 - expected_y1) < 0.001
    assert abs(x2 - expected_x2) < 0.001 and abs(y2 - expected_y2) < 0.001

def test_scaling():
    """Тест масштабирования"""
    poly = Polygon(points=[(2, 2), (4, 2), (4, 4)])
    matrix = scaling_matrix(2, 2, 2, 2)
    apply_transform(poly, matrix)
    
    expected = [(2, 2), (6, 2), (6, 6)]
    for i, (point, expected_point) in enumerate(zip(poly.points, expected)):
        assert abs(point[0] - expected_point[0]) < 0.001
        assert abs(point[1] - expected_point[1]) < 0.001

def test_matrix_multiplication():
    """Тест умножения матриц"""
    a = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    
    b = [[9, 8, 7],
         [6, 5, 4], 
         [3, 2, 1]]
    
    result = multiply_matrices(a, b)
    expected = [[30, 24, 18],
                [84, 69, 54],
                [138, 114, 90]]
    
    for i in range(3):
        for j in range(3):
            assert result[i][j] == expected[i][j]

if __name__ == "__main__":
    test_translation()
    test_rotation() 
    test_scaling()
    test_matrix_multiplication()
    print("Все тесты пройдены!")