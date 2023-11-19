from settings import *
from sys import exit
#components

# self = attributes

from game import Game
from score import Score
from preview import Preview
from random import choice

class Main:
    def __init__(self):
        
        # general things to do
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        #shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]
        print(self.next_shapes)

        self.game = Game(self.get_next_shape)
        self.score = Score()
        self.preview = Preview()

    
    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0) #pop = pick and remove
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_surface.fill(GRAY)

            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            pygame.display.update()
            self.clock.tick() #fps


if __name__ == '__main__': # we will only run this script
    main = Main()
    main.run()
