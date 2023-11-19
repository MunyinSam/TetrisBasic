from settings import *
from os.path import join

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        #put the rect above surface
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING,WINDOW_HEIGHT - PADDING)) 
        self.display_surface = pygame.display.get_surface() 

        # font
        self.font = pygame.font.Font( join('assets/graphics','Russo_One.ttf'), 30)

    def run(self):
        self.display_surface.blit(self.surface,self.rect)