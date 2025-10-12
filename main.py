import pygame
import sys
from src.ui import UserInterface
from src.polygon import PolygonManager
from src.transformations import TransformManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Polygon Geometry Application")
    clock = pygame.time.Clock()
    
    polygon_manager = PolygonManager()
    transform_manager = TransformManager(polygon_manager)
    ui = UserInterface(screen, polygon_manager, transform_manager)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)
        
        screen.fill((255, 255, 255))  # White background
        ui.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()