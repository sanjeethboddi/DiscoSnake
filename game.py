#!/usr/bin/env python

from colorama import *
import time
import random
import os
import sys
import getch
import multiprocessing


#start of pos() funciton
def pos(x,y):
    return '\x1b['+str(y)+';'+str(x)+'H'
#end of pos() function


#start of display() function
#displays the game
def display():
    global board,board_width,board_height
    random_color=random.choice(colors)
    os.system('cls' if os.name=='nt' else 'clear')
    for _ in board:
        for element in _ :
            if element == 'u' or element == 'l' or element == 'd' or element == 'r':
                print("{col}██".format(col=random_color),end='')
            if element == 'w':
                print("██".format(col=random_color),end='')
            if element == 'f':
                print("🔵".format(col=random_color),end='')
            if element == 'o':
                print('  ',end ='')
        print()

#end of display() function


#start of movement() function
#checks the next position the snake is going to move based on direction it has
def movement():
    global next_pos,head,tail
    game_over = False
    while not game_over:
        display()
        direction = dir_object.value.decode("utf-8")
        if direction  == 'u':
            next_pos =(head[0]-1,head[1])
        elif direction  == 'd':
            next_pos =(head[0]+1,head[1])
        elif direction  == 'l':
            next_pos =(head[0],head[1]-1)
        elif direction  == 'r':
            next_pos =(head[0],head[1]+1)

        if board[next_pos[0]][next_pos[1]] == 'f':
            board[head[0]][head[1]] = direction
            board[next_pos[0]][next_pos[1]] = direction
            head = next_pos
            empty_spaces = list()
            for _ in board:
                empty_spaces.append([index for index, value in enumerate(_) if value == 'o'])

            while(1):
                try:
                    random_row = random.randint(0,len(empty_spaces)-1)
                    random_index = (random_row,random.choice(empty_spaces[random_row]))
                    board[random_index[0]][random_index[1]] = 'f'
                    break
                except:
                    pass
        elif board[next_pos[0]][next_pos[1]] != 'o' and board[next_pos[0]][next_pos[1]] != 'f':
            game_over = True
            print("Game_over")
            time.sleep(1)
            #blink()
        else:
            board[head[0]][head[1]] = direction
            board[next_pos[0]][next_pos[1]] = direction
            head = next_pos
            if board[tail[0]][tail[1]]=='u':
                board[tail[0]][tail[1]]='o'
                tail = (tail[0]-1,tail[1])
            elif board[tail[0]][tail[1]]=='d':
                board[tail[0]][tail[1]]='o'
                tail = (tail[0]+1,tail[1])
            elif board[tail[0]][tail[1]]=='l':
                board[tail[0]][tail[1]]='o'
                tail = (tail[0],tail[1]-1)
            elif board[tail[0]][tail[1]]=='r':
                board[tail[0]][tail[1]]='o'
                tail = (tail[0],tail[1]+1)

        time.sleep(0.1)
#end of movement() function
    status.value = 0


#start of game_start() function
def game_start(sv1,sv2,sv3,level=None):

    global dir_object,lock,status,next_pos,colors,score
    global head,tail,board,board_width,board_height

    dir_object = sv1
    lock = sv2
    status = sv3

    score = 0
    if(level == None):
        board = [
        ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','r','r','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','o','o','o','o','o','o','o','o','o','o','o','o','o','o','w'],
        ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
        ]
        # w - wall
        # r - body of snake moving right
        # l - body of snake moving left
        # u - body of snake moving up
        # d - body of snake moving down
        # f - food
        # o - empty space

        board_height = len(board)
        board_width =  len(board[board_height-1])
        head = (5,4)
        tail = (5,3)

    else:
        pass
    print("\x1b[8;{y};{x}t".format(y=board_height+5, x=board_width))

    empty_spaces = list()
    for _ in board:
        empty_spaces.append([index for index, value in enumerate(_) if value == 'o'])

    while(1):
        try:
            random_row = random.randint(0,len(empty_spaces)-1)
            random_index = (random_row,random.choice(empty_spaces[random_row]))
            board[random_index[0]][random_index[1]] = 'f'
            break
        except:
            pass

    colors=[Fore.BLACK,Fore.BLUE,Fore.CYAN,Fore.GREEN,Fore.YELLOW,Fore.MAGENTA,Fore.RED]

    movement()
#end of game_start() function

#start of keypress() function
def keypress(dir_object,lock,status):
    while(status.value == 1):
        key = getch.getch()
        direction = dir_object.value.decode("utf-8")
        try:
            lock.acquire()
            if key.lower() == 'w' and direction !='d':
                dir_object.value = b'u'
            elif key.lower() == 'a'and direction !='r':
                dir_object.value = b'l'
            elif key.lower() == 's'and direction !='u':
                dir_object.value = b'd'
            elif key.lower() == 'd'and direction !='l':
                dir_object.value = b'r'
            lock.release()

        except:
            lock.release()

#end of dir_input() function



#start of main() function
def main():
    sys.stdout.write('\33]0;* Disco-Snake *\a')
    init(autoreset=True)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("W - to move up ")
    print("S - to move down")
    print("A - to move left")
    print("D - to move right")
    print("==============")
    print("Keep Your fingers ready & Press any Key")
    x=getch.getch()

    dir_object = multiprocessing.Value('c', 1)
    dir_object.value = b'r'
    status = multiprocessing.Value('i', 1)
    status.value = 1
    # creating a lock object
    lock = multiprocessing.Lock()
    # creating new processes
    p1 = multiprocessing.Process(target=keypress, args=(dir_object,lock,status))
    p2 = multiprocessing.Process(target=game_start, args=(dir_object,lock,status))


    p1.start()
    p2.start()
#end of main() function

if __name__=="__main__":
    main()
