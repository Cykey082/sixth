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
sto=storage()

def easeInQuad(quotient):
    return (quotient)**2
def easeOutQuad(quotient):
    return 1-(1-quotient)**2

class Draw:
    font=pygame.font.Font(None,36)
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

class Object:
    def __init__(self):
        self.x=0
        self.y=0
        self.width=0
        self.height=0
        self.color=(0,0,0)
    def tick(self):
        pass
    def draw(self):
        canvas=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        pygame.draw.rect(canvas,self.color,pygame.rect.Rect(0,0,self.width,self.height),border_radius=5)
        screen.blit(canvas,(self.x,self.y),special_flags=pygame.BLEND_ALPHA_SDL2)

class Room:
    def __init__(self):
        self.color=(0,0,0)
        self.objects=[]
    def tick(self):
        screen.fill(self.color)
        for obj in self.objects:
            obj.tick()
class Grid(Object):
    def __init__(self,x,y,offset=0):
        super().__init__()
        self.x=x
        self.y=y
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
        self.draw()

class Block(Object):
    def __init__(self,x,y,belong=0,offset=0):
        super().__init__()
        self.x=x
        self.y=y
        self.width0=60
        self.height0=60
        self.xc0=self.x+self.width0/2
        self.yc0=self.y+self.height0/2
        self.offset=offset
        self.color=red if belong==1 else blue if belong==2 else grey
        self.color=[*self.color,255]
        self.event="blooming"
    def tick(self):
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
                    self.x=self.xc0-self.width/2
                    self.y=self.yc0-self.height/2
                elif self.offset==10:
                    self.event=None
                    self.offset=0
        if  self.event==None and Mouse.pressed[0] and not Mouse.last_pressed[0] and Mouse.inrect(self.x,self.y,self.width,self.height):
            self.event="tapping"
            self.offset=0

        self.draw()

class Entry(Room):
    def __init__(self):
        super().__init__()
        self.color=(178,178,178)
        self.objects+=[Grid((width-440)/2+90*(i%5),(height-350)/2+90*(i//5),-5*(i%5+i//5))for i in range(20)]
        self.objects+=[Block(10+70*(i%2),(height-480)/2+70*(i//2),belong=1,offset=-5*(i%2+i//2))for i in range(14)]
        self.objects+=[Block(150,490,belong=1,offset=-40)]
        self.objects+=[Block(width-140+70*(i%2),(height-480)/2+70*(i//2),belong=2,offset=-5*(i%2+i//2))for i in range(14)]
        self.objects+=[Block(590,490,belong=2,offset=-30)]
    def tick(self):
        super().tick()

running = True
room=Entry()
while running:
    Mouse.last_pressed=Mouse.pressed
    Mouse.pressed=pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    room.tick()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
