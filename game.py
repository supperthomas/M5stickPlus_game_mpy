import uos
import machine
from time import sleep_us
import random
import framebuf
from time import sleep
from m5stack import *
from m5ui import *
from uiflow import *
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
global cell
global gameover
gameover=False
cell=15
box_column=4
box_row=0
song= '0 E5 2 14;4 B4 2 14;6 C5 2 14;8 D5 2 14;10 E5 1 14;11 D5 1 14;12 C5 2 14;14 B4 2 14;16 A4 2 14;20 A4 2 14;22 C5 2 14;24 E5 2 14;28 D5 2 14;30 C5 2 14'   
st7789_res=0
st7789_dc=1
disp_width=240
disp_height=240


def newbox():
    box_id=random.randint(0,6)
    box_org=boxes[box_id]
    b=[]
    for i in range(len(box_org)):
        b.append(box_org[i][:])
    return b
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
                M5Rect(x, y, 15, 15, color[3], 0x10)
                #display.rect(x,y,15,15,0x10)
                #display.fill_rect(x+1,y+1,13,13,color[3])
            x+=cell
        y+=cell

def game():
    #display = hardware.tft
    print("game")
    while True:
        xValue=1#xAxis.read_u16()
        yValue=2#yAxis.read_u16()
        f=4
        #if buttonB.value()==0:
#         if 1==0:
#             up()
#             print("up")
#         elif yValue >40000:
#             right()
#             print("right")
#         elif yValue <1000:
#             left()
#             print("left")
#         elif xValue >40000:
#             down()
#             print("down")
#         else:
#             print("stop")
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
            #display.text(font2,"===GAME===",45,60)
            #display.text(font2,"===OVER===",45,130)
            print("game end")
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
            game()

def main():
    #hardware.init()
    #hardware.tft.fill(st7789.BLUE)
    restart()
main()
