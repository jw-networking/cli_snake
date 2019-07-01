#!/bin/python3
import curses
import random
from time import sleep

class Snake():
    def __init__(self,head,length=2,orientation='L'):
        self.length=length
        self.body=[[head,orientation]]
        for i in range(length):
            self.add_Segment()


    def add_Segment(self):
        last_move=self.body[-1]
        if last_move[1] == 'L':
            self.body.append( [ (last_move[0][0],last_move[0][1]+1), last_move[1]] )
        elif last_move[1] == 'R':
            self.body.append( [ (last_move[0][0],last_move[0][1]-1), last_move[1]] )
        elif last_move[1] == 'U':
            self.body.append( [ (last_move[0][0]+1,last_move[0][1]), last_move[1]] )
        elif last_move[1] == 'D':
            self.body.append( [ (last_move[0][0]-1,last_move[0][1]), last_move[1]] )
        else:
            raise IndexError(str(last_move[1])+": invalid orientation U,D,L,R only")

    def forward(self,orientation=None):
        head=self.body[0]
        if orientation == None:
            orientation=head[1]
        self.body.pop()

        new_segment=None
        if orientation == 'L':
            new_segment= [ (head[0][0],head[0][1]-1), orientation]
            if new_segment[0]==self.body[1][0]:
                new_segment[0]=(head[0][0],head[0][1]+1)
        elif orientation == 'R':
            new_segment= [ (head[0][0],head[0][1]+1), orientation]
            if new_segment[0]==self.body[1][0]:
                new_segment[0]=(head[0][0],head[0][1]-1)
        elif orientation == 'U':
            new_segment= [ (head[0][0]-1,head[0][1]), orientation]
            if new_segment[0]==self.body[1][0]:
                new_segment[0]=(head[0][0]+1,head[0][1])
        elif orientation == 'D':
            new_segment= [ (head[0][0]+1,head[0][1]), orientation]
            if new_segment[0]==self.body[1][0]:
                new_segment[0]=(head[0][0]-1,head[0][1])
        else:
            raise IndexError(str(orientation)+": invalid orientation U,D,L,R only")

        self.body.insert(0,new_segment)

        


        

class Board():
    def __init__(self,size):
        random.seed()
        self.size=size
        self.snake=Snake((int(size[0]/2),int(size[1]/2)))
        self.food=set()
        self.add_food()
        self.state="play"
        self.score=0

    def add_food(self):
        x=random.randint(1,self.size[1]-1)
        y=random.randint(1,self.size[0]-1)
        self.food.add((y,x))

    def get_pieces(self):
        output=(self.snake.body,self.food)
        return output

    def step(self,key):
        direction=''
        if key in ['w',curses.KEY_UP]:
            direction='U'
        elif key in ['s',curses.KEY_DOWN]:
            direction='D'
        elif key in ['a',curses.KEY_LEFT]:
            direction='L'
        elif key in ['d',curses.KEY_RIGHT]:
            direction='R'
        else:
            direction=self.snake.body[0][1]

        self.snake.forward(direction)
        if 0 in self.snake.body[0][0] or \
        self.snake.body[0][0][0] == self.size[0] or \
        self.snake.body[0][0][1] == self.size[1]:
            self.state="wall"
        elif self.snake.body[0][0] in [x[0] for  x in self.snake.body[1:]]:
            self.state="body"
        elif self.snake.body[0][0] in self.food:
            self.snake.add_Segment()
            self.food.pop()
            self.add_food()
            self.score+=1




def draw_Window(window,game):
    snake,foods=game.get_pieces()
    window.erase()
    window.border('|','|','-','-','/','\\','\\','/')
    window.addstr(0,0,str(game.score))
    
    character='@'
    previous_segment=snake[0]
    window.addch(*previous_segment[0],character)
    for segment in snake[2:]:
        if segment[1] in ('L','R'):
            character = '-'
        else:
            character = '|'
        if(not previous_segment[1]==segment[1]):
            if (previous_segment[1],segment[1]) in set([('L','D'),('U','R'),('R','U'),('D','L')]):
                character='/'
            else:
                character='\\'
        previous_segment=segment

        window.addch(*segment[0],character)
    for food in foods:
        character='X'
        window.addch(*food,character)

    window.move(0,0)

def main(stdscr):
# Clear screen
    stdscr.clear()
    size=(curses.LINES-2,curses.COLS-2)
    game_Window=stdscr.subwin(*size,1,1)
    game_Window.nodelay(1)

    game=Board((size[0]-1,size[1]-1))
    while(game.state =="play"):
        draw_Window(game_Window,game)
        game_Window.refresh()
        sleep(.1)
        try:
            key=game_Window.getkey()
        except:
            key=game.snake.body[0][1]
        game.step(key)

    game_Window.erase()
    message="score: "+str(game.score)
    game_Window.addstr(int(size[0]/2),int((size[1]/2)-len(message)/2),message)
    game_Window.refresh()
    sleep(5)

if __name__ == "__main__":
    curses.wrapper(main)
    