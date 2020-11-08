import pygame
from pygame.locals import *
import time
import random
SIZE=40
BG_COLOR=(255,0,0)
class Apple:
    def __init__(self,screen):
        self.food=pygame.image.load('resources/food.png').convert_alpha()
        self.food=pygame.transform.scale(self.food,(40,40))
        self.screen=screen
        self.x=SIZE*random.randint(0,15)
        self.y=SIZE*random.randint(0,15)
    
    def draw(self):
        self.screen.blit(self.food,(self.x,self.y))
        pygame.display.flip()
    
    def move(self):
        self.x=SIZE*random.randint(0,15)
        self.y=SIZE*random.randint(0,15)
        self.draw()

class Snake:
    def __init__(self,screen,length):
        self.length=length
        self.screen=screen
        self.block=pygame.image.load('resources/snake.png').convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'

    def draw(self):
        self.screen.fill((255,0,0))
        for i in range(0,self.length):
            self.screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
        
    def increase_length(self):
        self.length+=1
        self.x.append(0)
        self.y.append(0)

    def move_down(self):
        self.direction='down'
    def move_up(self):
        self.direction='up'
    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        
        if(self.direction=='down'):
            self.y[0]=self.y[0]+SIZE
        if(self.direction=='up'):
            self.y[0]=self.y[0]-SIZE
        if(self.direction=='left'):
            self.x[0]=self.x[0]-SIZE
        if(self.direction=='right'):
            self.x[0]=self.x[0]+SIZE

        self.draw()

    
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake by Pratik')
        programIcon = pygame.image.load('resources/icon.png')
        pygame.display.set_icon(programIcon)
        pygame.mixer.init()
        #self.play_bg()
        self.surface=pygame.display.set_mode((680, 680))
        self.surface.fill((255,0,0))
        self.snake=Snake(self.surface,1)
        self.snake.draw() 
        self.food=Apple(self.surface)
        self.food.draw()


    def play_sound(self,sound):
        pygame.mixer.music.load(f'resources/{sound}.mp3')
        pygame.mixer.music.play()
    
    def play_bg(self):
        pygame.mixer.music.load('resources/bg.mp3')
        pygame.mixer.music.play()

    def play(self):
        self.snake.walk()
        self.food.draw()
        self.display_score()
        pygame.display.flip()
        
        if self.check_collision(self.snake.x[0],self.snake.y[0],self.food.x,self.food.y):
            self.play_sound('sound')
            self.snake.increase_length()
            self.food.move()

        if self.border_collision(self.snake.x[0],self.snake.y[0]):
            self.play_sound('gameover')
            raise 'Game Over'
        
        for i in range(3,self.snake.length):
            if self.check_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound('gameover')
                raise "Game Over"


    def check_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
            
        return False

    def border_collision(self,x,y):
        if(x<0 or x==680 or y<0 or y==680):
            return True
        return False
        
    def display_score(self):
        font=pygame.font.SysFont('arial',40)
        score=font.render(f'Score: {self.snake.length}',True,(255,255,255))
        self.surface.blit(score,(10,10))

    def game_over(self):
        self.surface.fill(BG_COLOR)
        font=pygame.font.SysFont('arial',30)
        message=font.render(f'Gameover, Your score is: {self.snake.length}',True,(255,255,255))
        self.surface.blit(message,(100,100))
        message=font.render('Press Enter to play again',True,(255,255,255))
        self.surface.blit(message,(100,200))
        pygame.display.flip()
    

    def reset(self):
        self.snake=Snake(self.surface,1)
        self.food=Apple(self.surface)

    def run(self):
        running=True
        stop=False
        while running:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_RETURN:
                        stop=False
                    if event.key == K_ESCAPE:
                        running=False
                    if not stop:
                        if event.key==K_RIGHT:
                            self.snake.move_right()
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_DOWN:
                            self.snake.move_down()
                        if event.key==K_LEFT:
                            self.snake.move_left()
                elif event.type==QUIT:
                    running=False
            try:
                if not stop:
                    self.play()
            except Exception as e:
                self.game_over()
                self.reset()
                stop=True
            time.sleep(0.05)
        
if __name__=='__main__':
    game=Game()
    game.run()