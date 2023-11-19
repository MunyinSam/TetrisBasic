from settings import *
from pygame.image import load
from os import path

class Preview:
    def __init__(self, get_next_shapes):

        #general
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        #put the rect above surface
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING)) 
        self.display_surface = pygame.display.get_surface() 
        self.display_surface.blit(self.surface, self.rect)

        #shapes
        self.next_shapes = get_next_shapes
        # get the img
        # self.shape_surfaces = {shape: load('assets/graphics/T.png') for shape in TETROMINOS.keys()}
        self.shape_surfaces = {shape: load(path.join('assets','graphics'
                            ,f'{shape}.png')).convert_alpha() for shape in TETROMINOS.keys()}
        print(self.shape_surfaces)

    def run(self):
        self.display_surface.blit(self.surface,self.rect)