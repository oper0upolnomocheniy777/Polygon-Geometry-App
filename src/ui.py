import pygame

class UserInterface:
    def __init__(self, screen, polygon_manager, transform_manager):
        self.screen = screen
        self.polygon_manager = polygon_manager
        self.transform_manager = transform_manager
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Состояние интерфейса
        self.mode = "draw"  # draw, select, transform
        self.message = "Левый клик: добавить точку | Правый клик: завершить полигон | Колесо: выбрать"
        
        # Элементы управления преобразованиями
        self.input_boxes = {}
        self.create_transform_ui()
        self.active_input_box = None
    
    def create_transform_ui(self):
        """Создает элементы UI для преобразований"""
        # Поля ввода для параметров - расположены вертикально с метками слева
        start_x = 400
        start_y = 40  # Оставляем место для заголовка
        input_width = 60
        input_height = 25
        vertical_spacing = 30
        label_width = 100  # Ширина для меток
        
        # Сначала создаем метки, потом поля ввода
        self.input_boxes = {
            'dx': pygame.Rect(start_x + label_width, start_y, input_width, input_height),
            'dy': pygame.Rect(start_x + label_width + 70, start_y, input_width, input_height),
            'angle': pygame.Rect(start_x + label_width, start_y + vertical_spacing, input_width, input_height),
            'center_x': pygame.Rect(start_x + label_width, start_y + vertical_spacing * 2, input_width, input_height),
            'center_y': pygame.Rect(start_x + label_width + 70, start_y + vertical_spacing * 2, input_width, input_height),
            'scale_x': pygame.Rect(start_x + label_width, start_y + vertical_spacing * 3, input_width, input_height),
            'scale_y': pygame.Rect(start_x + label_width + 70, start_y + vertical_spacing * 3, input_width, input_height)
        }
        
        self.input_values = {
            'dx': '10', 'dy': '10', 'angle': '45',
            'center_x': '100', 'center_y': '100',
            'scale_x': '1.5', 'scale_y': '1.5'
        }
        
        # Позиции для меток (левая колонка)
        self.label_positions = {
            'translate_label': (start_x, start_y + 5),
            'angle_label': (start_x, start_y + vertical_spacing + 5),
            'center_label': (start_x, start_y + vertical_spacing * 2 + 5),
            'scale_label': (start_x, start_y + vertical_spacing * 3 + 5)
        }
        
        # Кнопки преобразований - расположены вертикально справа
        button_width = 200
        button_height = 25
        button_start_x = start_x + label_width + 150
        button_start_y = start_y
        
        self.buttons = {
            'translate': pygame.Rect(button_start_x, button_start_y, button_width, button_height),
            'rotate_point': pygame.Rect(button_start_x, button_start_y + vertical_spacing, button_width, button_height),
            'rotate_center': pygame.Rect(button_start_x, button_start_y + vertical_spacing * 2, button_width, button_height),
            'scale_point': pygame.Rect(button_start_x, button_start_y + vertical_spacing * 3, button_width, button_height),
            'scale_center': pygame.Rect(button_start_x, button_start_y + vertical_spacing * 4, button_width, button_height)
        }
    
    def handle_event(self, event):
        """Обрабатывает события мыши и клавиатуры"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Проверка кликов по полям ввода
            self.active_input_box = None
            for name, rect in self.input_boxes.items():
                if rect.collidepoint(pos):
                    self.active_input_box = name
                    break
            
            # Проверка кликов по кнопкам
            if self.buttons['translate'].collidepoint(pos):
                self.apply_translation()
            elif self.buttons['rotate_point'].collidepoint(pos):
                self.apply_rotation_around_point()
            elif self.buttons['rotate_center'].collidepoint(pos):
                self.apply_rotation_around_center()
            elif self.buttons['scale_point'].collidepoint(pos):
                self.apply_scaling_around_point()
            elif self.buttons['scale_center'].collidepoint(pos):
                self.apply_scaling_around_center()
            
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
            elif event.key == pygame.K_t:  # Переключение в режим преобразований
                self.mode = "transform"
                self.message = "Режим преобразований: используйте панель управления"
            
            # Обработка ввода в активное поле
            if self.active_input_box and event.key != pygame.K_TAB:
                if event.key == pygame.K_BACKSPACE:
                    self.input_values[self.active_input_box] = self.input_values[self.active_input_box][:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.active_input_box = None
                else:
                    # Разрешаем только цифры, точку и минус
                    char = event.unicode
                    if char in '0123456789.-':
                        self.input_values[self.active_input_box] += char
    
    def apply_translation(self):
        """Применяет смещение"""
        try:
            dx = float(self.input_values['dx'])
            dy = float(self.input_values['dy'])
            if self.transform_manager.translate_selected(dx, dy):
                self.message = f"Смещение применено: dx={dx}, dy={dy}"
            else:
                self.message = "Ошибка: нет выбранного полигона"
        except ValueError:
            self.message = "Ошибка: неверные значения dx, dy"
    
    def apply_rotation_around_point(self):
        """Поворачивает вокруг заданной точки"""
        try:
            angle = float(self.input_values['angle'])
            cx = float(self.input_values['center_x'])
            cy = float(self.input_values['center_y'])
            if self.transform_manager.rotate_around_point(angle, (cx, cy)):
                self.message = f"Поворот вокруг точки ({cx}, {cy}) на {angle}°"
            else:
                self.message = "Ошибка: нет выбранного полигона"
        except ValueError:
            self.message = "Ошибка: неверные значения угла или центра"
    
    def apply_rotation_around_center(self):
        """Поворачивает вокруг центра полигона"""
        try:
            angle = float(self.input_values['angle'])
            if self.transform_manager.rotate_around_center(angle):
                self.message = f"Поворот вокруг центра на {angle}°"
            else:
                self.message = "Ошибка: нет выбранного полигона"
        except ValueError:
            self.message = "Ошибка: неверное значение угла"
    
    def apply_scaling_around_point(self):
        """Масштабирует относительно заданной точки"""
        try:
            sx = float(self.input_values['scale_x'])
            sy = float(self.input_values['scale_y'])
            cx = float(self.input_values['center_x'])
            cy = float(self.input_values['center_y'])
            if self.transform_manager.scale_around_point(sx, sy, (cx, cy)):
                self.message = f"Масштабирование относительно ({cx}, {cy}): sx={sx}, sy={sy}"
            else:
                self.message = "Ошибка: нет выбранного полигона"
        except ValueError:
            self.message = "Ошибка: неверные значения масштаба или центра"
    
    def apply_scaling_around_center(self):
        """Масштабирует относительно центра полигона"""
        try:
            sx = float(self.input_values['scale_x'])
            sy = float(self.input_values['scale_y'])
            if self.transform_manager.scale_around_center(sx, sy):
                self.message = f"Масштабирование относительно центра: sx={sx}, sy={sy}"
            else:
                self.message = "Ошибка: нет выбранного полигона"
        except ValueError:
            self.message = "Ошибка: неверные значения масштаба"
    
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
            "T - режим преобразований",
            "Левый клик - добавить точку",
            "Правый клик - завершить полигон",
            "Колесо - выбрать полигон"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, (100, 100, 100))
            self.screen.blit(control_surface, (10, 40 + i * 20))
        
        # Отрисовываем текущий режим
        mode_text = f"Режим: {self.mode.upper()}"
        mode_color = {
            "draw": (0, 100, 0),
            "select": (0, 0, 100),
            "transform": (100, 0, 0)
        }.get(self.mode, (0, 0, 0))
        
        mode_surface = self.font.render(mode_text, True, mode_color)
        self.screen.blit(mode_surface, (10, 750))
        
        # Статистика полигонов
        completed = sum(1 for p in self.polygon_manager.polygons if p.completed)
        total = len(self.polygon_manager.polygons)
        stats_text = f"Полигоны: {completed} завершено, {total} всего"
        stats_surface = self.small_font.render(stats_text, True, (0, 0, 0))
        self.screen.blit(stats_surface, (800, 10))
        
        # Отрисовываем панель преобразований
        self.draw_transform_panel()
    
    def draw_transform_panel(self):
        """Отрисовывает панель управления преобразованиями"""
        # Фон панели
        panel_rect = pygame.Rect(380, 5, 800, 200)
        pygame.draw.rect(self.screen, (240, 240, 240), panel_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2)
        
        # Заголовок
        title = self.small_font.render("Аффинные преобразования", True, (0, 0, 0))
        self.screen.blit(title, (400, 10))
        
        # Отрисовываем метки (левая колонка)
        labels = {
            'translate_label': 'Смещение:',
            'angle_label': 'Угол:',
            'center_label': 'Центр:',
            'scale_label': 'Масштаб:'
        }
        
        for name, pos in self.label_positions.items():
            label = self.small_font.render(labels[name], True, (0, 0, 0))
            self.screen.blit(label, pos)
        
        # Дополнительные метки для полей ввода
        additional_labels = {
            'dx': 'X:', 'dy': 'Y:',
            'center_x': 'X:', 'center_y': 'Y:',
            'scale_x': 'X:', 'scale_y': 'Y:'
        }
        
        additional_positions = {
            'dx': (self.input_boxes['dx'].x - 15, self.input_boxes['dx'].y + 5),
            'dy': (self.input_boxes['dy'].x - 15, self.input_boxes['dy'].y + 5),
            'center_x': (self.input_boxes['center_x'].x - 15, self.input_boxes['center_x'].y + 5),
            'center_y': (self.input_boxes['center_y'].x - 15, self.input_boxes['center_y'].y + 5),
            'scale_x': (self.input_boxes['scale_x'].x - 15, self.input_boxes['scale_x'].y + 5),
            'scale_y': (self.input_boxes['scale_y'].x - 15, self.input_boxes['scale_y'].y + 5)
        }
        
        for name, pos in additional_positions.items():
            label = self.small_font.render(additional_labels[name], True, (0, 0, 0))
            self.screen.blit(label, pos)
        
        # Отрисовываем поля ввода
        for name, rect in self.input_boxes.items():
            # Поле ввода
            color = (255, 255, 255) if self.active_input_box != name else (200, 255, 200)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
            
            # Текст
            text_surface = self.small_font.render(self.input_values[name], True, (0, 0, 0))
            self.screen.blit(text_surface, (rect.x + 5, rect.y + 5))
        
        # Отрисовываем кнопки
        button_labels = {
            'translate': 'Смещение',
            'rotate_point': 'Поворот вокруг точки',
            'rotate_center': 'Поворот вокруг центра', 
            'scale_point': 'Масштаб относительно точки',
            'scale_center': 'Масштаб относительно центра'
        }
        
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 255), rect)
            pygame.draw.rect(self.screen, (0, 0, 100), rect, 2)
            
            label = self.small_font.render(button_labels[name], True, (0, 0, 100))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)