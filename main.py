from settings import *
from sys import exit
#components

from game import Game
from score import Score
from preview import Preview


class Main:
    def __init__(self):
        
        # general things to do
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        self.game = Game()
        self.score = Score()
        self.preview = Preview()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_surface.fill(GRAY)

            self.game.run()
            self.score.run()
            self.preview.run()

            pygame.display.update()
            self.clock.tick() #fps


if __name__ == '__main__': # we will only run this script
    main = Main()
    main.run()
