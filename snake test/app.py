import pygame, time, random
from pygame.locals import *

# COLORS
BLACK = '#000000'
WHITE = '#FFFFFF'
GREY = '#808080'
DARK_GREY = '#404040'
RED = '#DFA995'
GREEN = '#44D362'

# DIMENSIONS
ROWS = 20
COLS = 20
GRIDSIZE = 30
WIDTH = COLS * GRIDSIZE
HEIGHT = ROWS * GRIDSIZE + GRIDSIZE

class Snake:

    def __init__(self, screen, length):

        self.parent_screen = screen        
        self.length = length

        self.block = pygame.image.load('block.png').convert()
        self.blank = pygame.image.load('blank.png').convert()

        self.start_pos = 1
        self.posx = [self.start_pos] * self.length
        self.posy = [self.start_pos] * self.length

        self.dir = 'down'

    def draw(self):

        for i in range (self.length):

            self.parent_screen.blit(self.block, (self.posx[i], self.posy[i]))
            
            self.delete(-1)

        pygame.display.flip()

    
    def delete(self, i):

        self.parent_screen.blit(self.blank, (self.posx[i], self.posy[i]))

        pygame.display.flip()

    
    def inc_length(self):

        self.length += 1

        self.posx.append([-1])
        self.posy.append([-1])

        self.walk()
    

    def move_left(self):
        if self.dir != 'right':
            self.dir = 'left'

    def move_right(self):
        if self.dir != 'left':
            self.dir = 'right'

    def move_up(self):
        if self.dir != 'down':
            self.dir = 'up'

    def move_down(self):
        if self.dir != 'up':
            self.dir = 'down'


    def walk(self):
        
        for i in range(self.length-1, 0, -1):

            self.posx[i] = self.posx[i - 1]
            self.posy[i] = self.posy[i - 1]
            

        if self.dir == 'up':
            self.posy[0] -= 30

        if self.dir == 'down':
            self.posy[0] += 30

        if self.dir == 'right':
            self.posx[0] += 30

        if self.dir == 'left':
            self.posx[0] -= 30

        self.draw()

        pygame.display.flip()



class Apple:

    def __init__(self, screen):

        self.parent_screen = screen
        
        self.block = pygame.image.load('apple.png').convert()
        self.blank = pygame.image.load('blank.png').convert()

    
    def get_pos(self):

        x = random.randint(0,19)
        y = random.randint(0,19)

        self.posx = x * GRIDSIZE + 1
        self.posy = y * GRIDSIZE + 1


    
    def draw(self):
        
        self.get_pos()
        self.parent_screen.blit(self.block, (self.posx, self.posy))
        pygame.display.flip()

    
    def delete(self):

        self.parent_screen.blit(self.blank, (self.posx, self.posy))
        pygame.display.flip()

    def move(self):

        self.draw()



class Poison:
    
    def __init__(self, screen):

        self.parent_screen = screen

        self.posx = 0
        self.posy = 0
        
        self.block = pygame.image.load('poison.png').convert()
        self.blank = pygame.image.load('blank.png').convert()

    
    def get_pos(self):

        x = random.randint(0,19)
        y = random.randint(0,19)

        self.posx = x * GRIDSIZE + 1
        self.posy = y * GRIDSIZE + 1

    def show(self):

        num = random.randint(1, 5)

        if num == 5:
            return True

        return False

    
    def draw(self):

        if self.show() == True:
            
            self.delete()
            self.get_pos()
            self.parent_screen.blit(self.block, (self.posx, self.posy))

        else:
            self.delete()

        pygame.display.flip()

    def delete(self):

        self.parent_screen.blit(self.blank, (self.posx, self.posy))
        self.posx =-1
        self.posy =-1
        pygame.display.flip()



class Game:

    def __init__(self):

        pygame.init()

        self.score = 0
        self.delay = .3      
        
        self.display_window()


    def display_window(self):   

        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

    
    def display_grid(self):

        for r in range(ROWS+1):
            pygame.draw.line(self.screen, GREY, (0, r * GRIDSIZE), (COLS*GRIDSIZE, r * GRIDSIZE))

        for c in range(COLS):
            pygame.draw.line(self.screen, GREY, (c * GRIDSIZE, 0), (c * GRIDSIZE, ROWS*GRIDSIZE))

        pygame.display.flip()


    def display_score(self):

        pygame.draw.rect(self.screen, DARK_GREY, (0,600, WIDTH, GRIDSIZE))

        font = pygame.font.SysFont('arial', 20)
        score = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score, (500,600))
        pygame.display.flip()
    

    def display_gameover(self, reason):

        font = pygame.font.SysFont('arial', 50)
        font2 = pygame.font.SysFont('arial', 20)

        text = font.render("GAME OVER!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(text, text_rect)
        
        text2 = font2.render(reason, True, WHITE)
        text2_rect = text2.get_rect(center=(WIDTH/2, HEIGHT/2+30))
        self.screen.blit(text2, text2_rect)
        pygame.display.flip()
        

    def clear_screen(self):

        self.screen.fill(BLACK)
        pygame.display.flip()


    def eats_apple(self, x1, y1, x2, y2):

        if x1 == x2 and y1 == y2:
            return True

        return False

    
    def eats_body(self):

        x1, y1 = self.snake.posx[0], self.snake.posy[0]

        if self.snake.length > 3 :

            for i in range(3, self.snake.length):

                x2, y2 = self.snake.posx[i], self.snake.posy[i]

                if x1 == x2 and y1 == y2:
                    return True

        return False


    def eats_poison(self, x1, y1, x2, y2):
    
        if x1 == x2 and y1 == y2:
            return True

        return False


    def hits_border(self):

        x = self.snake.posx[0]
        y = self.snake.posy[0]

        if x<0 or x>600 or y<0 or y>600:
            return True

        return False

    
    def overlaps(self):

        applex, appley = self.apple.posx, self.apple.posy
        poisonx, poisony = self.poison.posx, self.poison.posy

        if applex == poisonx and appley == poisony:
            self.poison.draw()
            print('poison redrew')

        for i in range(self.snake.length-1):

            snakex, snakey = self.snake.posx[i], self.snake.posy[i]

            if snakex == applex and snakey == appley:
                self.apple.move()
                print('apple redrew')
            
            if snakex == poisonx and snakey == poisony:
                self.posion.draw()
                print('poison redrew')


    def game_over(self, reason):
    
        self.display_gameover(reason)
        time.sleep(1)
        self.running = False


    def play(self):
    
        self.snake.walk()

        if self.eats_body() == True:
            self.game_over('Suicidal much?')


        if self.hits_border() == True:
            self.game_over('You went out of the border.')
            
        if self.eats_poison(self.snake.posx[0], self.snake.posy[0], self.poison.posx, self.poison.posy):    
            self.game_over('You were poisoned.')

        
        if self.eats_apple(self.snake.posx[0], self.snake.posy[0], self.apple.posx, self.apple.posy):

            self.score += 1

            if self.delay > .2 :
                self.delay -= .0050

            elif self.delay > .1 :
                self.delay -= .0025

            elif self.delay > .05 :
                self.delay -= .00125

            self.snake.inc_length()
            self.apple.move()
            self.poison.draw()
            self.display_score()
            self.overlaps()

        time.sleep(self.delay)

        
    def run(self):

        self.clear_screen()
        self.display_grid()

        self.display_score()
        
        self.snake = Snake(self.screen, 2)  
        self.snake.draw()

        self.apple = Apple(self.screen)  
        self.apple.draw()

        self.poison = Poison(self.screen)
        self.poison.draw()

        self.running = True

        while self.running:

            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    # quit on ESC
                    if event.key == K_ESCAPE:
                        self.running = False

                    # move snake
                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()
                
                elif event.type == pygame.QUIT:
                    self.running = False
            
            self.play()

        

# main
if __name__ == '__main__':

    game = Game()
    game.run()