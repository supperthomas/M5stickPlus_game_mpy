import uos
import machine
from time import sleep_us
import random
import framebuf
from time import sleep
from m5stack import *
from m5ui import *
from uiflow import *
import imu
global g_tetris
g_tetris=[]

    
boxo=[[1,1],[1,1]]
boxz_1=[[1,1,0],[0,1,1],[0,0,0]]
boxz_2=[[0,1,1],[1,1,0],[0,0,0]]
box7_1=[[1,1,0],[0,1,0],[0,1,0]]
box7_2=[[0,1,1],[0,1,0],[0,1,0]]
boxt=[[0,1,0],[1,1,1],[0,0,0]]
boxi=[[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0]]
boxes=[boxo,boxz_1,boxz_2,box7_1,box7_2,boxt,boxi]
color=[0xFFE0,0x867f,0x7ef,0xfb08]
score=0

box_row=0
global gameover
gameover=False


box_row=0


global g_width_pix
global g_hight_pix
global g_column
global g_row
global g_box_width
global box_column

g_width_pix = 135
g_hight_pix = 240
#9 16 15
#13 24 10
g_column = 9    #  当前 有多少列方块 g_width_pix/15
g_row = 16      #
g_box_width = 15  
box_column=4    # box的当前列

#color
color_background = 0x0 

def newbox():
    box_id=random.randint(0,6)  #随机一个方块形状
    box_org=boxes[box_id]        #获取方块形状数组
    b=[]
    for i in range(len(box_org)):
        b.append(box_org[i][:])    
    return b                     #返回方块
box=newbox()              #当前运动中的方块

def clockwise():
    N=len(box)
    a=[]
    for i in range(N):
        a.append(box[i][:])
    for i in range(N):
        for j in range(N):
            box[N-j-1][i]=a[i][j]
            
def counter_clockwise():
    N=len(box)
    a=[]
    for i in range(N):
        a.append(box[i][:])
    for i in range(N):
        for j in range(N):
            box[j][N-i-1]=a[i][j]
            
#box中所有的方块离开当前坐标，向下一个坐标进军
def leave():
    global box_column
    global g_tetris
    j=box_row
    for r in box:
        i=box_column
        for d in r:
            if d==1:
                g_tetris[j][i]=0
            i+=1
        j+=1

def enter():
    #print("enter")
    global box_row
    global box_column
    global g_tetris
    j=box_row
    for r in box:
        i=box_column
        for d in r:
            if d==1:
                g_tetris[j][i]=1
            i+=1
        j+=1

        
def checkvalid():
    global box_row
    global box_column
    global g_tetris
    j=box_row
    for r in box:
        i=box_column
        for d in r:
            if d==1:
                if i<0 or i>=g_column:
                    return False
                
                if j<0 or j>=g_row:
                    return False
                
                if g_tetris[j][i]==1:
                    return False
                
            i+=1
        j+=1
    return True
def up():
    leave()
    clockwise()
    if checkvalid()==False:
        counter_clockwise()
    enter()
    
def down():
    global box_row
    leave()
    box_row+=1
    if checkvalid()==False:
        box_row-=1
    enter()
def left():
    global box_column
    leave()
    box_column-=1
    if checkvalid()==False:
        box_column+=1
    enter()

def right():
    global box_column
    leave()
    box_column+=1
    if checkvalid()==False:
        box_column-=1
    enter()
def clear():
    global score,gameover
    global g_tetris
    i=0
    c=0
    while i<g_row:
        if 0 in g_tetris[i]:
            i+=1
        else:
            c+=1
            del g_tetris[i]
            g_tetris.insert(0,[0]*g_column)
    if c>0:
        score +=50*(2**(c-1))
        if score>1000:
            score=999
        print(score,"a")
    
    if 1 in g_tetris[0]:
        print("===========test========")
        gameover = True
def autodown():
    global box_row,box_column,box,box_id
    leave()
    box_row+=1
    if checkvalid()==False:
        box_row-=1
        enter()
        clear()
        
        box=newbox()
        box_column=4
        box_row=0
    enter()

def drawbox():
    global color
    global g_tetris
    setScreenColor(0x0000)
    y=0
    #print("=====drawbox=====")
    #print(g_tetris)
    
    for r in g_tetris:
        x=0
        for d in r:
            if d==1:
                M5Rect(x, y, g_box_width, g_box_width, color[3], 0x10)
                #display.rect(x,y,15,15,0x10)
                #display.fill_rect(x+1,y+1,13,13,color[3])
                #print('draw box x:%d y:%d'%(x,y))
            x+=g_box_width
        y+=g_box_width

def game():
    global gameover
    global g_tetris
    while True:
        imu0 = imu.IMU()
        c = imu0.acceleration[0]
        print("=====box_column=before====",box_column)

        if btnB.wasPressed():
            up()
            print("up box changed")
        elif c < 0 and c < -0.2:
            right()
#             print("right")
        elif c > 0 and c > 0.2:
            left()
#             print("left")
        print("=====box_column=after====",box_column)

        drawbox()
        autodown()
        time.sleep(0.5)
        if gameover==True:
            #mysong.stop()
            #display.fill(0x0000)
            setScreenColor(0x000000)
            #display.text(font2,"===GAME===",45,60)
            #display.text(font2,"===OVER===",45,130)
            print("game end")
            #print(g_tetris)
            time.sleep(0.2)
            gameover = False
            restart()
def restart():
    global g_tetris
    setScreenColor(0)
    label0 = M5TextBox(14, 169, "start game", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
    rectangle0 = M5Rect(40, 21, 25, 25, 0xec0606, 0xFFFFFF)
    label1 = M5TextBox(40, 104, "Please", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    circle0 = M5Circle(100, 34, 12, 0xeae407, 0xe60a0a)
    label2 = M5TextBox(0, 73, "Welcome to Tetris", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    label3 = M5TextBox(24, 132, "pulse button ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    print("hello")
    while True:
        if (btnA.wasPressed()):
            M5Led.on()
            print(".....")
            setScreenColor(0)
            g_tetris.clear()
            for i in range(g_row):
                g_tetris.append([0]*g_column)
            
            enter()
            #print(g_tetris)
            game()

def main():
    global g_tetris
    #hardware.init()
    #hardware.tft.fill(st7789.BLUE)
    for i in range(16):
        g_tetris.append([0]*g_column)
    restart()
main()
