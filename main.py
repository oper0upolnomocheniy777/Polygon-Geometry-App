import pygame
import sys
from src.ui import UserInterface
from src.polygon import PolygonManager
from src.transformations import TransformManager
# ИМПОРТИРУЕМ ВАШИ АЛГОРИТМЫ
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
    
    # ПЕРЕМЕННЫЕ ДЛЯ ВИЗУАЛИЗАЦИИ РЕЗУЛЬТАТОВ
    test_point = None
    point_result = ""
    polygon_type_info = ""
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)
            
            # ДОБАВЛЯЕМ ПРОВЕРКУ ВАШИХ АЛГОРИТМОВ ПРАВОЙ КНОПКОЙ МЫШИ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Правая кнопка мыши
                test_point = event.pos
                print(f"🧪 Тестируем точку: {test_point}")
                
                # ПРОВЕРЯЕМ ПРИНАДЛЕЖНОСТЬ ТОЧКИ ПОЛИГОНУ (ваш алгоритм)
                if polygon_manager.polygons:
                    current_polygon = polygon_manager.polygons[-1]
                    
                    # ПРОВЕРЯЕМ РАЗНЫЕ ВАРИАНТЫ АТРИБУТОВ
                    vertices = None
                    
                    if hasattr(current_polygon, 'vertices'):
                        vertices = current_polygon.vertices
                    elif hasattr(current_polygon, 'points'):
                        vertices = current_polygon.points
                    elif hasattr(current_polygon, 'nodes'):
                        vertices = current_polygon.nodes
                    elif isinstance(current_polygon, list):
                        vertices = current_polygon
                    
                    if vertices and len(vertices) >= 3:
                        # ДЕБАГ: выводим вершины для проверки
                        print(f"🔍 Вершины полигона: {vertices}")
                        
                        is_inside = point_in_polygon(test_point, vertices)
                        point_result = f"Точка {test_point}: {'ВНУТРИ' if is_inside else 'СНАРУЖИ'} полигона"
                        print(f"📊 {point_result}")
                        
                        # ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА ДЛЯ ВЫПУКЛОГО ПОЛИГОНА
                        if is_convex_polygon(vertices):
                            print("🔷 Полигон выпуклый, проверяем алгоритм...")
                            # Проверяем классификацию для каждого ребра
                            for i in range(len(vertices)):
                                edge_start = vertices[i]
                                edge_end = vertices[(i + 1) % len(vertices)]
                                classification = classify_point(edge_start, edge_end, test_point)
                                print(f"   Ребро {i}: {edge_start}-{edge_end}, точка: {classification}")
                    else:
                        print("⚠️  Недостаточно вершин для проверки полигона")
        
        # ОСНОВНАЯ ОТРИСОВКА
        screen.fill((255, 255, 255))  # Белый фон
        
        # Отрисовываем основной интерфес (от других участников)
        ui.draw()
        
        # ОПРЕДЕЛЯЕМ ТИП ПОЛИГОНА (ваш алгоритм)
        polygon_type_info = ""
        if polygon_manager.polygons:
            current_polygon = polygon_manager.polygons[-1]
            
            # ПРОВЕРЯЕМ РАЗНЫЕ ВАРИАНТЫ АТРИБУТОВ
            vertices = None
            
            if hasattr(current_polygon, 'vertices'):
                vertices = current_polygon.vertices
            elif hasattr(current_polygon, 'points'):
                vertices = current_polygon.points
            elif hasattr(current_polygon, 'nodes'):
                vertices = current_polygon.nodes
            elif isinstance(current_polygon, list):
                vertices = current_polygon
            
            if vertices and len(vertices) >= 3:
                is_convex = is_convex_polygon(vertices)
                polygon_type_info = f"Полигон: {'ВЫПУКЛЫЙ' if is_convex else 'НЕВЫПУКЛЫЙ'} ({len(vertices)} вершин)"
                print(f"📐 {polygon_type_info}")
        
        # ВИЗУАЛИЗИРУЕМ РЕЗУЛЬТАТЫ ВАШИХ АЛГОРИТМОВ (В ЛЕВОМ НИЖНЕМ УГЛУ)
        font = pygame.font.Font(None, 32)
        
        # Координаты для левого нижнего угла
        text_y = screen.get_height() - 100  # Отступ от низа
        
        # Показываем тип полигона
        if polygon_type_info:
            type_surface = font.render(polygon_type_info, True, (0, 100, 0))  # Темно-зеленый
            screen.blit(type_surface, (10, text_y))
        
        # Показываем тестовую точку и результат
        if test_point:
            # Рисуем красную точку
            pygame.draw.circle(screen, (255, 0, 0), test_point, 6)
            
            # Показываем текст результата под типом полигона
            if point_result:
                result_surface = font.render(point_result, True, (0, 0, 255))  # Синий
                screen.blit(result_surface, (10, text_y + 35))
        
        # ОБНОВЛЯЕМ ЭКРАН
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()