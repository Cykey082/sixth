# Sixth 2024-10-04
# This is a typical class for sixth.
# Use as you wish!
BACK_BLACK="\033[40m"
BACK_RED="\033[41m"
BACK_BLUE="\033[44m"
BACK_WHITE="\033[47m"
FORE_BLACK="\033[30m"
FORE_RED="\033[31m"
FORE_BLUE="\033[34m"
FORE_WHITE="\033[37m"
COL_RESET="\033[0m"
display_text="0123456789X↑↓←→"
input_text="0123456789xudlr"
input_args=[]
for i in "1234":
    for j in "12345":
        for k in input_text:
            input_args.append(i+j+k)

class storage:
    def __init__(self) -> None:self.status:list[int]=[0]*20+[1]*30
    def display(self)->None:display(self.status)
    def canput(self,arg:int)->bool:return canput(self.status,arg)
    def putf(self,arg:int)->list[int]:return put(self.status,arg)
    def update(self,args:list[int])->None:return update(self.status,args)
    def choices(self)->list[int]:return choices(self.status)
    def evaluate(self)->tuple[int]:return evaluate(self.status)
    def reverse(self)->list[int]:return reverse(self.status)
    def is_gameover(self)->bool:return is_gameover(self.status)  
def display(status:list[int])->None:#Simple output of the Board
    print("i\\j 1  2  3  4  5 ",end='')
    for i in range(20):
        if not i%5:print("\n %d "%(i//5+1),end='')
        if status[i] in range(1,12):print(f"{BACK_RED}[{display_text[status[i]-1]}]{COL_RESET}",end='')
        elif status[i] in range(12,23):print(f"{BACK_BLUE}[{display_text[status[i]-12]}]{COL_RESET}",end='')
        else:print(f"{BACK_WHITE}{FORE_BLACK}[ ]{COL_RESET}",end='')
    print(f"\n{BACK_RED}P1{COL_RESET}",end=' ')
    for i in range(20,35):
        if status[i]==1:print(f"{BACK_RED}[{display_text[i-20]}]{COL_RESET}",end='')
    print(f"\n{BACK_BLUE}P2{COL_RESET}",end=' ')
    for i in range(35,50):
        if status[i]==1:print(f"{BACK_BLUE}[{display_text[i-35]}]{COL_RESET}",end='')
    print("")
    return
def canput(status:list[int],arg:int)->bool:
    if not arg in range(300):return False
    a,b,c,i=arg//75,arg//15%5,arg%15,arg//15
    if status[20+c]!=1:
        if status[20+c]==2 or not c in range(10):return False
        if status[20]!=1:return False
    if c in range(10):return status[i]<=c
    if c==10:return not status[i]
    elif not status[i]:return False
    if c==11:return a and not status[i-5]
    if c==12:return a!=3 and not status[i+5]
    if c==13:return b and not status[i-1]
    if c==14:return b!=4 and not status[i+1]
    return False
def put(status:list[int],arg:int)->list[int]:#WARNING:Ensure canput!!!
    c,i=arg%15,arg//15
    if status[20+c]!=1:status[20]=3
    if c in range(11):
        if status[i]:status[status[i]+19]=1
        status[i],status[20+c]=c+1,2
        return [i]
    if c in range(11,15):
        p=[-5,+5,-1,+1][c-11]
        status[i+p],status[i],status[20+c]=status[i],0,2
        return [i,i+p]
def update(status:list[int],args:list[int]):
    kill=[False]*20
    for arg in args:
        i,j=arg//5,arg%5
        targ=status[arg]
        dirs=[[-1,0],[0,1],[1,0],[0,-1]]
        sums:list[list[int]]=[]
        for dir in dirs:
            a,b,s,n=i+dir[0],j+dir[1],0,0
            while a in range(4)and b in range(5):
                p=a*5+b
                t=status[p]
                a,b=a+dir[0],b+dir[1]
                if t==0:continue
                if t%11==0:break
                if t>11:t-=11
                s+=t-1
                n+=1
            sums.append([s,n])
        if targ==0:#Empty
            suml=[[sums[_][0]+sums[_+2][0],sums[_][1]+sums[_+2][1]]for _ in range(2)]
            for _ in range(2):
                if suml[_][1]>=2 and suml[_][0]%6==0:
                    for dir in [dirs[_],dirs[_+2]]:
                        a,b=i+dir[0],j+dir[1]
                        while a in range(4)and b in range(5):
                            p=a*5+b
                            t=status[p]
                            a,b=a+dir[0],b+dir[1]
                            if t==0:continue
                            if t%11==0:break
                            kill[p]=True
        elif targ%11:#Number
            suml=[[sums[_][0]+sums[_+2][0]+targ%11-1,sums[_][1]+sums[_+2][1]+1]for _ in range(2)]#counting on myself
            for _ in range(2):
                if suml[_][1]>=2 and suml[_][0]%6==0:
                    kill[arg]=True #also kill myself
                    for dir in [dirs[_],dirs[_+2]]:
                        a,b=i+dir[0],j+dir[1]
                        while a in range(4)and b in range(5):
                            p=a*5+b
                            t=status[p]
                            a,b=a+dir[0],b+dir[1]
                            if t==0:continue
                            if t%11==0:break
                            kill[p]=True
        else:#Barrier
            for _ in range(4):
                if sums[_][1]>=2 and sums[_][0]%6==0:
                    for dir in [dirs[_]]:
                        a,b=i+dir[0],j+dir[1]
                        while a in range(4)and b in range(5):
                            p=a*5+b
                            t=status[p]
                            a,b=a+dir[0],b+dir[1]
                            if t==0:continue
                            if t%11==0:break
                            kill[p]=True
        kill=[_ for _ in range(20)if kill[_]]
        for _ in kill:
            status[19+status[_]%11+status[_]//11*15]=3
            status[_]=0
        return kill
def choices(status:list[int])->list[int]:
    return [i for i in range(300)if canput(status,i)]
def evaluate(status:list[int])->tuple[int]:
    return sum([_-20 for _ in range(20,30)if status[_]!=3]),sum([_-35 for _ in range(35,45)if status[_]!=3])
def reverse(status:list[int])->list[int]:
    for i in range(20):
        if status[i]==0:continue
        if status[i] in range(1,12):status[i]+=11
        elif status[i] in range(12,23):status[i]-=11
    status[20:35],status[35:50]=status[35:50],status[20:35]
    return status
def is_gameover(status:list[int])->bool:
    return not choices(status) and not choices(reverse([_ for _ in status]))
def main():
    print("Sixth")
    sto=storage()
    sto.display()
    turn=0
    while True:
        if turn:sto.reverse()
        if sto.choices():
            res=input("{}:".format("\033[31mP1\033[0m"if turn==0 else"\033[34mP2\033[0m"))
            if res in input_args:res=input_args.index(res)
            if sto.canput(res):
                args=sto.putf(res)
                if turn:sto.reverse()
                sto.display()
                while True:
                    args=sto.update(args)
                    if args:sto.display()
                    else:break
                turn=not turn
            else:print("Not Puttable")
        elif sto.choices(reverse([_ for _ in sto.status])):
            print("{}:None".format("\033[31mP1\033[0m"if turn==0 else"\033[34mP2\033[0m"))
            sto.turn=not sto.turn
        else:break
    if turn:sto.reverse()
    p1,p2=sto.evaluate()
    if p1==p2:input("Draw!%d:%d"%(p1,p2))
    else:input("{} Won! {}:{}".format("\033[31mP1\033[0m"if turn==0 else"\033[34mP2\033[0m",p1,p2))
    return
if __name__=="__main__":main()