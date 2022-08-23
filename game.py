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
global g_box_download_rate
g_box_download_rate = 0.5

    
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
g_column = 13    #  当前 有多少列方块 g_width_pix/g_box_width
g_row = 23      #  当前有多少行方块  g_hight_pix/g_box_width
g_box_width = 10  
box_column=7    # box的当前列

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

    
    if 1 in g_tetris[0]:
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
    global box_column
    setScreenColor(0x0000)
    y=0
    #print(box_column)
    
    #print("=====drawbox=====")
    #print(g_tetris)
    title0 = M5Title(title="Score", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label0 = M5TextBox(86, 0, str(score), lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)

    for r in g_tetris:
        x=0
        for d in r:
            if d==1:
                #cheat
                #if x == box_column * g_box_width :
                    #M5Line(M5Line.PLINE, x, y, x, 240, 0xFFFFFF)
                M5Rect(x, y, g_box_width, g_box_width, color[3], 0x0640f7)
                #print('draw box x:%d y:%d'%(x,y))
            x+=g_box_width
        y+=g_box_width

def game():
    global gameover
    global g_tetris
    global g_box_download_rate
    while True:
        imu0 = imu.IMU()
        x = imu0.acceleration[0]
        z = imu0.acceleration[2]
        if btnA.wasPressed():
            up()
            print("up box changed")
        elif x < 0 and x < -0.2:
            right()
        elif x > 0 and x > 0.2:
            left()
        if z < 0.7 and z > -0.7:
            g_box_download_rate = 0.1
        else:
            g_box_download_rate = 0.5
             

        drawbox()
        autodown()
        time.sleep(g_box_download_rate)
        if gameover==True:
            setScreenColor(0x000000)
            title0 = M5Title(title="Score", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
            label0 = M5TextBox(86, 0, str(score), lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
            label1 = M5TextBox(36, 60, "Game", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
            label2 = M5TextBox(36, 107, "Over", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
            label3 = M5TextBox(10, 188, "Press M5 button ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
            label4 = M5TextBox(33, 211, "To Restart", lcd.FONT_Default, 0xFFFFFF, rotate=0)
            while True:
                if (btnA.wasPressed()):
                    time.sleep(1)
                    break;
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
    label3 = M5TextBox(24, 132, "press B button ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    print("hello")
    while True:
        if (btnA.wasPressed()):
            M5Led.on()
            setScreenColor(0)
            g_tetris.clear()
            for i in range(g_row):
                g_tetris.append([0]*g_column)
            
            enter()
            #print(g_tetris)
            game()

def main():
    global g_tetris
    for i in range(16):
        g_tetris.append([0]*g_column)
    restart()
main()
