'''import sys
import os

# Добавляем src в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.algorithms import (
    classify_point, 
    find_intersection, 
    is_convex_polygon,
    point_in_convex_polygon,
    point_in_nonconvex_polygon,
    point_in_polygon
)

def test_classify_point():
    """Тест классификации точки относительно ребра"""
    print("=== Тест classify_point ===")
    
    # Тест 1: Точка слева
    result = classify_point((0, 0), (1, 0), (0.5, 0.5))
    print(f"Точка (0.5, 0.5) относительно ребра ((0,0), (1,0)): {result}")
    assert result == "left", "Должно быть 'left'"
    
    # Тест 2: Точка справа
    result = classify_point((0, 0), (1, 0), (0.5, -0.5))
    print(f"Точка (0.5, -0.5) относительно ребра ((0,0), (1,0)): {result}")
    assert result == "right", "Должно быть 'right'"
    
    # Тест 3: Точка на прямой
    result = classify_point((0, 0), (1, 1), (0.5, 0.5))
    print(f"Точка (0.5, 0.5) относительно ребра ((0,0), (1,1)): {result}")
    assert result == "on", "Должно быть 'on'"
    
    print(" Все тесты classify_point пройдены!\n")

def test_find_intersection():
    """Тест поиска пересечения отрезков"""
    print("=== Тест find_intersection ===")
    
    # Тест 1: Отрезки пересекаются
    edge1 = ((0, 0), (1, 1))
    edge2 = ((0, 1), (1, 0))
    result = find_intersection(edge1, edge2)
    print(f"Пересечение ((0,0)-(1,1)) и ((0,1)-(1,0)): {result}")
    assert result == (0.5, 0.5), f"Должно быть (0.5, 0.5), получили {result}"
    
    # Тест 2: Отрезки не пересекаются
    edge1 = ((0, 0), (0, 1))
    edge2 = ((1, 0), (1, 1))
    result = find_intersection(edge1, edge2)
    print(f"Пересечение ((0,0)-(0,1)) и ((1,0)-(1,1)): {result}")
    assert result is None, "Должно быть None"
    
    # Тест 3: Параллельные отрезки
    edge1 = ((0, 0), (1, 0))
    edge2 = ((0, 1), (1, 1))
    result = find_intersection(edge1, edge2)
    print(f"Пересечение ((0,0)-(1,0)) и ((0,1)-(1,1)): {result}")
    assert result is None, "Должно быть None"
    
    print(" Все тесты find_intersection пройдены!\n")

def test_polygon_algorithms():
    """Тест алгоритмов для полигонов"""
    print("=== Тест алгоритмов для полигонов ===")
    
    # Выпуклый полигон (квадрат)
    convex_polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
    
    # Невыпуклый полигон (форма звезды)
    nonconvex_polygon = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)]
    
    # Тест проверки выпуклости
    print(f"Квадрат выпуклый: {is_convex_polygon(convex_polygon)}")
    assert is_convex_polygon(convex_polygon) == True
    
    print(f"Звезда выпуклая: {is_convex_polygon(nonconvex_polygon)}") 
    assert is_convex_polygon(nonconvex_polygon) == False
    
    # Тест принадлежности точки выпуклому полигону
    print(f"Точка (0.5, 0.5) в квадрате: {point_in_convex_polygon((0.5, 0.5), convex_polygon)}")
    assert point_in_convex_polygon((0.5, 0.5), convex_polygon) == True
    
    print(f"Точка (2, 2) в квадрате: {point_in_convex_polygon((2, 2), convex_polygon)}")
    assert point_in_convex_polygon((2, 2), convex_polygon) == False
    
    # Тест принадлежности точки невыпуклому полигону
    print(f"Точка (1, 1) в звезде: {point_in_nonconvex_polygon((1, 1), nonconvex_polygon)}")
    assert point_in_nonconvex_polygon((1, 1), nonconvex_polygon) == True
    
    print(f"Точка (0.5, 0.5) в звезде: {point_in_nonconvex_polygon((0.5, 0.5), nonconvex_polygon)}")
    assert point_in_nonconvex_polygon((0.5, 0.5), nonconvex_polygon) == False
    
    # Тест универсальной функции
    print(f"Универсальная проверка (0.5,0.5) в квадрате: {point_in_polygon((0.5, 0.5), convex_polygon)}")
    assert point_in_polygon((0.5, 0.5), convex_polygon) == True
    
    print(f"Универсальная проверка (1,1) в звезде: {point_in_polygon((1, 1), nonconvex_polygon)}")
    assert point_in_polygon((1, 1), nonconvex_polygon) == True
    
    print(" Все тесты полигонов пройдены!\n")

if __name__ == "__main__":
    test_classify_point()
    test_find_intersection() 
    test_polygon_algorithms()
    print(" Все тесты успешно пройдены!")
    '''