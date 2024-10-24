from sixth import *
import pygame
import os
import math
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
pygame.init()
red=(0xc7,0x4a,0x47)
blue=(0x4a,0x97,0xc3)
grey=(0xc4,0xc4,0xc4)
white=(255,255,255)
white_half=(255,255,255,32)
black=(0,0,0)
black_half=(0,0,0,16)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("sixth")
clock = pygame.time.Clock()
sto=storage()#real
# sto_disp=storage()#display
class Game:
    turn=1
    target=None
def easeInQuad(quotient):
    return (quotient)**2
def easeOutQuad(quotient):
    return 1-(1-quotient)**2
class Draw:
    font=pygame.font.Font("NormalFont.ttf",36)
    def text(x,y,text,col=black,scale=1):
        text=Draw.font.render(text,True,col)
        text=pygame.transform.scale(text,(int(text.get_width()*scale),int(text.get_height()*scale)))
        screen.blit(text,(x,y))
    def text_inrect(x,y,w,h,text,col=black,scale=1,alpha=255):
        text=Draw.font.render(text,True,col).convert_alpha()
        text.set_alpha(alpha)
        text=pygame.transform.scale(text,(int(text.get_width()*scale),int(text.get_height()*scale)))
        screen.blit(text,(x+(w-text.get_width())/2,y+(h-text.get_height())/2),special_flags=pygame.BLEND_ALPHA_SDL2)
    def rect(x,y,w,h,col=black,border_radius=0):
        canvas=pygame.Surface((w,h),pygame.SRCALPHA)
        pygame.draw.rect(canvas,col,pygame.rect.Rect(0,0,w,h),border_radius=border_radius)
        screen.blit(canvas,(x,y),special_flags=pygame.BLEND_ALPHA_SDL2)
class Mouse:
    def get():
        return pygame.mouse.get_pos()
    def inrect(x,y,w,h):
        mouse_x,mouse_y=Mouse.get()
        return x<=mouse_x and mouse_x<=x+w and y<=mouse_y and mouse_y<=y+h
    pressed=[False,False,False]
    last_pressed=[False,False,False]
    clicked=[None,None,None]
    last_clicked=[None,None,None]
class Object:
    def __init__(self):
        self.x=0
        self.y=0
        self.width=0
        self.height=0
        self.color=black
    def tick(self):
            pass
    def draw(self):
        canvas=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        pygame.draw.rect(canvas,self.color,pygame.rect.Rect(0,0,self.width,self.height),border_radius=5)
        screen.blit(canvas,(self.x,self.y),special_flags=pygame.BLEND_ALPHA_SDL2)
class Room:
    def __init__(self):
        self.color=(0,0,0)
        self.objects:list[Object]=[]
    def tick(self):
        screen.fill(self.color)
        for obj in self.objects:
            obj.tick()
class Grid(Object):
    def __init__(self,x,y,status,offset=0):
        super().__init__()
        self.x=x
        self.y=y
        self.width0=80
        self.height0=80
        self.xc0=self.x+self.width0/2
        self.yc0=self.y+self.height0/2
        self.id=status
        self.status=sto.status[status]
        self.offset=offset
        self.color=[166,166,166,255]
        self.event="blooming"
    def tick(self):
        if self.event!=None:
            self.offset+=1
            if self.event=="blooming":
                if self.offset in range(0,30):
                    q=(self.offset+1)/30
                    self.width=80*easeOutQuad(q)
                    self.height=self.width
                elif self.offset==30:
                    self.event=None
                    self.offset=0
                else:
                    self.width=0
                    self.height=0
        if  Mouse.clicked[0]==self and self.event==None:
            if Mouse.last_clicked[0]!=None:
                if Game.target!=None and Game.target in range(20,50):
                    Game.target=None
                    t:Block=Mouse.last_clicked[0]
                    action=self.id*15+t.id-20
                    print(input_args[action],end=" ")
                    if Game.turn==2:sto.reverse()
                    if sto.canput(arg=action):
                        print("canput")
                        t.xc=self.xc0
                        t.yc=self.yc0
                        t.event="tapping"
                        room.args=sto.putf(arg=action)
                        room.event="update"
                        room.offset=-30
                    else:
                        print("INVALID")
                    if Game.turn==2:sto.reverse()
            else:Game.target=self.id
        self.draw()
class Block(Object):
    icons="0123456789↑↓←→×"
    def __init__(self,x,y,status,belong,offset=0):
        super().__init__()
        self.x=x
        self.y=y
        self.width0=60
        self.height0=60
        self.id=status
        self.belong=belong
        if self.id==34:self.id=30
        elif self.id>=30:self.id+=1
        self.icon=Block.icons[status-20-15*(belong-1)]
        self.status=sto.status[status]+15*(belong-1)
        self.xc0=self.x+self.width0/2
        self.yc0=self.y+self.height0/2
        self.xc=self.xc0
        self.yc=self.yc0
        self.offset=offset
        self.color=red if belong==1 else blue if belong==2 else grey
        self.color=[*self.color,255]
        self.event="blooming"
    def tick(self):
        super().tick()
        self.status=sto.status[self.id+15*(self.belong-1)]
        if self.event!=None:
            
            self.offset+=1
            if self.event=="blooming":
                if self.offset in range(0,30):
                    q=(self.offset+1)/30
                    self.width=60*easeOutQuad(q)
                    self.height=self.width
                elif self.offset==30:
                    self.event=None
                    self.offset=0
                else:
                    self.width=0
                    self.height=0
            elif self.event=="tapping":
                if self.offset in range(0,10):
                    q=(self.offset+1)/10
                    self.width=50+10*q
                    self.height=self.width
                    self.x=self.xc-self.width/2
                    self.y=self.yc-self.height/2
                elif self.offset==10:
                    self.event=None
                    self.offset=0
            elif self.event=="damocles":
                print(self.event,self.status)
                if self.status==3:
                    if self.offset in range(0,60):
                        q=(self.offset+1)/60
                        self.width=60+30*easeOutQuad(q)
                        self.color[3]=255-255*easeInQuad(q)
                        self.height=self.width
                        self.x=self.xc-self.width/2
                        self.y=self.yc-self.height/2
                    elif self.offset==60:
                        self.event=None
                        self.offset=0
                        self.xc=self.xc0
                        self.yc=self.yc0
                        self.width=self.width0
                        self.height=self.height0
                        self.x=self.xc-self.width/2
                        self.y=self.yc-self.height/2
                else:
                    self.event=None
                    self.offset=0
            elif self.event=="morpheus":
                pass
        if self.event==None and Mouse.pressed[0] and not Mouse.last_pressed[0] and Mouse.inrect(self.x,self.y,self.width,self.height):
            if self.belong==Game.turn:
                self.event="tapping"
                self.offset=0
                Game.target=self.id
        if self.status==3 and not self.event:return
        self.draw()
        Draw.text_inrect(self.x,self.y,self.width,self.height,self.icon,white,self.width/self.width0,alpha=self.color[3])
        if Mouse.clicked[0]==self:
            Draw.rect(self.x,self.y,self.width,self.height,black_half)
        elif Mouse.inrect(self.x,self.y,self.width,self.height):
            Draw.rect(self.x,self.y,self.width,self.height,white_half)
class Entry(Room):
    def __init__(self):
        super().__init__()
        self.event=None
        self.args=[]
        self.offset=0
        self.color=(178,178,178)
        self.objects+=[Grid((width-440)/2+90*(i%5),(height-350)/2+90*(i//5),i,-5*(i%5+i//5))for i in range(20)]
        self.objects+=[Block(10+70*(i%2),(height-480)/2+70*(i//2),status=20+i,belong=1,offset=-5*(i%2+i//2))for i in range(14)]
        self.objects+=[Block(150,490,status=34,belong=1,offset=-40)]
        self.objects+=[Block(width-140+70*(i%2),(height-480)/2+70*(i//2),status=20+i,belong=2,offset=-5*(i%2+i//2))for i in range(14)]
        self.objects+=[Block(590,490,status=34,belong=2,offset=-30)]
    def tick(self):
        if self.event!=None:
            if self.event=="update":
                if self.offset==0:
                    sto.display()
                    status=[_ for _ in sto.status]
                    self.args=sto.update(args=self.args)
                    kills=[19+status[_]%11+status[_]//11*15 for _ in self.args]
                    print(kills)
                    for i in kills:
                        self.objects[i].event="damocles"
                        self.objects[i].offset=0
                    if not self.args:
                        self.event=None
                        self.offset=0
                        Game.turn=3-Game.turn
                        # sto.reverse()
                    else:
                        self.offset=-60
                else:
                    self.offset+=1
        else:
            self.offset=0
        super().tick()
running = True
room=Entry()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:running = False
    Mouse.last_pressed=Mouse.pressed
    Mouse.pressed=pygame.mouse.get_pressed()
    if any(Mouse.pressed):
        _clicked = [obj for obj in room.objects if Mouse.inrect(obj.x, obj.y, obj.width, obj.height)]
        _clicked = _clicked[-1] if _clicked else None
        for i in range(3):
            if Mouse.pressed[i] and not Mouse.last_pressed[i]:
                Mouse.last_clicked[i] = Mouse.clicked[i]
                Mouse.clicked[i] = _clicked
    room.tick()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
