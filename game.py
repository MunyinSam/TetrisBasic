from settings import *
from random import choice

from timer import Timer

class Game:

    def __init__(self, get_next_shape):

        #general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface() 
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connection
        self.get_next_shape = get_next_shape


        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120) # transparency

        #tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
                    choice(list(TETROMINOS.keys())),
                    self.sprites,
                    self.create_new_tetromino,
                    self.field_data)

        #timer
        self.timers = {
            'vertical move' : Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move' : Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }

        self.timers['vertical move'].activate()

    def create_new_tetromino(self):

        self.check_finished_rows()
        self.tetromino = Tetromino(
                    self.get_next_shape(),
                    self.sprites,
                    self.create_new_tetromino,
                    self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
        
    def move_down(self):
        self.tetromino.move_down()    

    def draw_grid(self):

        for col in range(1, COLUMNS):
            #surface, color, startpos, end pos , width
            x = col * CELL_SIZE #how wide
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):

            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y) , (self.surface.get_width(),y) , 1)

        self.surface.blit(self.line_surface, (0,0))

    def input(self):

        keys = pygame.key.get_pressed()


    # checking horizontal movement
        if not self.timers['horizontal move'].active:

            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

    # check a rotation
        # so we need to wait out the timer to run it cant spam

        if not self.timers['rotate'].active:
            
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

    def check_finished_rows(self):

        # get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data): #enumerate gets the indexes
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:

                #del full row
                for block in self.field_data[delete_row]:
                    block.kill() # will delete rows but not field data

                #move down the blocks
                for row in self.field_data:
                    for block in row: #pulling down the block(only in visible)
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

                #rebuild the field data
                #clean the field
                self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
                for block in self.sprites:
                    self.field_data[int(block.pos.y)][int(block.pos.x)] = block

    def run(self):
        
        #update
        self.input()
        self.timer_update()
        self.sprites.update() #takes all the sprite

        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        # display , color , rect, width, corner radius
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):

        #setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape'] #indexing dict.
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        #create blocks 
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    #collisions we gonna vreate an imaginary shape and check if it collides with the outside
    def next_move_horizontal_collide(self, blocks, amount):
        #collision list will check every block 
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    
    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount): #if this is false u can move
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1): #if this is false u can move
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block #[row][col]
            self.create_new_tetromino()

            #for row in self.field_data:
                #print(row)
    
    def rotate(self):
        if self.shape != 'O':

            # 1 need pivot point
            pivot_pos = self.blocks[0].pos # the 0,0 one

            # 2 New block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # 3 Collision check
            for pos in new_block_positions:

                #horizontal
                if pos.x < 0 or pos.x >= COLUMNS:
                    return #it would end and wont continue (cant rotate)

                #field check / collision with other pieces

                if self.field_data[int(pos.y)][int(pos.x)]: # true
                    return

                # vertical / floor check

                if pos.y > ROWS:
                    return

            # 4 Impliment new pos
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
        
class Block(pygame.sprite.Sprite):

  
    def __init__(self, group, pos, color):

        #general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)

        #position

        #store pos as attribute
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft = (x,y))

    def rotate(self, pivot_pos):
        '''
        distance = self.pos - pivot_pos
        rotated = distance.rotate(90)
        new_pos = pivot_pos + rotated
        return new_pos
        '''
        return pivot_pos + (self.pos - pivot_pos).rotate(90)
        

    def horizontal_collide(self, x, field_data):
        if not 0 <=  x < COLUMNS:
            return True

        if field_data[int(self.pos.y)][x]: #[row][col] #check if theres a piece here
            return True
        
    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True

        if y>= 0 and field_data[y][int(self.pos.x)]: #[row][col]
            return True

        

    def update(self):
        '''
        #print(self.pos)
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.pos * 40
        # (1,3) *40 = (40,120)
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)
        '''
        self.rect.topleft = self.pos * CELL_SIZE