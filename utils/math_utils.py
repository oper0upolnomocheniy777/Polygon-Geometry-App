def distance(p1, p2):
    """Вычисляет расстояние между двумя точками."""
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5

def dot_product(v1, v2):
    """Скалярное произведение двух векторов."""
    return v1[0] * v2[0] + v1[1] * v2[1]

def cross_product(v1, v2):
    """Векторное произведение двух векторов."""
    return v1[0] * v2[1] - v1[1] * v2[0]

def normalize_vector(v):
    """Нормализует вектор."""
    length = (v[0]**2 + v[1]**2)**0.5
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)