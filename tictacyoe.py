import pygame,sys
import numpy as np
import random
import button
pygame.init()

WIDTH=600
HEIGHT=600
board_rows=3
board_col=3
circle_radius=60
circle_width=15
cross_width=25
space=55

board=np.zeros((board_rows,board_col))

RED=(255,0,0)
BLUE=(0,0,255)
back_color=(28,170,156)
line_color=(23,145,135)
line_width=15

game_over=False
game_paused=False
menu_state="main"
player=1

#creating main screen 
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(back_color)



font=pygame.font.SysFont("arialblack",40)
text_col=(255,255,255)

#load button images
start_img=pygame.image.load("button_images/start_img.png").convert_alpha()
quit_img=pygame.image.load("button_images/quit.png").convert_alpha()

start_button=button.Button(170,100,start_img,1)
quit_button=button.Button(170,300,quit_img,1)


def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))


#board
def mark_square(row,col,player):
    board[row][col]=player

def is_avaliable(row,col):
    return board[row][col]==0

def is_full():
    for i in range(board_rows):
        for j in range(board_col):
            if board[i][j]==0:
                return False
    return True

def draw_lines():
    pygame.draw.line(screen,line_color,(0,190),(600,190),line_width)
    pygame.draw.line(screen,line_color,(0,395),(600,395),line_width)
    pygame.draw.line(screen,line_color,(190,0),(190,600),line_width)
    pygame.draw.line(screen,line_color,(395,0),(395,600),line_width)

def draw_figures():
    for i in range(board_rows):
        for j in range(board_col):
            if board[i][j]==1:
                pygame.draw.circle(screen,RED,(int(j*200+200/2),int(i*200+200/2)),circle_radius,circle_width)

            elif board[i][j]==2:
                pygame.draw.line(screen,BLUE,(j*200+space,i*200+200-space),(j*200+200-space,i*200+space),cross_width)
                pygame.draw.line(screen,BLUE,(j*200+space,i*200+space),(j*200+200-space,i*200+200-space),cross_width)
#draw_lines()

def check_win(player):
    for col in range(board_col):
        if board[0][col]==board[1][col]==board[2][col]==player:
            draw_vertical_winning_line(col,player)
            return True
        if board[col][0]==board[col][1]==board[col][2]==player:
            draw_horizontal_winning_line(col,player)
            return True
    
    if board[2][0]==board[1][1]==board[0][2]==player:
        draw_asc_diagonal(player)
        return True

    if board[0][0]==board[1][1]==board[2][2]==player:
        draw_desc_diagonal(player)
        return True
    return False
    

def draw_vertical_winning_line(col,player):
    posX=col*200+100
    if player==1:
        color=RED
    
    elif player==2:
        color=BLUE
    pygame.draw.line(screen,color,(posX,15),(posX,HEIGHT-15),15)

def draw_horizontal_winning_line(row,player):
    posY=row*200+100
    if player==1:
        color=RED
    
    elif player==2:
        color=BLUE
    pygame.draw.line(screen,color,(15,posY),(WIDTH-15,posY),15)

def draw_asc_diagonal(player):
    if player==1:
        color=RED
    
    elif player==2:
        color=BLUE
    pygame.draw.line(screen,color,(15,HEIGHT-15),(WIDTH-15,15),15)
    
def draw_desc_diagonal(player):
    if player==1:
        color=RED
    
    elif player==2:
        color=BLUE
    pygame.draw.line(screen,color,(15,15),(WIDTH-15,HEIGHT-15),15)

def restart():
    screen.fill(back_color)
    draw_lines()
    player=1
    for row in range(board_rows):
        for col in range(board_col):
            board[row][col]=0
    return player

def rand():
    position_i = random.randint(0, 2)
    position_y= random.randint(0, 2)
    return comp(position_i,position_y)

def comp(position_i,position_y):
     
    if board[position_i][position_y] == 0:  
        mark_square(position_i,position_y,2)
    else:
        return rand()

run = True
#Mainloop
while run:
    screen.fill(back_color)
    draw_lines()
    draw_figures()
    check_win(player)
    
    if game_paused==True:
        screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        screen.fill(back_color)
        if menu_state=="main":
            if start_button.draw(screen):
                game_paused=False
            if quit_button.draw(screen):
                run=False
    else:
        draw_text("Press space to pause",font,text_col,80,260)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row=int(mouseY)//190
            clicked_col=int(mouseX)//190

            if is_avaliable(clicked_row,clicked_col):
                if player==1:
                    mark_square(clicked_row,clicked_col,1)
                    if check_win(player):
                        game_over=True
                    player=2
                
                if player==2:
                    rand()

                if check_win(player):
                    game_over=True
                #print(board)
                player=1

                draw_figures()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                restart()

            if event.key==pygame.K_SPACE:
                game_paused= True


    pygame.display.update()

