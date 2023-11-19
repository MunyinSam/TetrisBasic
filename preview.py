from settings import *
from pygame.image import load
from os import path

class Preview:
    def __init__(self):

        #general
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        #put the rect above surface
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING)) 
        self.display_surface = pygame.display.get_surface() 
        self.display_surface.blit(self.surface, self.rect)

        #shapes
        #self.next_shapes = next_shapes
        # get the img
        # self.shape_surfaces = {shape: load('assets/graphics/T.png') for shape in TETROMINOS.keys()}
        self.shape_surfaces = {shape: load(path.join('assets/graphics'
                            ,f'{shape}.png')).convert_alpha() for shape in TETROMINOS.keys()}
        

        #img position data
        self.fracment_height = self.surface.get_height() / 3



    def display_pieces(self, shapes):
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() / 2
            y = self.fracment_height / 2 + i * self.fracment_height
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface, rect)

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface,self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)