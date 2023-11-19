from settings import *

class Main:
    def __init__(self):
        
        # general things to do
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.FULLSCREEN)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_surface.fill('gray')
            pygame.display.update()


if __name__ == '__main__': # we will only run this script
    main = Main()
    main.run()
