import pygame
import sys
from src.ui import UserInterface
from src.polygon import PolygonManager
from src.transformations import TransformManager
from src.algorithms import (
    classify_point, 
    find_intersection, 
    is_convex_polygon,
    point_in_polygon
)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Polygon Geometry Application")
    clock = pygame.time.Clock()
    
    polygon_manager = PolygonManager()
    transform_manager = TransformManager(polygon_manager)
    ui = UserInterface(screen, polygon_manager, transform_manager)
    
    demo_edges = []  # Ребра для демонстрации пересечений
    demo_current_edge = None  # Текущее создаваемое ребро
    demo_intersections = []  # Точки пересечений
    demo_test_point = None  # Точка для тестирования
    demo_results = []  # Результаты проверок
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)  # Оригинальный обработчик
            
            if event.type == pygame.KEYDOWN:
                # F1 - создать тестовое ребро
                if event.key == pygame.K_F1:
                    if demo_current_edge is None:
                        demo_current_edge = pygame.mouse.get_pos()
                
                # F2 - тестировать точку
                elif event.key == pygame.K_F2:
                    demo_test_point = pygame.mouse.get_pos()
                    demo_results = []
                    
                    # Проверка точки в полигонах
                    if polygon_manager.polygons:
                        for i, polygon in enumerate(polygon_manager.polygons):
                            vertices = get_polygon_vertices(polygon)
                            if vertices and len(vertices) >= 3:
                                is_inside = point_in_polygon(demo_test_point, vertices)
                                poly_type = "выпуклый" if is_convex_polygon(vertices) else "невыпуклый"
                                demo_results.append(f"Полигон {i+1} ({poly_type}): {'ВНУТРИ' if is_inside else 'СНАРУЖИ'}")
                    
                    # Классификация относительно ребер
                    if demo_edges:
                        for i, edge in enumerate(demo_edges):
                            classification = classify_point(edge[0], edge[1], demo_test_point)
                            demo_results.append(f"Ребро {i+1}: {classification}")
                
                # F3 - очистить демо-данные
                elif event.key == pygame.K_F3:
                    demo_edges.clear()
                    demo_intersections.clear()
                    demo_current_edge = None
                    demo_test_point = None
                    demo_results = []
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Shift + ЛКМ - создать ребро
                if event.button == 1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if demo_current_edge is None:
                        demo_current_edge = event.pos
                    else:
                        new_edge = (demo_current_edge, event.pos)
                        demo_edges.append(new_edge)
                        # Поиск пересечений
                        update_intersections(demo_edges, demo_intersections)
                        demo_current_edge = None
        
        # ОСНОВНАЯ ОТРИСОВКА
        screen.fill((255, 255, 255))
        ui.draw()  # Оригинальная отрисовка
        
        # ДОПОЛНИТЕЛЬНАЯ ОТРИСОВКА ДЛЯ ДЕМОНСТРАЦИИ
        # 1. Рисуем ребра
        for edge in demo_edges:
            pygame.draw.line(screen, (0, 0, 255), edge[0], edge[1], 2)
        
        # 2. Рисуем точки пересечения
        for intersection in demo_intersections:
            pygame.draw.circle(screen, (255, 0, 0), (int(intersection[0]), int(intersection[1])), 6)
        
        # 3. Рисуем текущее создаваемое ребро
        mouse_pos = pygame.mouse.get_pos()
        if demo_current_edge:
            pygame.draw.line(screen, (0, 255, 0), demo_current_edge, mouse_pos, 2)
        
        # 4. Рисуем тестовую точку
        if demo_test_point:
            pygame.draw.circle(screen, (255, 0, 0), demo_test_point, 6)
        
        # 5. Отображаем информацию
        draw_demo_info(screen, polygon_manager.polygons, demo_edges, demo_intersections, demo_results)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def get_polygon_vertices(polygon):
    """Получает вершины полигона"""
    if hasattr(polygon, 'vertices'):
        return polygon.vertices
    elif hasattr(polygon, 'points'):
        return polygon.points
    elif hasattr(polygon, 'nodes'):
        return polygon.nodes
    elif isinstance(polygon, list):
        return polygon
    return None

def update_intersections(edges, intersections):
    """Обновляет точки пересечений"""
    intersections.clear()
    for i, edge1 in enumerate(edges):
        for j, edge2 in enumerate(edges[i+1:], i+1):
            intersection = find_intersection(edge1, edge2)
            if intersection:
                intersections.append(intersection)

def draw_demo_info(screen, polygons, edges, intersections, results):
    """Отображает информацию о демонстрации"""
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 20)
    
    # Информация в правом верхнем углу
    x = screen.get_width() - 300
    y = 10
    
    # Управление
    controls = [
        "ДЛЯ АЛГОРИТМОВ:",
        "Shift+ЛКМ - создать ребро",
        "F2 - тест точки под курсором",
        "F3 - очистить демо",
    ]
    
    for i, text in enumerate(controls):
        color = (100, 0, 100) if i == 0 else (80, 80, 80)
        surface = small_font.render(text, True, color)
        screen.blit(surface, (x, y + i * 20))
    
    y += len(controls) * 20 + 10
    
    # Статистика
    stats = [
        f"Полигонов: {len(polygons)}",
        f"Ребер: {len(edges)}",
        f"Пересечений: {len(intersections)}"
    ]
    
    for i, text in enumerate(stats):
        surface = small_font.render(text, True, (0, 100, 0))
        screen.blit(surface, (x, y + i * 20))
    
    y += len(stats) * 20 + 10
    
    # Результаты тестирования
    if results:
        for i, result in enumerate(results):
            surface = small_font.render(result, True, (0, 0, 200))
            screen.blit(surface, (x, y + i * 18))

if __name__ == "__main__":
    main()