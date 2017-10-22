from colorama import *
import time
import random
import os
import multiprocessing
import getch




class Cell(object):
    cell_value="[]"
    def __init__(self,Xpos,Ypos):
        self.Xpos=Xpos
        self.Ypos=Ypos

    def __str__(self):
        return 'Xposition:'+str(self.Xpos)+' Ypostition'+str(self.Ypos)

#start of pos() funciton
def pos(x,y):
    """
    takes integers as arguements and returns a escape sequence string for position
    """
    return '\x1b['+str(y)+';'+str(x)+'H'
#end of pos() function


#start of board() function
#plots the snake in terminal
def board():
    """
    takes no arguements
    """
    global window_xsize,window_ysize,score
    random_color=random.choice(colors)
    os.system('clear')
    print("{loc}{val}".format(val=food.cell_value,loc=pos(food.Xpos,food.Ypos)),end='')
    for i in snake:
        print("{col}{loc}{val}".format(col=random_color,loc=pos(i.Xpos,i.Ypos),val=i.cell_value))
    print("{loc}========================================".format(loc=pos(1,window_ysize+1)))
    print("{loc}Score : {scor}".format(loc=pos(1,window_ysize+2),scor=score))
    print("{loc}HighScore :in the next update".format(loc=pos(1,window_ysize+3)))
#end of board() function


#start of movement() function
#checks the next position the snake is going to move based on dirction it has
def movement(direction,game_over,lock,moved):
    """
    takes 4 arguements
    direction(Shared Object),game_over(Shared object),lock(Lock object),moved(Shared Object)

    """
    global next_pos , snake ,colors,food,window_xsize,window_ysize,window_size,snake_pos,score
    while not game_over.value:
        board()
        if(chr(direction.value).upper()=='W'):
            next_pos =((snake[0].Xpos),(snake[0].Ypos)-1)
            moved.value=1
        elif(chr(direction.value).upper()=='A'):
            next_pos =((snake[0].Xpos)-2,(snake[0].Ypos))
            moved.value=1
        elif(chr(direction.value).upper()=='S'):
            next_pos =((snake[0].Xpos),(snake[0].Ypos)+1)
            moved.value=1
        elif(chr(direction.value).upper()=='D'):
            next_pos =((snake[0].Xpos)+2,(snake[0].Ypos))
            moved.value=1

        if next_pos == (food.Xpos,food.Ypos):
            score+=1
            cell_obj=Cell(next_pos[0],next_pos[1])
            snake.insert(0,cell_obj)
            random_pos=random.choice(list(set(window_size).difference(set(snake))))
            food=Cell(random_pos[0],random_pos[1])

        elif any(map(lambda x : x.Xpos==next_pos[0]and x.Ypos==next_pos[1],snake)) or window_size.count(next_pos)==0:
            lock.acquire()
            game_over.value=1
            lock.release()

        else:
            snake.insert(0,Cell(next_pos[0],next_pos[1]))
            snake.pop()
        time.sleep(0.1)

#end of movement() function


#start of game_start() function
#starts the game by initializing some variables(runs as a seperate process)
def game_start(direction,game_over,lock,moved):
    """
    takes 4 arguements
    direction(Shared Object),game_over(Shared object),lock(Lock object),moved(Shared Object)

    """
    global next_pos , snake ,colors,food,window_xsize,window_ysize,window_size,score
    score=0
    window_xsize=40
    window_ysize=20
    print("\x1b[8;{y};{x}t".format(y=(window_ysize+5), x=window_xsize))
    window_size=list()
    global i,j
    i=1
    while i<=window_xsize:
        j=1
        while j<=window_ysize:
            window_size.append((i,j))
            j+=1
        i+=2
    window_size=list(set(window_size))
    next_pos=tuple()
    snake =list()
    cell_obj= Cell(3,3)
    snake.append(cell_obj)
    cell_obj=Cell(1,3)
    snake.append(cell_obj)
    random_pos=random.choice(list(set(window_size).difference(set(snake))))
    food=Cell(random_pos[0],random_pos[1])
    colors=[Fore.BLACK,Fore.BLUE,Fore.CYAN,Fore.GREEN,Fore.YELLOW,Fore.MAGENTA,Fore.RED]
    movement(direction,game_over,lock,moved)
#end of game_start() function

#start of dir_input() function
#takes userinput till the game completes (runs as a different process)
def dir_input(direction,game_over,lock,moved):
    """
    takes 4 arguements
    direction(Shared Object),game_over(Shared object),lock(Lock object),moved(Shared Object)

    """
    while not game_over.value:
        x=str(getch.getch()).upper()
        if(x=='W' or x=='S' or x=='A' or x=='D')and moved.value==1:
            lock.acquire()
            y=chr(direction.value).upper()
            if((y=='S' and x!='W')or (y=='A' and x!='D') or (y=='D' and x!='A') or(y=='W' and x!='S')):
                direction.value=ord(x)
                moved.value=0
            lock.release()
#end of dir_input() function

#start of main() function
def main():
    init(autoreset=True)
    game_over = multiprocessing.Value('i')
    game_over.value = 0
    direction = multiprocessing.Value('i')
    direction.value=ord('D')
    moved = multiprocessing.Value('i')
    moved.Value=0
    lock = multiprocessing.Lock()
    process1=multiprocessing.Process(target=dir_input,args=(direction,game_over,lock,moved))
    process2=multiprocessing.Process(target=game_start,args=(direction,game_over,lock,moved))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
#end of main() function

if __name__=="__main__":
    main()
