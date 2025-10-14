def classify_point(edge_start, edge_end, point):
    """
    Классифицирует положение точки относительно ребра.
    
    Args:
        edge_start: tuple (x, y) - начальная точка ребра
        edge_end: tuple (x, y) - конечная точка ребра  
        point: tuple (x, y) - точка для классификации
    
    Returns:
        str: "left", "right" или "on"
    """
    # Вектор ребра
    edge_vector = (edge_end[0] - edge_start[0], edge_end[1] - edge_start[1])
    # Вектор от начала ребра к точке
    point_vector = (point[0] - edge_start[0], point[1] - edge_start[1])
    
    # Векторное произведение
    cross_product = (edge_vector[0] * point_vector[1] - 
                    edge_vector[1] * point_vector[0])
    
    # Определение положения
    if cross_product > 0:
        return "left"
    elif cross_product < 0:
        return "right"
    else:
        return "on"


def find_intersection(edge1, edge2):
    """
    Находит пересечение двух отрезков.
    
    Args:
        edge1: tuple ((x1, y1), (x2, y2)) - первый отрезок
        edge2: tuple ((x3, y3), (x4, y4)) - второй отрезок
    
    Returns:
        tuple (x, y) or None: точка пересечения или None если не пересекаются
    """
    (p1, p2), (p3, p4) = edge1, edge2
    
    # Параметры для уравнений отрезков
    A1 = p2[1] - p1[1]
    B1 = p1[0] - p2[0]
    C1 = A1 * p1[0] + B1 * p1[1]
    
    A2 = p4[1] - p3[1]
    B2 = p3[0] - p4[0]
    C2 = A2 * p3[0] + B2 * p3[1]
    
    # Определитель
    det = A1 * B2 - A2 * B1
    
    # Если отрезки параллельны
    if abs(det) < 1e-10:
        return None
    
    # Точка пересечения прямых
    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det
    
    # Проверка, что точка принадлежит обоим отрезкам
    if (min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]) and
        min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]) and
        min(p3[0], p4[0]) <= x <= max(p3[0], p4[0]) and
        min(p3[1], p4[1]) <= y <= max(p3[1], p4[1])):
        return (x, y)
    
    return None


def is_convex_polygon(polygon):
    """
    Проверяет, является ли полигон выпуклым.
    
    Args:
        polygon: list of tuples [(x1, y1), (x2, y2), ...]
    
    Returns:
        bool: True если выпуклый, False если нет
    """
    if len(polygon) < 3:
        return True
    
    # Проверяем знаки векторных произведений для всех последовательных ребер
    signs = []
    n = len(polygon)
    
    for i in range(n):
        edge_start = polygon[i]
        edge_end = polygon[(i + 1) % n]
        next_point = polygon[(i + 2) % n]
        
        classification = classify_point(edge_start, edge_end, next_point)
        
        if classification == "left":
            signs.append(1)
        elif classification == "right":
            signs.append(-1)
        # Если точка на прямой - игнорируем
    
    # Если все знаки одинаковые (или есть только один знак) - полигон выпуклый
    unique_signs = set(signs)
    return len(unique_signs) <= 1


def point_in_convex_polygon(point, polygon):
    """
    Проверяет принадлежность точки выпуклому полигону.
    Исправленная версия - проверяет одинаковость знаков для всех ребер.
    """
    if len(polygon) < 3:
        return False
    
    n = len(polygon)
    signs = []
    
    for i in range(n):
        edge_start = polygon[i]
        edge_end = polygon[(i + 1) % n]
        
        classification = classify_point(edge_start, edge_end, point)
        
        # Определяем знак для текущего ребра
        if classification == "left":
            signs.append(1)
        elif classification == "right":
            signs.append(-1)
        elif classification == "on":
            signs.append(0)
    
    # Отладочный вывод
    print(f"🔍 Знаки для точки {point}: {signs}")
    
    # Если есть точки на границе - считаем внутри
    if 0 in signs:
        return True
    
    # Проверяем что все ненулевые знаки одинаковы
    non_zero_signs = [s for s in signs if s != 0]
    if not non_zero_signs:  # Все точки на границе
        return True
    
    # Все ненулевые знаки должны быть одинаковы
    first_sign = non_zero_signs[0]
    return all(sign == first_sign for sign in non_zero_signs)


def point_in_nonconvex_polygon(point, polygon):
    """
    Проверяет принадлежность точки невыпуклому полигону с помощью Ray Casting.
    
    Args:
        point: tuple (x, y) - проверяемая точка
        polygon: list of tuples - вершины полигона
    
    Returns:
        bool: True если точка внутри полигона
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # Проверяем пересечение луча с ребром
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    
    return inside


def point_in_polygon(point, polygon):
    """
    Универсальная функция проверки принадлежности точки полигону.
    Автоматически определяет тип полигона и выбирает алгоритм.
    
    Args:
        point: tuple (x, y) - проверяемая точка
        polygon: list of tuples - вершины полигона
    
    Returns:
        bool: True если точка внутри полигона
    """
    if is_convex_polygon(polygon):
        return point_in_convex_polygon(point, polygon)
    else:
        return point_in_nonconvex_polygon(point, polygon)