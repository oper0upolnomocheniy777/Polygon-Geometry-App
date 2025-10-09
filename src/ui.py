import pygame

class UserInterface:
    def __init__(self, screen, polygon_manager):
        self.screen = screen
        self.polygon_manager = polygon_manager
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Состояние интерфейса
        self.mode = "draw"  # draw, select
        self.message = "Левый клик: добавить точку | Правый клик: завершить полигон | Колесо: выбрать"
    
    def handle_event(self, event):
        """Обрабатывает события мыши и клавиатуры"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if event.button == 1:  # Левый клик
                if self.mode == "draw":
                    if not self.polygon_manager.current_polygon:
                        self.polygon_manager.start_new_polygon(pos)
                    else:
                        self.polygon_manager.add_point_to_current(pos)
                
            elif event.button == 3:  # Правый клик
                if self.mode == "draw" and self.polygon_manager.current_polygon:
                    self.polygon_manager.complete_current_polygon()
                
            elif event.button == 2:  # Колесо мыши
                self.mode = "select"
                selected = self.polygon_manager.select_polygon_at_point(pos)
                if selected:
                    self.message = f"Полигон выбран ({len(selected.points)} вершин)"
                else:
                    self.message = "Полигон не найден"
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Очистка по клавише C
                self.polygon_manager.clear_all()
                self.message = "Сцена очищена"
                self.mode = "draw"
            elif event.key == pygame.K_d:  # Переключение в режим рисования
                self.mode = "draw"
                self.message = "Режим рисования: левый клик - точки, правый - завершить"
            elif event.key == pygame.K_s:  # Переключение в режим выбора
                self.mode = "select"
                self.message = "Режим выбора: клик колесом по полигону"
    
    def draw(self):
        """Отрисовывает интерфейс"""
        # Отрисовываем полигоны
        self.polygon_manager.draw_all(self.screen)
        
        # Отрисовываем информационное сообщение
        message_surface = self.small_font.render(self.message, True, (0, 0, 0))
        self.screen.blit(message_surface, (10, 10))
        
        # Отрисовываем подсказки по управлению
        controls = [
            "C - очистить сцену",
            "D - режим рисования", 
            "S - режим выбора",
            "Левый клик - добавить точку",
            "Правый клик - завершить полигон",
            "Колесо - выбрать полигон"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, (100, 100, 100))
            self.screen.blit(control_surface, (10, 40 + i * 20))
        
        # Отрисовываем текущий режим
        mode_text = f"Режим: {self.mode.upper()}"
        mode_surface = self.font.render(mode_text, True, (0, 100, 0) if self.mode == "draw" else (0, 0, 100))
        self.screen.blit(mode_surface, (10, 750))
        
        # Статистика полигонов
        completed = sum(1 for p in self.polygon_manager.polygons if p.completed)
        total = len(self.polygon_manager.polygons)
        stats_text = f"Полигоны: {completed} завершено, {total} всего"
        stats_surface = self.small_font.render(stats_text, True, (0, 0, 0))
        self.screen.blit(stats_surface, (800, 10))