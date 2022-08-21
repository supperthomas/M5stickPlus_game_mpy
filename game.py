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
global g
g=[]
for i in range(16):
    g.append([0]*12)
    
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
box_column=4
box_row=0
global gameover
gameover=False

box_column=4
box_row=0
disp_width=136
disp_height=240


global g_width_pix
global g_hight_pix
global g_column
global g_row
global g_box_width

g_width_pix = 135
g_hight_pix = 240
g_column = 12
g_row = 16
g_box_width = 15


def newbox():
    box_id=random.randint(0,6)  #随机一个方块形状
    box_org=boxes[box_id]        #获取方块形状数组
    b=[]
    for i in range(len(box_org)):
        b.append(box_org[i][:])    
    return b                     #返回方块
box=newbox()
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
            
def leave():
    j=box_row
    for r in box:
        i=box_column
        for d in r:
            if d==1:
                g[j][i]=0
            i+=1
        j+=1

def enter():
    print("enter")
    global box_row
    global box_column
    j=box_row
    for r in box:
        i=box_column
        for d in r:
            if d==1:
                g[j][i]=1
            i+=1
        j+=1

        
def checkvalid():
    global box_row
    global box_column
    j=box_row
    for r in box:
        i=box_column
        for d in r:
            if d==1:
                if i<0 or i>=12:
                    return False
                
                if j<0 or j>=16:
                    return False
                
                if g[j][i]==1:
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
        box_column-=1
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
    i=0
    c=0
    while i<16:
        if 0 in g[i]:
            i+=1
        else:
            c+=1
            del g[i]
            g.insert(0,[0]*12)
    if c>0:
        score +=50*(2**(c-1))
        if score>1000:
            score=999
        print(score,"a")
    
    if 1 in g[0]:
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
#     display = hardware.tft
    global color
    setScreenColor(0x0000)
    y=0
    for r in g:
        x=0
        for d in r:
            if d==1:
                M5Rect(x, y, g_box_width, g_box_width, color[3], 0x10)
                #display.rect(x,y,15,15,0x10)
                #display.fill_rect(x+1,y+1,13,13,color[3])
            x+=g_box_width
        y+=g_box_width

def game():
    #display = hardware.tft

    while True:
        imu0 = imu.IMU()
        c = imu0.acceleration[0]
        print("game")
        print("acceleration[0] x ",c)
        if c>0 and c > 0.2 :
            if(c > 0.5):
                print("fast left")
            else:
                print("left")
        elif c<0 and c < -0.2:
            if(c < -0.5):
                print("fast right")
            else:
                print("right")
        #if buttonB.value()==0:
        if btnB.wasPressed():
            up()
            print("g.append([0]*12)up")
        elif c < 0 and c < -0.2:
            right()
            print("right")
        elif c > 0 and c > 0.2:
            left()
            print("left")

        drawbox()
        #M5Rect(136-30, 0, 25, 25, 0xec0606, 0xFFFFFF)
        #display.fill_rect(181,0,4,240,color[1])
#         display.fill_rect(236,0,4,240,color[1])
#         display.text(font1,"Score",185,20)
#         display.text(font2,str(score),185,60)
#         display.text(font1,"Micro",185,120,color[2])
#         display.text(font1,"Python",185,150,color[2])
#         display.text(font1,"Tetris",185,200,color[2])
        autodown()
        time.sleep(1)
        if gameover==True:
            #mysong.stop()
            #display.fill(0x0000)
            setScreenColor(0x000000)
            #display.text(font2,"===GAME===",45,60)
            #display.text(font2,"===OVER===",45,130)
           
            print("game end")
            print(g)
            time.sleep(1)
            restart()
def restart():
    #display = hardware.tft
    #display.fill(0x0000)
    #display.fill_rect(4,0,4,240,0x07FFF)
    #display.fill_rect(227,0,4,240,0x077FF)
    #display.text(font2,"muc hyy",30,10,color=0x4416)
    #display.text(font2,"A to start",30,130,color=0x7e0)
    #display.text(font2,"Tetris",70,60,color=0x471a)
    #buttonValueB=buttonB.value()
    setScreenColor(0x111111)
    label0 = M5TextBox(14, 169, "start game", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
    rectangle0 = M5Rect(40, 21, 25, 25, 0xec0606, 0xFFFFFF)
    label1 = M5TextBox(40, 104, "Please", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    circle0 = M5Circle(100, 34, 12, 0xeae407, 0xe60a0a)
    label2 = M5TextBox(0, 73, "Welcome to Tetris", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    label3 = M5TextBox(24, 132, "pulse button ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    print("hello")
    while True:
        #buttonValueA=buttonA.value()
        #if buttonValueA==0:
        if (btnA.wasPressed()):
            M5Led.on()
            print(".....")
            setScreenColor(0)
            g=[]
            for i in range(16):
                g.append([0]*12)
            enter()
            print(g)
            game()

def main():
    #hardware.init()
    #hardware.tft.fill(st7789.BLUE)
    restart()
main()
