import pygame
import sys
from src.ui import UserInterface
from src.polygon import PolygonManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Polygon Geometry Application")
    clock = pygame.time.Clock()
    
    polygon_manager = PolygonManager()
    ui = UserInterface(screen, polygon_manager)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)
        
        screen.fill((255, 255, 255))  # Белый фон
        ui.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()