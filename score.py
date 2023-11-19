from settings import *

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.display_surface = pygame.display.get_surface() 

    def run(self):
        self.display_surface.blit(self.surface,(0, 0))