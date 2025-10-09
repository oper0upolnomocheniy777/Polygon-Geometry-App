import pygame

class Polygon:
    def __init__(self, points=None, color=(0, 0, 0)):
        self.points = points if points else []
        self.color = color
        self.completed = False
        self.is_selected = False
    
    def add_point(self, point):
        """Добавляет точку к полигону"""
        self.points.append(point)
    
    def complete(self):
        """Отмечает полигон как завершенный"""
        self.completed = True
    
    def draw(self, screen):
        """Отрисовывает полигон на экране"""
        if len(self.points) < 2:
            return
        
        # Рисуем линии между точками
        if self.completed and len(self.points) > 2:
            pygame.draw.polygon(screen, self.color, self.points, 2 if self.is_selected else 1)
        else:
            # Рисуем незавершенный полигон
            for i in range(len(self.points) - 1):
                pygame.draw.line(screen, self.color, self.points[i], self.points[i + 1], 2 if self.is_selected else 1)
        
        # Рисуем точки
        for point in self.points:
            pygame.draw.circle(screen, (255, 0, 0), point, 4)

class PolygonManager:
    def __init__(self):
        self.polygons = []
        self.current_polygon = None
    
    def start_new_polygon(self, start_point):
        """Начинает новый полигон"""
        self.current_polygon = Polygon()
        self.current_polygon.add_point(start_point)
        self.polygons.append(self.current_polygon)
    
    def add_point_to_current(self, point):
        """Добавляет точку к текущему полигону"""
        if self.current_polygon and not self.current_polygon.completed:
            self.current_polygon.add_point(point)
    
    def complete_current_polygon(self):
        """Завершает текущий полигон"""
        if self.current_polygon and len(self.current_polygon.points) >= 3:
            self.current_polygon.complete()
            self.current_polygon = None
    
    def clear_all(self):
        """Очищает все полигоны"""
        self.polygons = []
        self.current_polygon = None
    
    def select_polygon_at_point(self, point):
        """Выбирает полигон по точке клика"""
        for polygon in self.polygons:
            polygon.is_selected = False
        
        # Простой выбор по попаданию в bounding box
        for polygon in reversed(self.polygons):  # Проверяем сверху вниз
            if polygon.completed and len(polygon.points) > 2:
                # Простая проверка - если точка рядом с любой вершиной
                for poly_point in polygon.points:
                    distance = ((point[0] - poly_point[0]) ** 2 + (point[1] - poly_point[1]) ** 2) ** 0.5
                    if distance < 10:  # 10 пикселей - радиус попадания
                        polygon.is_selected = True
                        return polygon
        return None
    
    def draw_all(self, screen):
        """Отрисовывает все полигоны"""
        for polygon in self.polygons:
            polygon.draw(screen)